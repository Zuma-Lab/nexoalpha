# Registro de alterações — trilha de auditoria de projeto

**Formato:** ID | Data local | Mudança | Razão | Arquivos | Estado | Evidência/validação.  
**Fuso:** America/Sao_Paulo. Commits automáticos podem aparecer em 2026-11-24 UTC embora os registros abaixo sejam de 2026-11-23 no fuso local.  
**Primeira revisão estruturada:** 2026-11-23. **Última revisão técnica:** 2026-11-24. Não apagar entradas; substituir por nova entrada vinculada.

## Consolidação operacional do consultor — 2026-11-25

| ID | Data | Mudança e justificativa | Arquivos / referência | Estado e evidência |
|---|---|---|---|---|
| CHG-042 | 2026-11-25 | Auditoria profunda de `queue`, permissões, RFQ, proposta, financeiro e versionamento identificou 12 lacunas operacionais. Criada especificação com jobs-to-be-done, IA das telas, gates e riscos, sem alterar identidade visual. | `design/CONSULTOR_WORKSPACE_ESPECIFICACAO_2026-11-25.md` | Design documentado na branch isolada; aprovação pendente |
| CHG-043 | 2026-11-25 | Implementado MVP de fila orientada a ações factuais por `company_id`, novo endpoint interno, navegação para etapa correta e **CTA contextual também na visão do projeto**, com testes de perfis, alterações V1/V2 e isolamento de tenant. Sem alterar homepage, tokens, cálculos ou schema. | `backend/consultant_queue.py`, `backend/main.py`, `workspace-v2/app.js`, `tests/test_workflow.py` | Implementado em branch isolada; CI e avaliação manual necessárias |
| CHG-044 | 2026-11-25 | Reemissão de link de RFQ individual no histórico do projeto, com substituição do hash e auditoria. | backend/main.py, workspace-v2/app.js, tests/test_workflow.py | Implementado para revisão. Retomada de lotes e propostas segue na issue #8. |

## Concepção das telas seguintes — 2026-11-25

| ID | Data | Mudança e justificativa | Arquivos / referência | Estado e evidência |
|---|---|---|---|---|
| CHG-041 | 2026-11-25 | Inspecionadas referências exploratórias de briefing (3/5 passos, UI escura) e capturas do workspace real (4 passos, superfícies claras). Criado mapa de seis telas, composição e gates sem mexer na implementação. | `design/PROPOSTA_PROXIMAS_TELAS_2026-11-25.md` | **Proposta, aguardando validação visual**; nenhum HTML/CSS alterado |

## Handoff de implementação para Work e Claude — 2026-11-25

| ID | Data | Mudança e justificativa | Arquivos / referência | Estado e evidência |
|---|---|---|---|---|
| CHG-040 | 2026-11-25 | Preparado handoff técnico executável com roadmap F0–F10, contrato automático para Claude Code, comandos de teste e separação de branches Work/Claude. Distinção registrada: copy A/B está codificada; **notebook aprovado é referência conceitual e não asset implementado**. Nenhum merge, deploy ou edição de layout realizado nesta tarefa. | `CLAUDE.md`, `handoff/ROADMAP_WORK_CLAUDE_2026-11-25.md`, `README.md`, `governanca/README.md` | **Documentação implementada** na PR #1; tarefas funcionais continuam pendentes |

## Correção editorial sem redesenho — 2026-11-25

| ID | Data | Mudança e justificativa | Arquivos / referência | Estado e evidência |
|---|---|---|---|---|
| CHG-039 | 2026-11-25 | Proprietário reafirmou preferência pelo **rascunho anterior com notebook**, criticando a troca das imagens e disposição. Restaurados HTML estrutural e CSS da homepage anteriores à última intervenção, preservando apenas a copy A/B mais concisa. O notebook aparece no **rascunho visual**, mas não existia como asset de notebook individual no HTML anterior; não alegar que foi incorporado ao site. | `homepage/dist/index.html`, `styles.css`, `tests/test_workflow.py`, `scripts/capture_screens.py` | Copy-only implementado; composição de notebook permanece conceito à espera de integração fiel |

