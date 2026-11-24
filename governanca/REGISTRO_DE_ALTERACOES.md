# Registro de alterações — trilha de auditoria de projeto

**Formato:** ID | Data local | Mudança | Razão | Arquivos | Estado | Evidência/validação.  
**Fuso:** America/Sao_Paulo. Commits automáticos podem aparecer em 2026-11-24 UTC embora os registros abaixo sejam de 2026-11-23 no fuso local.  
**Primeira revisão estruturada:** 2026-11-23. **Última revisão técnica:** 2026-11-24. Não apagar entradas; substituir por nova entrada vinculada.

## Reformulação crítica — 2026-11-24 (America/Sao_Paulo)

| ID | Data | Mudança e justificativa | Arquivos / referência | Estado e evidência |
|---|---|---|---|---|
| CHG-020 | 2026-11-24 | Workspace com estilo corporativo genérico foi mantido como histórico; criada interface independente com superfícies neutras, navegação escura e componentes operacionais. | `alpha-snapshot/workspace-v2/index.html`, `styles.css` | Implementado na PR #1 |
| CHG-021 | 2026-11-24 | Fluxos de trabalho ligados à API: fila, projetos, briefing guiado, fornecedores, RFQs por link, itens financeiros, propostas, tarefas e acesso público. | `workspace-v2/app.js` | Implementado em branch; QA funcional |
| CHG-022 | 2026-11-24 | `/app` passou a servir interface V2; snapshot anterior não é carregado, porém arquivos permanecem preservados. | `backend/main.py` | Implementado; smoke CI |
| CHG-023 | 2026-11-24 | Homepage deixou a direção SaaS genérica A e adotou narrativa editorial B, com alteração de briefing, impactos, raciocínio financeiro e matriz de acessos. | `homepage/dist/index.html`, `styles.css` | Implementado em branch; revisão visual |
| CHG-024 | 2026-11-24 | Sistema de evidência ampliado para autenticar no Alpha e capturar tela real de fila, projeto, orçamento, wizard e versões em desktop/mobile. | `scripts/capture_screens.py` | Pipeline E2E em revisão |
| CHG-025 | 2026-11-24 | Brandbook e tokens elevados a v2.1 para regular interface editorial e workspace operacional. | `design/brandbook-v2/` | Fonte alterada; PDF regenerado no pipeline |
| CHG-026 | 2026-11-24 | Verificações CI migradas para arquivos V2 e smoke de rotas ajustado; problemas no runner foram corrigidos. | `.github/workflows/alpha-ci.yml`, `tests/test_workflow.py` | CI Python/JS verde em execução recente; screenshot E2E ainda em validação |

| CHG-027 | 2026-11-24 | Rascunho persistente por usuário/projeto, protegido por CSRF, recuperável e limpo na publicação. | `db.py`, `main.py`, `workspace-v2/app.js`, testes | API e UI implementadas, CI automatizada |
| CHG-028 | 2026-11-24 | Editor básico de termos e apresentação comercial da proposta, gravados no snapshot versionado e mostrados em página pública sem custos internos. | `main.py`, `workspace-v2/app.js`, testes | Implementado e coberto por testes |
| CHG-029 | 2026-11-24 | Fluxo de wizard aprimorado ao retornar/avançar etapas, preservando edições locais. | `workspace-v2/app.js` | Implementado; teste visual pendente |

## Atualização técnica de 2026-11-24 (America/Sao_Paulo)

| ID | Data | Mudança e justificativa | Arquivos / referência | Status e evidência |
|---|---|---|---|---|
| CHG-015 | 2026-11-24 | Brandbook v2 passou a ter tokens JSON, manual Markdown e gerador PDF determinístico; v1 preservada. | `design/brandbook-v2/` | **PDF de 8 páginas** gerado e salvo na branch; GitHub Actions #45317774083 |
| CHG-016 | 2026-11-24 | Sete telas da homepage capturadas com Chrome/Playwright e banco de dados efêmero; manifesto registra commit e viewport. | `scripts/capture_screens.py`, `evidencias/capturas/` | **7 PNGs** e manifesto no GitHub; desktop 1440 e mobile 390, sem overflow externo |
| CHG-017 | 2026-11-24 | Introduzida validação obrigatória de IDs, datas, roadmap M0–M9 e tokens v2 na CI. | `scripts/validate_governance.py`, `.github/workflows/alpha-ci.yml` | Implementado; CI aprovada |
| CHG-018 | 2026-11-24 | Pipeline visual passou a aproveitar Chrome do runner; evita instalação desnecessária de navegador. | `.github/workflows/alpha-evidence.yml`, `scripts/capture_screens.py` | Validado no GitHub Actions #45317774083 |
| CHG-019 | 2026-11-24 | PDF e capturas gerados e commitados automaticamente na branch de revisão. Corrigido token `light_muted` no gerador. | `design/brandbook-v2/build_brandbook.py`, `evidencias/capturas/` | Validado em execução verde, [manifesto](../evidencias/capturas/manifest.json) |

