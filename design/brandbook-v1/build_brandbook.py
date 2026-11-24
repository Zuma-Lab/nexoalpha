from pathlib import Path
import json, hashlib
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from PIL import Image
import pypdfium2 as pdfium

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'NEXO-Brandbook-v1.pdf'
pdfmetrics.registerFont(TTFont('Arial','C:/Windows/Fonts/arial.ttf'))
pdfmetrics.registerFont(TTFont('ArialB','C:/Windows/Fonts/arialbd.ttf'))
C={'graphite':'#111315','canvas':'#0B0D0F','surface':'#1B1D20','raised':'#25282C','border':'#454A50','orange':'#FF850D','hover':'#F5A044','pressed':'#E77300','cream':'#F3EFE9','white':'#FFFFFF','muted':'#B8BDC4','ink':'#111315','light-muted':'#565C63','light-border':'#D9D4CD','orange-text':'#A84800','success':'#B9E56C','warning':'#FFD166','danger':'#FF9A9A','info':'#9DC8FF'}
W,H=960,600
c=canvas.Canvas(str(OUT),pagesize=(W,H))
c.setTitle('NEXO | Brandbook e padrões de interface | v1.0')
c.setAuthor('NEXO')
page=0
def rect(x,y,w,h,color,r=0):
    c.setFillColor(HexColor(color));c.setStrokeColor(HexColor(color))
    if r:c.roundRect(x,y,w,h,r,fill=1,stroke=0)
    else:c.rect(x,y,w,h,fill=1,stroke=0)
def txt(x,y,text,size=14,color=None,bold=False):
    c.setFillColor(HexColor(color or C['white']));c.setFont('ArialB' if bold else 'Arial',size);c.drawString(x,y,text)
def para(x,y,text,width=400,size=13,color=None):
    p=Paragraph(text,ParagraphStyle('p',fontName='Arial',fontSize=size,leading=size*1.48,textColor=HexColor(color or C['muted'])))
    _,h=p.wrap(width,500);p.drawOn(c,x,y-h);return y-h
def base(kicker,title,sub='',light=False):
    global page
    page+=1;rect(0,0,W,H,C['cream'] if light else C['graphite'])
    fg=C['ink'] if light else C['white']
    txt(46,558,'NEXO  /  '+kicker.upper(),10,C['orange-text'] if light else C['orange'],True)
    txt(46,510,title,30,fg,True)
    if sub:para(46,486,sub,850,12,C['light-muted'] if light else C['muted'])
    txt(46,23,'BRANDBOOK 1.0  •  23 NOV 2026',9,C['light-muted'] if light else C['muted'])
    txt(875,23,f'{page:02d}',10,C['light-muted'] if light else C['muted'])
def end():c.showPage()
def img(name,x,y,w,h):
    p=ROOT/'assets'/name
    im=Image.open(p); iw,ih=im.size;s=min(w/iw,h/ih)
    c.drawImage(str(p),x+(w-iw*s)/2,y+(h-ih*s)/2,iw*s,ih*s,mask='auto')
def block(x,y,title,body,w=400):
    txt(x,y,title,17,C['white'],True);para(x,y-15,body,w)

base('Sistema de marca','Clareza para conectar toda a operação.','Identidade visual e regras de aplicação para os próximos layouts NEXO.')
img('07-logo-recorte-original.png',46,310,210,96)
txt(46,264,'Uma marca. Três referências.',23,C['white'],True)
para(46,240,'Homepage aprovada + briefing por etapas + briefing inteligente. Grafite, laranja e luz quente formam a linguagem comum da plataforma.',390,16)
rect(510,115,400,315,C['surface'],20)
for i,(co,n) in enumerate([(C['orange'],'Laranja / ação'),(C['cream'],'Off-white / respiro'),(C['graphite'],'Grafite / estrutura')]):
    rect(535,330-i*75,52,52,co,10);txt(605,348-i*75,n,16)
para(46,104,'Escopo digital • versão 1.0. As referências visuais orientam a marca; este manual formaliza os valores e comportamentos necessários para implementá-la.',850,11)
end()

