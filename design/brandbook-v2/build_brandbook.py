"""Brandbook v2 — gerador reprodutível (PDF) a partir de fonte Markdown e tokens JSON.
Não altera brandbook v1. Executar: python design/brandbook-v2/build_brandbook.py
Requer reportlab + pillow. Capturas de navegador opcionais no final do PDF.
"""
from __future__ import annotations
import html
import json
import re
from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, LongTable, TableStyle,
    Image, KeepTogether, Preformatted, Flowable
)

ROOT=Path(__file__).resolve().parent
REPO=ROOT.parents[1]
SRC=ROOT/"BRANDBOOK_V2.md"
JSON=ROOT/"nexo-tokens.json"
OUTPUT=ROOT/"NEXO-Alpha-Brandbook-v2.pdf"
TOKENS=json.loads(JSON.read_text(encoding="utf-8"))
C={key:HexColor(value) for key,value in TOKENS["colors"].items()}
PAGE_W,PAGE_H=A4

font_candidates=[
 ("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
  "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
  "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"),
 ("/usr/local/share/fonts/DejaVuSans.ttf",
  "/usr/local/share/fonts/DejaVuSans-Bold.ttf",
  "/usr/local/share/fonts/DejaVuSansMono.ttf"),
]
regular,bold,mono="Helvetica","Helvetica-Bold","Courier"
for reg_path,b_path,m_path in font_candidates:
    if Path(reg_path).exists() and Path(b_path).exists():
        pdfmetrics.registerFont(TTFont("NexoPDF",reg_path))
        pdfmetrics.registerFont(TTFont("NexoPDF-Bold",b_path))
        regular,bold="NexoPDF","NexoPDF-Bold"
        if Path(m_path).exists():
            pdfmetrics.registerFont(TTFont("NexoPDF-Mono",m_path))
            mono="NexoPDF-Mono"
        break

def style(name,font,size,leading,color,space_after=0,space_before=0,indent=0):
    return ParagraphStyle(name,fontName=font,fontSize=size,leading=leading,
        textColor=color,spaceAfter=space_after,spaceBefore=space_before,
        leftIndent=indent,alignment=TA_LEFT,allowWidows=0,allowOrphans=0)

S={
 "cover_mark":style("cover_mark",bold,16,22,C["orange"],24),
 "cover_title":style("cover_title",bold,46,54,C["white"],18),
 "cover_sub":style("cover_sub",regular,18,28,C["muted"],28),
 "cover_note":style("cover_note",regular,11,18,C["muted"],16),
 "major":style("major",bold,20,28,C["graphite"],15,22),
 "minor":style("minor",bold,12,19,C["graphite"],9,14),
 "body":style("body",regular,9.4,15,C["graphite"],9),
 "bullet":style("bullet",regular,9.2,14.7,C["graphite"],6,0,15),
 "caption":style("caption",regular,8.5,13,C["light_muted"],12),
 "note":style("note",regular,9,14,C["graphite"],4),
 "table":style("table",regular,8.1,12,C["graphite"],0),
 "table_header":style("table_header",bold,8.4,12,C["white"],0),
 "table_tiny":style("table_tiny",regular,7.7,11.4,C["graphite"],0),
}
PAGE_CONTENT=PAGE_W-92

def fmt(text:str)->str:
    s=escape(text.strip())
    # Inline styling is intentionally limited to Markdown used in the canonical source.
    s=re.sub(r"\*\*(.+?)\*\*",r"<b>\1</b>",s)
    s=re.sub(r"`([^`]+)`",lambda m:'<font color="#A84800">'+m.group(1)+'</font>',s)
    s=re.sub(r"\[([^\]]+)\]\(([^)]+)\)",r"\1",s)
    return s

def p(text,kind="body"):
    return Paragraph(fmt(text),S[kind])