## Alterações de 2026-11-23

| ID | Data | Mudança e justificativa | Arquivos / referência | Status e evidência |
|---|---|---|---|---|
| CHG-001 | 2026-11-23 | Escolhida direção A: hero baseado em briefing V1/V2, sem foto artificial, para mostrar o produto em vez de imagem genérica. | `homepage/dist/index.html`, `styles.css`, `app.js` | Implementado na PR #1; QA visual a complementar |
| CHG-002 | 2026-11-23 | Formulário de demonstração e login no lugar de CTA sem ação. Inputs fazem chamadas à API, sem falso sucesso. | `homepage/dist/`, `alpha-snapshot/backend/main.py` | Implementado na PR #1; entrega por e-mail/CRM pendente |
| CHG-003 | 2026-11-23 | Migração de Bearer em `sessionStorage` para cookie HttpOnly, SameSite Strict e token CSRF. Reduz exposição a XSS do token. | `backend/main.py`, `db.py`, `frontend/app.js` | Implementado/testado, ainda não homologado |
| CHG-004 | 2026-11-23 | Limitação de login por identidade/origem, expiração de tokens públicos e revogação. | `alpha-snapshot/backend/` | Implementado/testado na PR #1 |
| CHG-005 | 2026-11-23 | Idempotência do registro de envio de RFQ e ampliação de testes de V1/V2 e arredondamento. | `backend/main.py`, `tests/` | Implementado; CI com 39 testes antes desta rodada |
| CHG-006 | 2026-11-23 | Sanitização da API pública para não revelar custos NET, fees e tributos internos ao cliente. | `alpha-snapshot/backend/main.py`, `tests/test_workflow.py` | Implementado/testado |
| CHG-007 | 2026-11-23 | Regras JavaScript de briefing do legado reinterpretadas em Python, sem importar telas antigas. | `backend/briefing_rules.py`, `tests/test_briefing_rules.py` | Implementado/testado em casos selecionados; editor pendente |
| CHG-008 | 2026-11-23 | Reorganização do README separando homepage, backend recuperado e documentos históricos; caminhos pessoais retirados. | `README.md`, `homepage/README.md`, `alpha-snapshot/README.md`, `design/`, `skills/` | Implementado |
| CHG-009 | 2026-11-23 | Retirada da transcrição pessoal da árvore atual; histórico antigo do Git continua acessível. | `historico/MENSAGENS_DO_USUARIO.md`, `.gitignore` | Implementado apenas na branch; reescrita histórica requer aprovação |
| CHG-010 | 2026-11-23 | Aprovada a organização de uma fonte única com regras, decisões, alterações e roadmap, para retomada em outro computador. | `governanca/` | Documentado; revisar a cada PR |
| CHG-011 | 2026-11-23 | Brandbook v2 separado do v1, com nome/domínio provisórios, tokens, identidade, UX, acessibilidade e padrões de conteúdo. | `design/brandbook-v2/` | Fonte em elaboração; PDF gerado por pipeline |
| CHG-012 | 2026-11-23 | Capturas passam a vir do navegador executando a branch, com metadados (viewport/commit), sem gerar imagens fictícias das telas. | `evidencias/`, `scripts/capture_screens.py`, GitHub Actions | Pipeline em elaboração |
| CHG-013 | 2026-11-23 | Nome final não será NEXO por pressuposição; possíveis Benexo, Nexobe, Bnexo. Não adotar `nexo.com.br`. | `governanca/DECISOES_ARQUITETURAIS.md`, brandbook v2 | Em aberto por decisão do proprietário |
| CHG-014 | 2026-11-23 | Roadmap com começo, meio e fim, gates, riscos e critérios verificáveis. | `governanca/ROADMAP.md`, `PENDENCIAS_E_RISCOS.md` | Documentado |

## Como registrar a próxima alteração

```text
ID: CHG-030 (sequencial)
Data local: AAAA-MM-DD (America/Sao_Paulo)
Autor/PR:
Motivo/decisão:
Regras BR/ADR afetadas:
Arquivos:
Antes -> depois:
Impacto em segurança, UX, dados e migração:
Testes/prints:
Estado e pendências:
```

**Observação:** capturas do site publicado anteriormente em prévia privada não representam as alterações da branch. Nova evidência precisa ser gerada a partir do código do PR.
