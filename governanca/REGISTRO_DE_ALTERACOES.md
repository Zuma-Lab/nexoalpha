# Registro de alterações — trilha de auditoria de projeto

**Formato:** ID | Data local | Mudança | Razão | Arquivos | Estado | Evidência/validação.  
**Fuso:** America/Sao_Paulo. Commits automáticos podem aparecer em 2026-11-24 UTC embora os registros abaixo sejam de 2026-11-23 no fuso local.  
**Primeira revisão estruturada:** 2026-11-23. Não apagar entradas; substituir por nova entrada vinculada.

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
ID: CHG-015 (sequencial)
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