## Implementação editorial e imagens originais — 2026-11-25

| ID | Data | Mudança e justificativa | Arquivos / referência | Estado e evidência |
|---|---|---|---|---|
| CHG-037 | 2026-11-25 | Usuário autorizou refinar copy e distribuição de imagens. Hero passou a título institucional A e texto enxuto; primeira rolagem recebe título B e imagem 03 do briefing. Imagem do sistema no hero; fotografia 01 omitida para evitar excesso. Sem novos tokens ou paleta. | `homepage/dist/index.html`, `styles.css`, `backend/main.py` | Implementado na PR #1; QA visual pendente |
| CHG-038 | 2026-11-25 | Testes e screenshots atualizados: arquivos existentes `/assets/briefing-*.webp` acessíveis, copy A/B e recortes do hero/briefing desktop e mobile. | `tests/test_workflow.py`, `scripts/capture_screens.py` | CI em execução |

## Guia editorial e prevenção de regressão de escopo — 2026-11-24

| ID | Data | Mudança e justificativa | Arquivos / referência | Estado e evidência |
|---|---|---|---|---|
| CHG-036 | 2026-11-24 | Após avaliação crítica dos rascunhos, registrado **excesso de informação, títulos concorrentes e densidade mobile**. Criado guia de editoria e processo de aprovação: preservar identidade atual; copy-only não autoriza CSS/layout; recomendações de redução e imagens ficam como proposta, não implementação. | `governanca/GUIA_EDITORIAL_E_APROVACAO_HOMEPAGE.md`, BR-051..056, ADR-023/024, checklist de PR | Documento registrado na PR #1; **homepage visualmente inalterada** |

## Correção de escopo — 2026-11-24

| ID | Data | Mudança e justificativa | Arquivos / referência | Estado e evidência |
|---|---|---|---|---|
| CHG-035 | 2026-11-24 | **Rollback por escopo:** proprietário aprovou ajuste de mensagem sobre dores, não nova seção nem mudança de cor/layout. Retirado bloco `#retrabalho`, CSS e capturas correspondentes. Mantida apenas nova copy no hero e composição anterior da direção B. Tokens e manual retornaram à versão 2.1. | `homepage/dist/`, `design/brandbook-v2/`, `scripts/capture_screens.py`, `evidencias/capturas/` | Revertido; nova validação CI |
 
## Ajuste de mensagem da homepage — 2026-11-24

| ID | Data | Mudança e justificativa | Arquivos / referência | Estado e evidência |
|---|---|---|---|---|
| CHG-030 | 2026-11-24 | Pesquisadas dores de fragmentação em operações de eventos, cruzando relatos do projeto com Forrester, ICE, Cvent e UX B2B; dados de quatro sistemas tratados como cenário, não estatística. | `governanca/PESQUISA_DORES_E_MENSAGEM_HOME_2026-11-24.md` | Pesquisa registrada com fontes e ressalvas |
| CHG-031 | 2026-11-24 | Hero da homepage passou a reconhecer e-mails, planilhas e cadastros repetidos, preservando o conceito de versionamento V1/V2. | `homepage/dist/index.html` | Código implementado, revisão em andamento |
| CHG-032 | 2026-11-24 | Nova seção no primeiro scroll apresenta fontes divergentes de um evento fictício (180/210 pessoas), efeito do retrabalho e limites de integração. | `homepage/dist/index.html`, `styles.css` | Implementado experimentalmente, depois **revertido a pedido do proprietário** |
| CHG-034 | 2026-11-24 | Revisão visual real desktop/mobile confirmou a leitura do fluxo e identificou necessidade de aumentar o texto de aviso de integrações; corrigido para 12px desktop e 11px mobile. | `homepage/dist/styles.css`, screenshots no GitHub | Alteração visual revertida no mesmo dia |
| CHG-033 | 2026-11-24 | Teste automatizado e captura Chromium desktop/mobile adicionados para validar dor, disclaimer e responsividade. | `tests/test_workflow.py`, `scripts/capture_screens.py` | Capturas da seção experimental descontinuadas; smoke da mensagem mantido |

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
ID: CHG-044 (sequencial)
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
