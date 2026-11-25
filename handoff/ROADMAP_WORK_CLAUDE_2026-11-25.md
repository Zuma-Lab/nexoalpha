# NEXO ALPHA — Roadmap operacional e handoff Work/Claude Code

**Data:** 2026-11-25 (America/Sao_Paulo). **Status:** plano de execução, não relatório de implementação de etapas futuras. **Nome:** provisório.  
**Repositório ativo:** https://github.com/Zuma-Lab/nexoalpha  
**Branch-base de revisão:** `feat/homepage-produto-revisao-claude-20261123` (PR #1 draft)  
**Repositório protegido:** `Zuma-Lab/nexo` — **não escrever**, não criar PR nem copiar frontend/banco.  
**Regra de operação:** cada tarefa em branch própria criada da branch-base **atualizada**; PR draft direcionada à branch-base; não realizar merge/deploy sem aprovação do proprietário.

## 1. Estado real antes de executar

- A **copy** A/B está no HTML: “O evento é um só. A informação não deveria estar em tantos lugares.” no hero; “Sua equipe precisa conduzir eventos. Não reconstruir informações.” na primeira rolagem.
- O HTML atual da homepage está em `homepage/dist/` e ainda utiliza `.hero-note` na dobra inicial. A arte aprovada **com notebook** existe como **mockup gerado no chat**, **não** como elemento de notebook já implementado individualmente no HTML. O executor deve receber/anexar o PNG aprovado e inspecioná-lo antes de mudar qualquer layout. Não dizer que foi restaurado no site.
- Identidade de trabalho: grafite `#111315`, laranja `#FF850D`, creme `#F3EFE9`, Inter. Fonte canônica: `design/brandbook-v2/nexo-tokens.json`; **não mudar** identidade, proporções, logotipo ou cores.
- API ativa em `alpha-snapshot/backend/main.py`, FastAPI com SQLite de **desenvolvimento**, sem homologação de produção. `/` é homepage; `/app` é `alpha-snapshot/workspace-v2/`; `alpha-snapshot/frontend/` é **histórico**, não a UI ativa.
- Já existem briefings versionados, rascunho privado, RFQs com tokens, cotação com centavos/basis points, propostas versionadas, permissões e tarefas; há implementação parcial e riscos em segurança, comunicação real, anexos, unidades financeiras e homologação.
- O fluxo **não integra automaticamente** e-mails, CRM/ERP nem elimina a redigitação externa. Cenários e clientes exibidos na home são ilustrativos.
- PR #1 segue em draft. Considerar uma imagem, um PDF de brandbook ou um teste CI como evidência do item específico, não homologação integral.

## 2. Ordem de leitura no Work/Claude

1. `README.md`, `CLAUDE.md`, `governanca/GUIA_EDITORIAL_E_APROVACAO_HOMEPAGE.md`.
2. `governanca/PADROES_E_REGRAS.md`, `governanca/DECISOES_ARQUITETURAIS.md`, `governanca/REGISTRO_DE_ALTERACOES.md`, `governanca/PENDENCIAS_E_RISCOS.md`, `governanca/ROADMAP.md`.
3. `design/brandbook-v2/BRANDBOOK_V2.md` e `nexo-tokens.json`; `assets/ASSETS_MANIFESTO.md`; assets binários existentes e **PNG do notebook enviado pelo usuário**.
4. `homepage/dist/index.html`, `styles.css`, `app.js`; `homepage/README.md`.
5. `alpha-snapshot/backend/`, `workspace-v2/`, `tests/`; `produto/FUNCIONALIDADES_E_REGRAS.md`.
6. Issues #2, #3, #4, #5, #6 e #7; CI e evidências em `evidencias/capturas/manifest.json`.

**Atenção:** `handoff/CONTINUAR_NO_WORK.md` e `alpha-snapshot/docs/ARCHITECTURE.md` contêm partes históricas e referências de identidade/estrutura possivelmente superadas (ex.: frontend antigo). Não tratá-los como fonte de verdade se contradisserem código ativo, brandbook e novas decisões.

## 3. Roadmap executável e dependências

| Fase | Prioridade | Entrega verificável | Gate de aceite |
|---|---|---|---|
| **F0 — Baseline auditado** | P0 inicial | HEAD/PR/arquivos mapeados; testes existentes; capturas atuais; divergências registradas; branch de tarefa isolada | Relatório de baseline e CI verificado, **sem** alteração do layout |
| **F1 — Home fiel ao notebook aprovado** | P1 de produto/marketing, primeiro item visual | Validar o PNG de referência; identificar asset autorizado para notebook; preservar os textos A/B, paleta, tipografia e seções; implementar só a integração visual aprovada | Comparativo exato antes/depois desktop 1440×960 e mobile 390×844; nenhuma foto aleatória, visual sem overflow e aprovação do proprietário |
| **F2 — Segurança e tenancy** | P0 bloqueante de dados reais | Auditar sessões, CSRF, revogação/expiração, tokens, autorização por tenant/perfil, vazamento NET, logs, LGPD e erros | Testes de ataque e acesso cruzado; nenhuma informação de outra empresa; sem dados reais em testes |
| **F3 — Modelo financeiro tipado** | **P0 issue #4** | Quarto × diárias/room nights, ocupação, café, taxas, fee/markup e totais com unidade semântica; migração aditiva | Ex.: 105 × 3 × R$612 = R$192.780 auditável; item/quote/proposta conciliam; pública sem NET |
| **F4 — Briefing por serviço** | P0 issue #2 | Wizard aéreo/hospedagem/salas-A&B/transfers, rascunho, anexos versionados, V1→V2, validações por campo | Testes de paridade das regras, histórico imutável, acesso por perfil, mobile |
| **F5 — Sourcing/RFQs** | P0 issue #2 | Versão fixada no lote, fornecedores, resposta estruturada, expiração/revogação, idempotência, fluxo de envio explícito | Pedido→resposta com ausência de duplicação, concorrência e tokens expirados; não afirmar e-mail enviado se não foi |
| **F6 — Cotação, proposta e decisão** | P0 issue #2/#4 | Comparativo de escopo equivalente; editor de proposta, snapshots V1/V2, aprovação/rejeição; NET privado | Cálculo reconciliado e imutável após publicação; público não acessa margem nem concorrentes |
| **F7 — Workspace robusto** | P1 issue #5 | Modularizar `workspace-v2/app.js`, estados vazios/carregamento/erro, fila acionável, teclado/zoom e responsividade | Sem regressão de fluxo, sem CSS legado, WCAG 2.2 AA revisado |
| **F8 — Redigitação e integrações** | Discovery P1 issue #6; implementação condicionada | Campo canônico do evento, mapa campo→sistema, export auditável e seleção da primeira integração | Integração só após contrato/API/segurança aprovados; sem prometer sincronização inexistente |
| **F9 — Homologação e lançamento** | P0 QA + P1 issue #3 | E2E, privacidade/retenção, destino de leads, HTTPS, backups/restores, domínio/marca e SEO | Go-live deliberado e assinado, ambiente de produção seguro, rollback ensaiado |
| **F10 — Evolução** | P2 | Importação Excel, portal fornecedor, notificações avançadas, dashboards e financeiro realizado | Dados reais, benefícios medidos e aprovações de escopo |

**Caminho crítico:** F0 → F2 → F3/F4 → F5 → F6 → F9. F1 é uma trilha visual independente e **não autoriza lançamento**. F7 e discovery F8 podem avançar em paralelo **somente em arquivos/branches isolados**.

## 4. Execução segura — passos para Work

1. Abrir **Work mode**, conectar o GitHub autorizado e disponibilizar o **PNG de referência do notebook** e este handoff. Não confundir PNG conceitual com uma tela real da API.
2. Inspecionar a PR #1, HEAD da branch-base, CI e os arquivos atuais. Produzir `governanca/BASELINE_WORK_YYYY-MM-DD.md` antes de fazer mudanças.
3. Criar branch isolada da branch-base atual (ex.: `work/home-notebook-fidelidade`). Não fazer commit diretamente em `main`; não editar `Zuma-Lab/nexo`.
4. No primeiro ciclo, executar **somente F0 e F1**. Não migrar framework, não refazer workspace, não adicionar seções, ícones, logos fictícios ou números de marketing.
5. Conferir a arte do notebook e separar visual de produto fictício/ilustrativo de screenshot funcional; obter asset individual autorizado e rotulagem correta. Se não houver como obter o asset fiel, **não substituir** por imagem arbitrária: registrar o bloqueio e entregar a copy/QA que puder.
6. Implementar diff mínimo, preservar `styles.css`/tokens salvo necessidade visual **especificamente autorizada**, e registrar por arquivo o motivo da modificação.
7. Executar testes, screenshots reais desktop/mobile e comparar com o PNG aprovado; não usar ImageGen para falsificar evidência de implementação.
8. Atualizar BR, ADR, CHG, roadmap e README somente quanto a mudanças de fato feitas. Criar PR draft **contra a branch-base** e apontar arquivos, resultados e bloqueios.
9. Enviar para revisão do proprietário e para Claude Code na branch **somente leitura**. Não fazer merge/deploy automaticamente.

### Comandos de baseline

```bash
git clone https://github.com/Zuma-Lab/nexoalpha.git
cd nexoalpha
git fetch origin
git switch -c work/home-notebook-fidelidade origin/feat/homepage-produto-revisao-claude-20261123
git status --short
git rev-parse HEAD
python -m pip install -r alpha-snapshot/requirements.txt pytest httpx
cd alpha-snapshot
python -m pytest -q
cd ..
python -m compileall -q alpha-snapshot/backend
python scripts/validate_governance.py
node --check homepage/dist/app.js
node --check alpha-snapshot/workspace-v2/app.js
```

**Execução local de desenvolvimento:** em shell Unix, `cd alpha-snapshot && NEXO_DEMO=1 uvicorn backend.main:app --host 127.0.0.1 --port 8000`; em PowerShell, `$env:NEXO_DEMO='1'; python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000`. `http://127.0.0.1:8000/` é a home; `/app` é o workspace. Somente em localhost/banco sintético; **não usar NEXO_DEMO=1 em produção**.

Para evidências reais, instalar Playwright e Chromium e executar `python scripts/capture_screens.py` **da raiz do repo**. A documentação do CI contém dependências. Usar banco efêmero no script, nunca banco real.

## 5. Claude Code — papel e fluxo

- Claude deve ler primeiro `CLAUDE.md`, o handoff e as regras de governança.
- **Revisar o PR do Work**: fidelidade ao notebook, conteúdo de verdade, acessibilidade, responsividade e exclusão de novos elementos não solicitados. Entregar relatório com P0/P1/P2 e diffs sugeridos.
- **Não editar a branch do Work durante a revisão**. Se solicitado a corrigir, criar branch separada `claude/review-home-notebook`, baseada na branch de revisão do Work, e abrir outro PR draft.
- Após aceite visual, Claude pode assumir tarefa independente (sugestão: auditoria dos modelos/serviços financeiros, issue #4) em `claude/financial-room-nights`, com tests antes de refatorar.
- Não trocar stack para React/Next por preferência pessoal; não renomear marca; não criar clientes, métricas, API ou integrações fictícias.
- Registrar tudo em BR/ADR/CHG, mostrar testes executados e falhas sem declarar sucesso onde não houve execução.

## 6. Critérios de aceite transversais

**Produto:** fluxo briefing→RFQ→cotação→proposta→decisão rastreável; V1/V2 preservadas; valores iguais entre orçamento e proposta.  
**Segurança:** segregação de empresa/perfil, NET não público, token expira/revoga, CSRF/sessão, ausência de PII real em exemplo/print.  
**Design:** brandbook 2.1, notebook fiel ao rascunho, sem redesign incidental, mobile 390×844, desktop 1440×960, sem overflow.  
**Código:** evitar módulos monolíticos novos; testes de regressão e E2E, migrations aditivas e rollback, sem mexer no legado.  
**Marketing:** promessas apenas sobre o que existe, exemplos fictícios marcados, nenhuma estatística ou logo de clientes inventados.  
**Governança:** cada etapa com PR, diff, screenshots reais, changelog e decisão aprovada/proposta separadas.

## 7. Prompt curto para iniciar no Work

> Atue como engenheiro fullstack sênior e diretor de produto do NEXO Alpha. Trabalhe exclusivamente em `Zuma-Lab/nexoalpha` a partir da branch `feat/homepage-produto-revisao-claude-20261123` e leia `CLAUDE.md`, este handoff e o brandbook 2.1. **Não altere o legado `Zuma-Lab/nexo`, nem faça merge/deploy.** Comece auditando o estado real, registrando baseline e verificando CI. Depois execute exclusivamente a etapa F1: integrar de modo fiel à homepage a composição visual **com notebook** do PNG que anexei, mantendo a copy A/B, todas as cores, tipografia, seções, componentes e CTAs aprovados. A arte é mockup, não tela funcional. Se o notebook não existir como asset isolado, identifique a necessidade e não substitua por fotografia/imagem arbitrária. Gere screenshots reais desktop/mobile, compare antes/depois, execute testes e abra PR draft da branch de trabalho para a branch-base. Registre alterações, limitações e critérios de aceite. Só após revisão passe a F2/F3, uma tarefa por vez.

## 8. Prompt curto para Claude Code

> Leia `CLAUDE.md`, `handoff/ROADMAP_WORK_CLAUDE_2026-11-25.md` e a PR de implementação do Work. Sua primeira tarefa é **revisar**, não redesenhar: fidelidade à composição aprovada com notebook, copy A/B, paleta/Inter, UI responsiva, acessibilidade, sem afirmações fictícias. Confronte código com evidências; aponte bugs com arquivo/linha, prioridade e correção mínima. Não edite a branch do Work nem `Zuma-Lab/nexo`. Para implementações autorizadas, use branch separada, testes, screenshots reais e PR draft, sem merge/deploy automático.

## 9. Dependências abertas

- A arte conceitual com notebook precisa ser anexada ao Work/Claude pelo usuário no handoff; não consta atualmente como notebook isolado na pasta `homepage/dist/assets/`.
- As regras das issues #2 e #4 são P0 antes de piloto comercial real. Migrations SQLite precisam estratégia de backup e testes; PostgreSQL é proposta de evolução, não decisão de migração já homologada.
- LGPD, política de privacidade/retenção, identidade/domínio final, e-mail/CRM de leads, TLS e consentimento permanecem pendentes antes de produção.
- `nexo.com.br` não deve ser assumido. Skills em `skills/portateis/` são referências; não autorização para criar um novo layout.

**Fonte de verdade da execução:** GitHub branch+PR+CI+tests+screenshots reais; não a descrição de um mockup ou um documento histórico.
