"""Validação leve do catálogo de governança e tokens.
Executar: python scripts/validate_governance.py
"""
from __future__ import annotations
import json
import re
from datetime import date
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
GOV=ROOT/"governanca"
REGISTRY={
    "BR":GOV/"PADROES_E_REGRAS.md",
    "ADR":GOV/"DECISOES_ARQUITETURAIS.md",
    "CHG":GOV/"REGISTRO_DE_ALTERACOES.md",
}
ISO=re.compile(r"\d{4}-\d{2}-\d{2}")

def read(path:Path)->str:
    assert path.is_file(),f"Arquivo não encontrado: {path.relative_to(ROOT)}"
    content=path.read_text(encoding="utf-8")
    assert len(content)>100,f"Arquivo de governança inesperadamente curto: {path}"
    return content

def main():
    for prefix,path in REGISTRY.items():
        content=read(path)
        records=[line for line in content.splitlines()
                 if re.match(rf"^\|\s*{prefix}-\d{{3}}\s*\|",line)]
        assert records,f"Nenhuma entrada {prefix} com ID e data: {path}"
        ids=[]
        for line in records:
            id_=re.match(rf"^\|\s*({prefix}-\d{{3}})",line).group(1)
            m=ISO.search(line)
            assert m,f"{id_} não possui data ISO"
            date.fromisoformat(m.group(0))
            ids.append(id_)
        assert len(ids)==len(set(ids)),f"IDs duplicados em {path}: {ids}"
        print(prefix,":",len(ids),"entradas datadas")
    roadmap=read(GOV/"ROADMAP.md")
    for step in range(10):
        assert re.search(rf"\bM{step}\b",roadmap),f"Roadmap sem M{step}"
    tokens_path=ROOT/"design"/"brandbook-v2"/"nexo-tokens.json"
    tokens=json.loads(read(tokens_path))
    assert tokens["schema_version"].startswith("2.")
    assert tokens["identity"]["canonical_domain"] is None
    assert tokens["colors"]["orange"].upper()=="#FF850D"
    assert tokens["colors"]["graphite"].upper()=="#111315"
    for col in ("border","cream","muted","light_muted"):
        assert re.fullmatch(r"#[0-9A-Fa-f]{6}",tokens["colors"][col])
    assert (ROOT/"design/brandbook-v2/BRANDBOOK_V2.md").exists()
    assert (GOV/"README.md").exists()
    # Impede perda silenciosa dos padrões de controle de escopo aprovados.
    editorial=read(GOV/"GUIA_EDITORIAL_E_APROVACAO_HOMEPAGE.md")
    assert "NÃO autoriza" in editorial or "não autoriza" in editorial.lower()
    assert "propostas ainda sujeitas a aceite" in editorial or "aguardando aprovação" in editorial
    for rule in ("BR-051","BR-052","BR-053","BR-054","BR-055","BR-056"):
        assert rule in read(REGISTRY["BR"]),f"Regra editorial ausente: {rule}"
    for decision in ("ADR-023","ADR-024"):
        assert decision in read(REGISTRY["ADR"]),f"Decisão de escopo ausente: {decision}"
    print("Roadmap M0-M9 e tokens v2: OK")

if __name__=="__main__":
    main()