def footer(canvas,doc):
    canvas.saveState()
    if doc.page==1:
        canvas.setFillColor(C["graphite"])
        canvas.rect(0,0,PAGE_W,PAGE_H,fill=1,stroke=0)
        canvas.setFillColor(C["orange"])
        canvas.rect(46,PAGE_H-62,70,4,fill=1,stroke=0)
        canvas.rect(0,0,14,PAGE_H,fill=1,stroke=0)
        canvas.setStrokeColor(C["border"])
        canvas.line(46,99,PAGE_W-46,99)
        canvas.setFont(regular,8.8)
        canvas.setFillColor(C["muted"])
        canvas.drawString(46,76,"NOME DE TRABALHO • MARCA DEFINITIVA EM ABERTO")
        canvas.drawString(46,58,"2026-11-24  |  BRANDBOOK 2.1  |  REPOSITÓRIO NEXO ALPHA")
    else:
        canvas.setFillColor(C["cream"])
        canvas.rect(0,0,PAGE_W,PAGE_H,fill=1,stroke=0)
        canvas.setFillColor(C["graphite"])
        canvas.rect(0,PAGE_H-54,PAGE_W,54,fill=1,stroke=0)
        canvas.setFillColor(C["orange"])
        canvas.rect(46,PAGE_H-54,41,3,fill=1,stroke=0)
        canvas.setFillColor(C["white"])
        canvas.setFont(bold,10.3)
        canvas.drawString(46,PAGE_H-34,"NEXO ALPHA  /  BRANDBOOK V2")
        canvas.setFont(regular,8)
        canvas.setFillColor(C["muted"])
        canvas.drawRightString(PAGE_W-46,PAGE_H-33,"IDENTIDADE PROVISÓRIA")
        canvas.setStrokeColor(C["light_border"])
        canvas.line(46,46,PAGE_W-46,46)
        canvas.setFont(regular,8)
        canvas.setFillColor(C["light_muted"])
        canvas.drawString(46,32,"2026-11-24 • Fonte: brandbook-v2 + governança")
        canvas.drawRightString(PAGE_W-46,32,f"{doc.page:02d}")
    canvas.restoreState()

class Palette(Flowable):
    def __init__(self,entries):
        super().__init__()
        self.entries=entries
        self.width=PAGE_CONTENT
        self.height=300
    def draw(self):
        from reportlab.pdfbase.pdfmetrics import stringWidth
        columns=4
        gap=10
        cell_w=(self.width-(columns-1)*gap)/columns
        cell_h=65
        for index,(label,code) in enumerate(self.entries[:16]):
            col=index%columns
            row=index//columns
            x=col*(cell_w+gap)
            y=self.height-(row+1)*cell_h-8*row
            self.canv.setFillColor(HexColor(code))
            self.canv.roundRect(x,y+20,cell_w,45,7,fill=1,stroke=0)
            self.canv.setFillColor(C["graphite"])
            self.canv.setFont(bold,7.7)
            self.canv.drawString(x,y+7,label[:16].upper())
            self.canv.setFont(regular,7.7)
            self.canv.setFillColor(C["light_muted"])
            self.canv.drawRightString(x+cell_w,y+7,code)

def make_table(lines):
    values=[[x.strip() for x in line.strip().strip("|").split("|")] for line in lines]
    if len(values)>1 and all(re.fullmatch(r":?-+:?",part.replace(" ","")) for part in values[1]):
        values.pop(1)
    if not values:
        return None
    cols=max(len(x) for x in values)
    values=[row+[""]*(cols-len(row)) for row in values]
    if cols==4: fractions=[.16,.17,.49,.18]
    elif cols==3:
        if any("Token" in x for x in values[0]):fractions=[.22,.20,.58]
        else:fractions=[.22,.50,.28]
    elif cols==2:fractions=[.30,.70]
    else:fractions=[1/cols]*cols
    widths=[PAGE_CONTENT*x/sum(fractions) for x in fractions]
    cells=[]
    for index,row in enumerate(values):
        kind="table_header" if index==0 else "table_tiny" if cols>=4 else "table"
        cells.append([p(text,kind) for text in row])
    t=LongTable(cells,colWidths=widths,repeatRows=1,hAlign="LEFT")
    t.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,0),C["graphite"]),
        ("ROWBACKGROUNDS",(0,1),(-1,-1),[C["white"],C["cream"]]),
        ("VALIGN",(0,0),(-1,-1),"TOP"),
        ("LINEBELOW",(0,0),(-1,0),.7,C["orange"]),
        ("LINEBELOW",(0,1),(-1,-1),.23,C["light_border"]),
        ("LEFTPADDING",(0,0),(-1,-1),8),
        ("RIGHTPADDING",(0,0),(-1,-1),8),
        ("TOPPADDING",(0,0),(-1,-1),8),
        ("BOTTOMPADDING",(0,0),(-1,-1),8),
    ]))
    return t

