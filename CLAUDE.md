# CLAUDE.md — NEXO Alpha | contrato de execução

**Atualizado em 2026-11-25.** Este arquivo orienta Claude Code e outros agentes. Leia o código e a governança antes de atuar. As regras confirmadas pelo proprietário prevalecem sobre sugestões genéricas de IA, frameworks ou skills.

## Repositório e isolamento (obrigatórios)

- Repositório de trabalho: `Zuma-Lab/nexoalpha`. Branch-base de revisão: `feat/homepage-produto-revisao-claude-20261123` (PR #1 em **draft**).
- Repositório `Zuma-Lab/nexo`: **somente leitura** para levantar regras de negócio. Nunca modificar, abrir PR nele, copiar seu layout/CSS ou alterar o banco original.
- Não realizar merge, deploy, publicação de leads, mudanças de domínio ou migrações destrutivas sem aprovação expressa.
- Trabalhar em **uma branch nova por tarefa**, a partir da branch-base atual, usando PR draft e commits pequenos. Work e Claude não devem editar simultaneamente a mesma branch/arquivos. Antes de começar, verificar `git status`, commit HEAD e diferenças remotas.
- Distinguir requisitos **confirmados**, **propostos** e **pendentes**. Não assumir que uma screenshot, um mockup de imagem ou uma ideia em documentação já foi implementada.

## Prioridade de leitura

1. `README.md`, `governanca/GUIA_EDITORIAL_E_APROVACAO_HOMEPAGE.md`, `governanca/PADROES_E_REGRAS.md`.
2. `governanca/DECISOES_ARQUITETURAIS.md`, `governanca/REGISTRO_DE_ALTERACOES.md`, `governanca/ROADMAP.md`, `governanca/PENDENCIAS_E_RISCOS.md`.
3. `design/brandbook-v2/BRANDBOOK_V2.md` e `design/brandbook-v2/nexo-tokens.json`.
4. `homepage/dist/`, `assets/`, `design/HOMEPAGE_DETALHADA.md`.
5. `alpha-snapshot/backend/`, `alpha-snapshot/workspace-v2/`, `alpha-snapshot/tests/`, `produto/FUNCIONALIDADES_E_REGRAS.md`.
6. Issues #2 a #7 e evidências `evidencias/capturas/manifest.json`. `alpha-snapshot/frontend/` é **histórico**, não a UI ativa.
7. Skills portáteis em `skills/portateis/`: consulte antes de usá-las; não deixar que alterem a marca ou o escopo aprovado.

**Atenção a documentos legados:** `handoff/CONTINUAR_NO_WORK.md` e partes de `alpha-snapshot/docs/ARCHITECTURE.md` são registros históricos e podem estar desatualizados sobre o frontend ativo, cores e arquivos. Em conflito, código atual + brandbook 2.1 + governança recente + aprovação do proprietário têm precedência. Registrar inconsistências, não corrigi-las silenciosamente.

## Identidade e homepage — REGRA CRÍTICA

- Identidade aprovada: grafite `#111315`, laranja `#FF850D`, creme `#F3EFE9`, tipografia Inter e símbolo angular provisório; não mudar cores, logos, tipografia, grid ou estrutura quando o pedido disser **apenas copy**.
- Copy confirmada no HTML:
  - Hero: **“O evento é um só. A informação não deveria estar em tantos lugares.”**
  - Primeira rolagem: **“Sua equipe precisa conduzir eventos. Não reconstruir informações.”**
  - Texto de apoio curto; sem repetir a mesma dor em todas as seções.
- **Visual com notebook:** o proprietário gostou do *rascunho anterior com notebook e sistema em destaque*. Esse notebook **NÃO está implementado como asset individual no HTML atual**. A homepage atual ainda possui `.hero-note` e `.case-board` e não tem `.hero-visual` ou `.briefing-visual`. NÃO afirmar que o notebook foi restaurado no site, nem substituir a arte aprovada por fotografias aleatórias ou screenshots planos.
- Antes de integrar o notebook, o Work/Claude deve receber **o PNG de referência aprovado pelo proprietário**, identificar o asset licenciado/fiel e apresentar diff visual antes/depois. Somente implementar após escopo de imagem/layout aprovado.
- Não usar marca de clientes, depoimentos, estatísticas, automações, integrações ou prazos inventados. Não usar mockup como screenshot funcional nem chamar exemplos fictícios de reais.
- Qualquer alteração visual requer validação em **1440×960** e **390×844**, comparação antes/depois, sem overflow e com contraste/foco/teclado. Alteração **copy-only** não pode tocar `styles.css` nem tokens.

## Stack e limites de produto

- Backend ativo: **FastAPI + SQLite de desenvolvimento**, localizado em `alpha-snapshot/backend/`.
- Homepage: `homepage/dist/index.html`, `styles.css`, `app.js`; servida em `/`.
- Workspace operacional ativo: `alpha-snapshot/workspace-v2/` em `/app`; JavaScript/HTML/CSS atuais, sem autorização para migrar automaticamente para Next/React.
- `alpha-snapshot/frontend/` preservado como histórico. Não ressuscitar layout legado.
- Briefings V1/V2 imutáveis, drafts por usuário, RFQ ligada à versão, fornecedor restrito, custos NET/fees internos, proposta versionada e permissão por tenant são invariantes.
- **Ainda não pronto para produção:** envio real de e-mail, integrações ERP/CRM, importação Excel, anexos, homologação de segurança/LGPD, cálculo de unidades de hospedagem completo, editor avançado de propostas.
- Não aplicar ferramentas externas ou “skills” como autorização para refazer o design.

## Primeiros trabalhos recomendados

1. **Auditoria e congelamento de baseline:** código, PR #1, CI, screenshots, divergências de documentação, nenhum merge.
2. **Homepage visual aprovada:** usando o PNG do notebook, implementar **somente após aprovação da alteração de layout**; manter copy A/B, cores e identidade. Issue #7.
3. **P0 financeiro:** itens tipados com quartos × diárias, room nights, café, impostos, fee e venda; migração **aditiva**, cálculo determinístico e tests. Issue #4.
4. **P0 briefing/RFQ/propostas:** concluir regras por serviço, anexos, comunicações e políticas sem vazamento entre tenants. Issue #2.
5. **P1 modularização/A11y:** dividir `workspace-v2/app.js` com testes e preservar comportamento. Issue #5.
6. **P1 dados/integrações:** modelagem e discovery antes de prometer sincronização externa. Issue #6.
7. **Pré-go-live:** testes E2E multiempresa, LGPD, identidade/domínio, políticas de privacidade, backup/restore, HTTPS, observabilidade. Issue #3.

## Gates de qualidade

Executar de `alpha-snapshot/`:
```bash
python -m pip install -r requirements.txt pytest httpx
python -m pytest -q
```
Da raiz:
```bash
python -m compileall -q alpha-snapshot/backend
python scripts/validate_governance.py
node --check homepage/dist/app.js
node --check alpha-snapshot/workspace-v2/app.js
```
Para screenshots reais, configurar Playwright/Chromium e executar `python scripts/capture_screens.py`; usa uma API e banco **efêmeros** de teste. Também verificar `.github/workflows/alpha-ci.yml` e `alpha-evidence.yml`. CI verde não equivale a homologação de segurança ou visual.

## Contrato de entrega por tarefa

Entregar sempre: **(1) escopo aprovado**, **(2) diff por arquivo**, **(3) testes executados e resultado**, **(4) capturas reais e comparação**, **(5) riscos/limites**, **(6) BR/ADR/CHG e data**, **(7) PR draft e próximo gate**. Não declarar concluído o que for somente rascunho. Não reescrever histórico sem aviso.

**Handoff completo:** consulte `handoff/ROADMAP_WORK_CLAUDE_2026-11-25.md` (quando sincronizado na branch) e as issues do GitHub.