base('01 / Referências','A origem da linguagem visual.','Usar os arquivos de referência originais; não usar o dashboard azul ou o login antigo como padrão.')
img('01-homepage-primeira-aprovada.png',46,115,285,330)
img('05-briefing-etapas-exploratorio.png',355,282,555,165)
img('06-briefing-inteligente-exploratorio.png',355,80,555,190)
txt(46,92,'Homepage: direção aprovada.',11,C['orange'],True)
para(46,78,'Mockups internos: referências de linguagem, sem afirmar funcionalidades já prontas.',280,10)
end()

base('02 / Princípios','Executiva. Clara. Conectada.')
block(46,425,'01  Hierarquia antes da decoração','Uma ação principal por contexto. Títulos curtos, informação agrupada e espaço para leitura. O laranja indica foco, seleção e avanço.')
block(510,425,'02  Profundidade com controle','Grafite em camadas e iluminação quente localizada. Fotografias e reflexos ficam fora das regiões de leitura densa.')
block(46,305,'03  Continuidade entre telas','A mesma marca, tipografia, escala de espaçamento, botões, cards e estados acompanham o usuário da homepage à operação.')
block(510,305,'04  Confiança por precisão','Valores, estados e confirmações devem ser claros. Distinguir dado sugerido de dado confirmado. Não inventar clientes ou resultados.')
rect(46,90,864,100,C['surface'],14)
para(66,168,'Consolidado das referências: paleta grafite/laranja/off-white, marca em minúsculas, contraste, cards e ícones lineares.<br/><br/>Formalizado nesta versão: valores exatos dos tokens, fonte de interface, dimensões, estados, responsividade e regras de acessibilidade. São especificações propostas para implementação, não medições exatas dos pixels dos mockups.',820,12)
end()

base('03 / Logotipo','Preservar o desenho da marca.')
img('07-logo-recorte-original.png',68,285,280,130)
block(440,420,'Assinatura principal','Símbolo angular laranja à esquerda + “nexo” branca em minúsculas. Usar sobre superfície grafite uniforme.',450)
block(440,320,'Área de proteção','Adotar x como altura do símbolo. Reservar ao menos 0,5x ao redor da assinatura e manter a proporção original entre símbolo e nome.',450)
block(46,235,'Tamanho e reprodução','Referência para o futuro vetor: largura mínima digital de 100 px; símbolo isolado a partir de 24 px, após teste de legibilidade. O recorte atual é pequeno e não deve ser ampliado como arquivo final.')
block(510,235,'Usos que descaracterizam','Não redesenhar com fonte digitada, esticar, rotacionar, adicionar brilho, alterar a geometria ou colocar sobre fotografia sem proteção. Em fundo claro, usar placa grafite até existir variante validada.')
para(46,85,'Entrega de marca pendente: vetor mestre SVG e variantes monocromáticas/claras conferidas com o recorte original. O logo HD gerado não substitui automaticamente a referência.',850,12,C['orange'])
end()

