# NEXO ALPHA — nome provisório

Produto independente de gestão de eventos e grupos corporativos. O repositório legado **Zuma-Lab/nexo** é apenas referência de regras de negócio; não deve ser editado como parte do Alpha.

## Ponto único de retomada e identidade

**Nome provisório:** NEXO Alpha; marca e domínio definitivos não foram escolhidos. `nexo.com.br` não será assumido. Alternativas de naming citadas: Benexo, Nexobe e Bnexo, ainda sem validação.

- **[Pasta de governança](governanca/README.md)** — regras, decisões, cronologia, riscos, roadmap e processo de revisão, todos com data de alteração.
- **[Roadmap de ponta a ponta](governanca/ROADMAP.md)** — M0 a M9, início/meio/fim, critérios de saída e dependências.
- **[Brandbook v2.1](design/brandbook-v2/BRANDBOOK_V2.md)** — guia completo, tokens canônicos e gerador PDF versionado.
- **[Galeria de telas reais](evidencias/capturas/README.md)** — capturas da branch em desktop e mobile; conferir manifesto e data.

## Retomar em outro computador

```bash
git clone https://github.com/Zuma-Lab/nexoalpha.git
cd nexoalpha
git fetch origin
git switch feat/homepage-produto-revisao-claude-20261123
cd alpha-snapshot
python -m pip install -r requirements.txt pytest httpx
NEXO_DEMO=1 uvicorn backend.main:app --host 127.0.0.1 --port 8000
```

O comando `NEXO_DEMO=1` é exemplo para shell Unix; em PowerShell use `$env:NEXO_DEMO='1'`. Abra `http://127.0.0.1:8000/`. Não publicar a configuração demo.

**Situação:** arquivos de trabalho e imagens/PDF ficam na branch do PR #1 até serem revisados e mesclados; a `main` ainda preserva a versão anterior.

## Estado de implementação

- [Homepage editorial B](homepage/README.md) — recontada pelo caso concreto de briefing alterado, impacto operacional ilustrativo, room nights, comparação de fornecedores e acessos; login e formulário conectados à API.
- [API e workspace V2 ativo](alpha-snapshot/README.md) — interface nova em `alpha-snapshot/workspace-v2/`, servida por `/app`. Fila por operação, projeto, wizard de briefing, RFQ manual, custos e propostas ligados à API. `alpha-snapshot/frontend/` permanece histórico. **O novo workspace ainda não está homologado em produção.**
- [Design tokens canônicos](design/brandbook-v2/nexo-tokens.json) — grafite, laranja `#FF850D`, off-white e Inter.
- [Produto e regras](produto/FUNCIONALIDADES_E_REGRAS.md) — escopo, fluxos e requisitos.
- [Histórico](historico/LEIA_PRIMEIRO.md) e [handoff anterior](handoff/ESTADO_ATUAL_2026-11-23.md) — registros de decisões passadas, não estado atual do código.

## Executar em conjunto

```bash
cd alpha-snapshot
python -m pip install -r requirements.txt
NEXO_DEMO=1 uvicorn backend.main:app --reload
```

Abrir `http://127.0.0.1:8000/` para a homepage e `http://127.0.0.1:8000/app` para o workspace. Os formulários usam a mesma origem que a API e não funcionam sem backend.

**Segurança de produção:** configurar TLS e `NEXO_SECURE_COOKIES=1`, além de `NEXO_RATE_LIMIT_SECRET` fixo e secreto; desativar `NEXO_DEMO`, trocar credenciais e configurar banco, backup, observabilidade, domínio, políticas de privacidade e envio de leads. API e frontend exigem revisão e testes antes de publicar.

## Decisões de identidade e apresentação

A homepage atual em revisão é a **direção editorial B**, centrada em consequências de mudanças do briefing, sem fotografia artificial ou template SaaS simétrico. Imagens de briefings e fotografias de explorações anteriores continuam preservadas como referências, mas não são apresentadas como telas reais. A fonte Inter é servida pelo Google Fonts nesta etapa; hospedagem local e otimizações de privacidade permanecem pendentes.

**Domínio:** `og:url`/canonical devem ser adicionados com a URL pública definitiva na implantação. A imagem `og:image` aponta provisoriamente para um PNG público do próprio repositório. Não usar o endereço privado da prévia ChatGPT.

## Verificação

A automação em `.github/workflows/alpha-ci.yml` verifica sintaxe e roda os testes Python em pull requests. Não presumir que um teste não executado passou.

Para consultar leads da homepage por API, configurar `NEXO_LEADS_ADMIN_EMAIL` com o e-mail exato do operador autorizado; administradores de workspaces de clientes não recebem acesso aos leads globais por padrão.

**Regras de briefing por serviço:** [validação Python](alpha-snapshot/backend/briefing_rules.py) implementa casos essenciais das regras recuperadas, sem importar frontend legado. O wizard visual V2 já existe; rascunhos persistentes, editor de cláusulas da proposta e paridade completa de regras ainda estão planejados na issue #2.