def markdown_story(markdown):
    result=[]
    lines=markdown.splitlines()
    i=0
    palette_done=False
    while i<len(lines):
        line=lines[i].strip()
        if not line:
            i+=1
            continue
        if line.startswith("# ") or line.startswith("**Versão:**") or line.startswith("**PDF gerado:**"):
            i+=1
            continue
        if line.startswith("## "):
            title=line[3:].strip()
            result.append(Spacer(1,14))
            result.append(p(title,"major"))
            if title.startswith("03.") and not palette_done:
                result.append(Palette(list(TOKENS["colors"].items())))
                result.append(Spacer(1,12))
                palette_done=True
            i+=1
            continue
        if line.startswith("### "):
            result.append(p(line[4:],"minor"))
            i+=1
            continue
        if line.startswith("|"):
            table=[]
            while i<len(lines) and lines[i].strip().startswith("|"):
                table.append(lines[i].strip())
                i+=1
            rendered=make_table(table)
            if rendered:
                result.append(rendered)
                result.append(Spacer(1,12))
            continue
        if line.startswith(">"):
            note=[]
            while i<len(lines) and lines[i].strip().startswith(">"):
                note.append(lines[i].strip().lstrip(">").strip())
                i+=1
            note_text=" ".join(note)
            tab=LongTable([[p(note_text,"note")]],colWidths=[PAGE_CONTENT])
            tab.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),C["white"]),
                ("LINEBEFORE",(0,0),(0,-1),3,C["orange"]),
                ("LEFTPADDING",(0,0),(-1,-1),15),
                ("RIGHTPADDING",(0,0),(-1,-1),15),
                ("TOPPADDING",(0,0),(-1,-1),12),
                ("BOTTOMPADDING",(0,0),(-1,-1),12)]))
            result.extend([tab,Spacer(1,12)])
            continue
        if line.startswith("- ") or re.match(r"^\d+\. ",line):
            label=re.sub(r"^(- |\d+\. )","",line)
            result.append(p("• "+label,"bullet"))
            i+=1
            continue
        if line.startswith("```"):
            i+=1
            code=[]
            while i<len(lines) and not lines[i].startswith("```"):
                code.append(lines[i])
                i+=1
            i+=1
            result.append(Preformatted("\n".join(code),style("pre_"+str(i),mono,7.1,11,C["light_muted"],10)))
            continue
        if line.startswith("---"):
            i+=1
            continue
        paragraph=[line]
        i+=1
        while i<len(lines):
            nxt=lines[i].strip()
            if not nxt or nxt.startswith(("## ","### ","|",">","- ","```")) or re.match(r"^\d+\. ",nxt):
                break
            paragraph.append(nxt)
            i+=1
        result.append(p(" ".join(paragraph),"body"))
    return result

def add_screenshots(story):
    pic_dir=REPO/"evidencias"/"capturas"
    images=[
        ("home-hero-desktop.png","Hero real da homepage em 1440 × 960; valores simulados."),
        ("home-comparativo.png","Matriz comparativa na homepage; dados fictícios e rotulados."),
    ]
    found=[(pic_dir/name,cap) for name,cap in images if (pic_dir/name).is_file()]
    if not found:
        story.append(p("As capturas de implementação serão anexadas pelo pipeline quando disponíveis.","caption"))
        return
    story.append(PageBreak())
    story.append(p("Evidências visuais da branch","major"))
    story.append(p("Capturas geradas automaticamente pelo navegador a partir do HTML/CSS/JS efetivo e API local. Não são telas de produção.","body"))
    for filepath,cap in found:
        w,h=ImageReader(str(filepath)).getSize()
        max_w,max_h=PAGE_CONTENT,310
        ratio=min(max_w/w,max_h/h)
        im=Image(str(filepath),width=w*ratio,height=h*ratio)
        im.hAlign="CENTER"
        story.append(im)
        story.append(Spacer(1,7))
        story.append(p(cap,"caption"))
        story.append(Spacer(1,14))

def build():
    markdown=SRC.read_text(encoding="utf-8")
    doc=SimpleDocTemplate(str(OUTPUT),pagesize=A4,
        leftMargin=46,rightMargin=46,topMargin=72,bottomMargin=64,
        title="NEXO Alpha | Brandbook v2 (nome provisório)",
        author="Projeto NEXO Alpha",
        subject="Identidade visual provisória, padrões de produto, UX e governança")
    story=[
        Spacer(1,126),
        p("NEXO / ALPHA","cover_mark"),
        Paragraph("Brandbook<br/>de produto<br/>v2.1",S["cover_title"]),
        Paragraph("A operação como protagonista.<br/>Interface editorial, decisões rastreáveis.",S["cover_sub"]),
        Spacer(1,54),
        p("Identidade de trabalho: grafite, laranja e off-white. Nome, domínio e geometria final do logo permanecem em avaliação.","cover_note"),
        PageBreak(),
        p("Índice e status do documento","major"),
        p("Este PDF consolida as 12 seções do Markdown canônico. Cores e medidas são parâmetros de implementação, enquanto o nome, o domínio e o símbolo final não estão homologados.","body"),
        p("Registro da alteração: 2026-11-24 • Fonte: design/brandbook-v2/BRANDBOOK_V2.md","caption"),
        Spacer(1,17),
    ]
    story.extend(markdown_story(markdown))
    add_screenshots(story)
    doc.build(story,onFirstPage=footer,onLaterPages=footer)
    print("BRANDBOOK_PDF",OUTPUT,OUTPUT.stat().st_size)

if __name__=="__main__":
    build()