base('04 / Cores','Paleta principal e superfícies.','Valores sRGB normalizados para esta versão. Não são uma extração instrumental dos mockups.')
swatches=[('graphite','Grafite / base'),('orange','Laranja / ação'),('cream','Off-white / respiro'),('white','Branco / texto'),('canvas','Fundo profundo'),('surface','Card escuro'),('raised','Elevação'),('border','Borda funcional')]
for i,(key,name) in enumerate(swatches):
    x=46+(i%4)*220;y=290-(i//4)*170
    rect(x,y,200,115,C[key],14)
    txt(x,y-24,name,12,C['white'],True);txt(x,y-44,C[key],11,C['muted'])
end()

def lum(h):
    rgb=[int(h[i:i+2],16)/255 for i in (1,3,5)]
    a=[v/12.92 if v<=.04045 else ((v+.055)/1.055)**2.4 for v in rgb]
    return sum(v*w for v,w in zip(a,[.2126,.7152,.0722]))
def ratio(a,b):
    x,y=sorted([lum(a),lum(b)]);return (y+.05)/(x+.05)
base('05 / Contraste','Cor bonita também precisa ser legível.')
pairs=[('Texto principal','white','graphite'),('Texto secundário','muted','graphite'),('Botão primário','graphite','orange'),('Texto em área clara','graphite','cream'),('Link em área clara','orange-text','cream')]
for i,(label,fg,bg) in enumerate(pairs):
    y=402-i*60;rect(46,y-15,320,44,C[bg],8);txt(60,y,label,14,C[fg],True)
    txt(395,y,f'{C[fg]} / {C[bg]}',12);txt(690,y,f'{ratio(C[fg],C[bg]):.2f}:1',15,C['orange'],True)
para(46,95,'Regra para texto normal: mínimo 4,5:1. O branco sobre o laranja principal tem apenas '+f"{ratio(C['white'],C['orange']):.2f}:1"+'; por isso, usar texto grafite nos botões laranja. Esta adaptação preserva a marca e melhora a leitura. Foco: contorno de 2 px, afastado 3 px; branco no tema escuro e grafite no claro.',850,12)
end()

base('06 / Tipografia','Uma voz visual, em todas as telas.','Família proposta: Inter, pesos 400, 500, 600 e 700. Fallback: Arial, sans-serif. O PDF usa Arial.')
for y,size,label in [(418,44,'Da solicitação à execução.'),(350,32,'Tudo conectado, em um só lugar.'),(293,24,'Confirme as informações do projeto.'),(245,16,'Revise os dados antes de continuar.')]:txt(46,y,label,size,C['white'],size>16)
block(46,170,'Escala para interfaces','Hero: 56/62 desktop e 36/40 mobile. Título de página: 32/40. Seção: 24/32. Card: 18/26. Corpo: 16/24. Apoio: 14/20. Metadado: 12/18.')
block(510,170,'Regras de composição','Títulos em frase, sem excesso de caixa alta. Texto corrido com 45–75 caracteres por linha. Valores financeiros alinhados à direita e números tabulares. Nunca usar texto incorporado em imagem como conteúdo funcional.')
end()

base('07 / Estrutura','Ritmo, proporção e respiro.')
block(46,425,'Espaçamento','Escala: 4, 8, 12, 16, 24, 32, 48, 64 e 96 px. Cards: 24 px de padding; 16 px no mobile. Entre grupos: 32 px. Seções de marketing: 96 px desktop / 56 px mobile.')
block(510,425,'Grade responsiva','Conteúdo até 1280 px. Margens laterais: 48 / 24 / 16 px. Desktop a partir de 1200 px: 12 colunas. Tablet: 8. Mobile abaixo de 768 px: 4. Sidebar: 240 px, recolhida em telas menores.')
block(46,290,'Formas','Inputs: raio 10 px. Cards: 16 px. Grandes painéis: 24 px. Botões principais: cápsula. Bordas finas; brilho laranja apenas discreto em seleção. Evitar excesso de sombras.')
block(510,290,'Densidade operacional','Inputs e botões com 48 px de altura; área clicável mínima de 44 px. Tabelas com linhas de 48–56 px. Não reduzir fonte para caber: agrupar, oferecer detalhe ou rolagem contida.')
rect(46,92,864,78,C['surface'],16)
txt(68,139,'Movimento discreto',17,C['white'],True)
para(68,125,'Transições de 160–220 ms para cor, opacidade e abertura. Respeitar prefers-reduced-motion. Não usar parallax ou animação contínua em formulários e tabelas.',820,12)
end()

base('08 / Componentes','Regras que tornam o produto reconhecível.')
rect(46,371,235,50,C['orange'],25);txt(72,389,'Confirmar e continuar',15,C['graphite'],True)
rect(305,371,180,50,C['raised'],25);txt(341,389,'Salvar rascunho',14)
para(46,350,'Primário: laranja + texto grafite. Hover '+C['hover']+'. Pressionado '+C['pressed']+'. Secundário: superfície neutra. Ação destrutiva: vermelho sem confundir com o primário.',435,12)
rect(520,298,390,123,C['surface'],16)
txt(540,390,'Evento corporativo',19,C['white'],True)
para(540,371,'Card selecionável: borda laranja, ícone de confirmação e texto. Não depender somente da cor.',347,13)
block(46,247,'Campos e formulários','Rótulo sempre visível. Ajuda abaixo do campo. Erro junto ao campo e resumo no envio. Manter o que foi digitado. Obrigatoriedade explícita; placeholder nunca substitui rótulo.')
block(510,247,'Estados completos','Prever padrão, hover, foco, selecionado, desabilitado, carregando, erro, vazio e sucesso. Em envio: “Salvando…” e proteção contra duplo clique. No sucesso: confirmar o resultado real.')
for i,(key,label) in enumerate([('success','Confirmado'),('warning','Pendente'),('danger','Erro'),('info','Informação')]):
    x=46+i*220;rect(x,78,200,44,C['surface'],10);txt(x+15,94,label,14,C[key],True)
end()

base('09 / Aplicação','Homepage e produto: a mesma marca.')
block(46,425,'Homepage / descoberta','Hero amplo com executivo e cidade ao entardecer. Texto à esquerda e prévia do produto à direita. Overlay grafite garante leitura. Seções claras criam respiro; benefícios entram no meio da rolagem.')
block(510,425,'Produto / execução','Sidebar grafite, item ativo laranja, título e contexto persistentes. Cards escuros e iluminação quente periférica. Em telas financeiras densas, priorizar superfícies sólidas e hierarquia de dados.')
block(46,285,'Briefing por etapas','Usar progresso com etapa atual nomeada, passos concluídos e retorno seguro. Cards com seleção explícita. No mobile, mostrar “Etapa X de Y” e título atual; preservar preenchimento ao voltar.')
block(510,285,'Briefing inteligente','Apresentar origem do dado sugerido, permitir editar e pedir confirmação. “Salvo” somente após persistência. Histórico não significa dado correto: nunca confirmar automaticamente pelo usuário.')
para(46,112,'A ordem final da homepage segue as decisões documentadas: hero → módulos → benefícios → fluxo → produto em ação → confiança → CTA. As marcas de terceiros visíveis no mockup não são clientes comprovados e não devem ser copiadas para a página publicada.',850,12,C['orange'])
end()

base('10 / Imagem e linguagem','Luz quente. Mensagens claras.')
block(46,425,'Fotografia','Arquitetura, encontros e cidade ao entardecer; composição com profundidade e espaço negativo para o texto. Fotografias devem ser licenciadas ou produzidas para a marca. Evitar fundos competindo com formulários.')
block(510,425,'Ícones','Um único conjunto linear, grid de 24 px, traço de 1,5–2 px. Cinza/branco no estado padrão, laranja no ativo. Ícones isolados precisam de nome acessível e tooltip quando necessário.')
block(46,285,'Tom de voz','Profissional, direto e acolhedor. Usar verbos concretos: Criar briefing, Comparar propostas, Revisar informações. Evitar jargões, mensagens vagas e promessas que o sistema não cumpre.')
block(510,285,'Mensagens de referência','Vazio: “Você ainda não criou um briefing.”<br/>Erro: “Não foi possível salvar. Seus dados continuam aqui. Tente novamente.”<br/>Sucesso: “Briefing salvo.”<br/>Sugestão: “Dados sugeridos pelo histórico. Revise antes de confirmar.”')
para(46,95,'Evitar: azul como cor principal; amarelo de identidade antiga; novos gradientes multicoloridos; brilho em todo elemento; texto branco pequeno sobre laranja; telas antigas como referência; dados e depoimentos fictícios tratados como reais.',850,13,C['orange'])
end()

base('11 / Governança','Um padrão que acompanha a evolução.')
block(46,425,'Checklist de cada layout','1. Usa os tokens desta versão?<br/>2. Preserva marca e hierarquia?<br/>3. Tem uma ação principal clara?<br/>4. Inclui estados e mensagens?<br/>5. Funciona em 390, 768 e 1440 px?<br/>6. Funciona com teclado e foco visível?<br/>7. Mantém contraste e dados legíveis?')
block(510,425,'Versionamento','Manter PDF, tokens CSS e JSON sincronizados. Ajustes de valores e componentes: versão 1.x. Mudança estrutural de identidade: versão 2.0. Registrar motivo, data e telas afetadas. Novos layouts devem referenciar a versão utilizada.')
block(510,250,'Próximos ativos da marca','Vetor mestre do logo, variante clara, versão monocromática, favicon e arquivo de fonte licenciado para distribuição. Até lá, preservar o recorte original e usar fallbacks de tipografia.')
para(46,178,'Fontes de referência',400,14,C['orange'])
url='https://github.com/Zuma-Lab/nexoalpha'
para(46,154,'Repositório: Zuma-Lab/nexoalpha<br/>assets/visuals/: imagens 01, 05, 06 e 07.<br/>design/HOMEPAGE_DETALHADA.md<br/>design/IDENTIDADE_VISUAL_NEXO.md<br/>Commit de referência: 7dfa55bc2c47.',430,11)
c.linkURL(url,(46,70,470,160),relative=0)
end();c.save()

tokens={'brand':'NEXO','version':'1.0.0','date':'2026-11-23','status':'Padrão proposto de implementação baseado nas referências visuais','colors':C,'font':{'family':'Inter, Arial, sans-serif','weights':[400,500,600,700]},'spacing':[4,8,12,16,24,32,48,64,96],'radius':{'input':10,'card':16,'panel':24,'pill':999},'breakpoints':{'tablet':768,'desktop':1200},'motion':{'fast':'160ms','normal':'220ms'},'references':[]}
for p in sorted((ROOT/'assets').glob('*.png')):tokens['references'].append({'file':p.name,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
(ROOT/'nexo-tokens.json').write_text(json.dumps(tokens,ensure_ascii=False,indent=2),encoding='utf-8')
css=['/* NEXO Brandbook v1.0 | 2026-11-23 | valores normalizados propostos */',':root {']
css += [f'  --nexo-{k}: {v};' for k,v in C.items()]
css += ['  --nexo-font: Inter, Arial, sans-serif;']
css += [f'  --nexo-space-{v}: {v}px;' for v in tokens['spacing']]
css += [f'  --nexo-radius-{k}: {v}px;' for k,v in tokens['radius'].items()]
css += ['  --nexo-motion-fast: 160ms;','  --nexo-motion-normal: 220ms;','  --nexo-bg: var(--nexo-graphite);','  --nexo-text: var(--nexo-white);','  --nexo-text-muted: var(--nexo-muted);','  --nexo-action-bg: var(--nexo-orange);','  --nexo-action-text: var(--nexo-graphite);','  --nexo-focus: var(--nexo-white);','}', '[data-nexo-theme="light"] {','  --nexo-bg: var(--nexo-cream);','  --nexo-text: var(--nexo-graphite);','  --nexo-text-muted: var(--nexo-light-muted);','  --nexo-focus: var(--nexo-graphite);','}', '@media (prefers-reduced-motion: reduce) {', '  :root { --nexo-motion-fast: 0ms; --nexo-motion-normal: 0ms; }','}']
(ROOT/'nexo-tokens.css').write_text('\n'.join(css)+'\n',encoding='utf-8')
(ROOT/'LEIA-ME.txt').write_text('NEXO BRANDBOOK 1.0\n\nPDF: manual visual de referência.\nCSS e JSON: valores normalizados para novos layouts; não alteram o sistema existente automaticamente.\nassets/: referências originais de homepage, briefings e logo.\nO PDF distingue direção aprovada de especificações propostas nesta versão. Fonte Inter proposta; Arial usada no PDF. Logo vetor ainda pendente.\nManter os três arquivos sincronizados ao alterar a marca.\nOs arquivos foram preparados localmente; publicação no GitHub não realizada.\n',encoding='utf-8')
qa=ROOT/'qa';qa.mkdir(exist_ok=True)
doc=pdfium.PdfDocument(str(OUT))
thumbs=[]
for i in range(len(doc)):
    im=doc[i].render(scale=1.3).to_pil();im.save(qa/f'page-{i+1:02d}.png')
    im.thumbnail((480,300));thumbs.append(im.copy())
for start in range(0,len(thumbs),4):
    sheet=Image.new('RGB',(960,600),'white')
    for j,im in enumerate(thumbs[start:start+4]):sheet.paste(im,((j%2)*480,(j//2)*300))
    sheet.save(qa/f'sheet-{start//4+1}.png')
print(f'Created {len(doc)} pages: {OUT}')
print('Contrast:',{f'{a}/{b}':round(ratio(C[a],C[b]),2) for _,a,b in pairs})
