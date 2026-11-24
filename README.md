# NEXO ALPHA — nome provisório

Produto independente de gestão de eventos e grupos corporativos. O repositório legado **Zuma-Lab/nexo** é apenas referência de regras de negócio; não deve ser editado como parte do Alpha.

## Ponto único de retomada e identidade

**Nome provisório:** NEXO Alpha; marca e domínio definitivos não foram escolhidos. `nexo.com.br` não será assumido. Alternativas de naming citadas: Benexo, Nexobe e Bnexo, ainda sem validação.

- **[Pasta de governança](governanca/README.md)** — regras, decisões, cronologia, riscos, roadmap e processo de revisão, todos com data de alteração.
- **[Roadmap de ponta a ponta](governanca/ROADMAP.md)** — M0 a M9, início/meio/fim, critérios de saída e dependências.
- **[Brandbook v2](design/brandbook-v2/BRANDBOOK_V2.md)** — guia completo, tokens canônicos e gerador PDF versionado.
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

- [Homepage do produto](homepage/README.md) — site estático responsivo, com demonstração ilustrativa de briefing V1/V2, comparação de fornecedores, perfis, login e formulário conectados à API Alpha.
- [API e workspace Alpha recuperados](alpha-snapshot/README.md) — aplicação FastAPI/SQLite e frontend independente. A interface interna ainda precisa de remodelagem completa com base no brandbook. **Não confundir snapshot com sistema homologado em produção.**
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

A homepage aprovada como **direção A** é centrada no produto, não na fotografia de executivo. Imagens de briefings e fotografias de explorações anteriores continuam preservadas como referências, mas não são apresentadas como telas reais. A fonte Inter é servida pelo Google Fonts nesta etapa; hospedagem local e otimizações de privacidade permanecem pendentes.

**Domínio:** `og:url`/canonical devem ser adicionados com a URL pública definitiva na implantação. A imagem `og:image` aponta provisoriamente para um PNG público do próprio repositório. Não usar o endereço privado da prévia ChatGPT.

## Verificação

A automação em `.github/workflows/alpha-ci.yml` verifica sintaxe e roda os testes Python em pull requests. Não presumir que um teste não executado passou.

Para consultar leads da homepage por API, configurar `NEXO_LEADS_ADMIN_EMAIL` com o e-mail exato do operador autorizado; administradores de workspaces de clientes não recebem acesso aos leads globais por padrão.

**Regras de briefing por serviço:** [validação Python](alpha-snapshot/backend/briefing_rules.py) reproduz as decisões e casos essenciais de `Zuma-Lab/nexo/briefing-rules.js` (sem importar código ou frontend). O editor visual por serviço e o editor completo de propostas continuam planejados na issue #2.
