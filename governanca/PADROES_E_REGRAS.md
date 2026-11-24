# Padrões e regras do produto — catálogo normativo

**Versão:** 1.1 · **Data de criação:** 2026-11-23 · **Última revisão:** 2026-11-24 · **Timezone:** America/Sao_Paulo.  
**Nome de trabalho:** NEXO Alpha. **Marca/domínio finais: em aberto.**

> **Legenda:** Decidido = regra de produto; Implementado = código existe no PR #1; Validado = teste de CI com evidência; Pendente = trabalho futuro. "Implementado" não significa homologado nem em produção.

## Identidade e apresentação

| ID | Data | Regra | Estado |
|---|---|---|---|
| BR-001 | 2026-11-23 | Homepage centrada em operação e produto (briefing V1/V2 no hero), não em fotografia artificial. | **Substituído por BR-036 (2026-11-24)** |
| BR-002 | 2026-11-23 | Grafite `#111315`, canvas `#0B0D0F`, off-white `#F3EFE9`, laranja `#FF850D`; sempre consultar tokens v2 antes de criar componentes. | Decidido/implementado na home |
| BR-003 | 2026-11-23 | Inter 400/500/600/700 é família primária; fallback system-ui/Arial; empacotar fonte localmente antes de go-live. | Proposto; fonte externa atual |
| BR-004 | 2026-11-23 | Contraste AA: ≥4,5:1 texto normal e ≥3:1 texto grande e controles relevantes. Labels editoriais secundários podem ser menores quando não são o único caminho para informação; tabelas, controles e conteúdo operacional devem ser legíveis e testados a zoom 200%. | Revisado 2026-11-24; QA pendente |
| BR-005 | 2026-11-23 | Evitar componentes genéricos ou imitação das telas antigas; priorizar legibilidade, hierarquia, foco, layout responsivo e estados explícitos. | Decidido |
| BR-006 | 2026-11-23 | Toda interface demonstrativa deve indicar dados fictícios; nunca simular clientes ou operações reais. | Implementado na home |
| BR-007 | 2026-11-23 | Tela de produto real substitui mockup ilustrativo somente após existir e ser homologada. | Pendente |
| BR-008 | 2026-11-23 | OG/canonical apenas no domínio final; nunca apontar a preview privada. Nome, domínio e logotipo final exigem decisão. | Parcial; domínio pendente |
| BR-009 | 2026-11-23 | Fotografias reais, autorizadas/licenciadas quando fizerem sentido; hero atual usa interface, sem imagens editoriais artificiais. | Decidido |

## Segurança, dados e conformidade

| ID | Data | Regra | Estado |
|---|---|---|---|
| BR-010 | 2026-11-23 | `Zuma-Lab/nexo` é legado de leitura: importar somente especificação funcional e casos de teste, reescritos e validados em Alpha. | Decidido; briefing parcialmente portado |
| BR-011 | 2026-11-23 | Sessões de 12 h em cookie `HttpOnly`, `SameSite=Strict`; `Secure` obrigatório via HTTPS; sessão nunca em `sessionStorage`. | Implementado na branch |
| BR-012 | 2026-11-23 | CSRF por sessão obrigatório em operações autenticadas de alteração; autorização por empresa e perfil sempre no servidor. | Implementado/testado |
| BR-013 | 2026-11-23 | Login limitado por identidade e origem: 5 falhas/e-mail e 30/IP em 15 min. Revisar para deployment distribuído. | Implementado/testado |
| BR-014 | 2026-11-23 | RFQ por fornecedor/briefing imutável; token aleatório armazenado como hash, 14 dias, revogável. | Implementado/testado |
| BR-015 | 2026-11-23 | Link público de proposta: token com hash, 30 dias, revogável; proposta V1 publicada preservada. | Implementado/testado |
| BR-016 | 2026-11-23 | API pública nunca entrega `unit_net_cents`, `net_total_cents`, `tax_cents`, `fee_cents`, `supplier_id` nem IDs internos desnecessários. | Implementado/testado |
| BR-017 | 2026-11-23 | RFQ enviada uma vez por lote; confirmação idempotente e auditoria. Comunicação real por e-mail ainda não está implementada. | Implementado/testado parcialmente |
| BR-018 | 2026-11-23 | Lead demo: validação de campos, antiabuso, armazenamento com acesso ao operador; definir consentimento, retenção e CRM antes de produção. | Parcial; dependências externas |
| BR-019 | 2026-11-23 | Repositório público não conterá arquivos de transcrição, senhas, credenciais ou caminhos pessoais. Reescrita do histórico é decisão separada. | Parcial; arquivo removido só do HEAD |
| BR-020 | 2026-11-23 | Não fazer deploy com `NEXO_DEMO=1`; configurar TLS, segredos, backup, auditoria, monitoração, migração de banco e política LGPD. | Pendente de produção |

## Operação e regras financeiras

| ID | Data | Regra | Estado |
|---|---|---|---|
| BR-021 | 2026-11-23 | Briefing por serviço aéreo/hospedagem/salas-A&B/transfers, validação condicional, flags estritos e campos inativos limpos. | API parcialmente implementada/testada; wizard pendente |
| BR-022 | 2026-11-23 | Versionamento de briefing: V1/V2 imutáveis, cada RFQ referencia exatamente a versão enviada. | Snapshot implementado/testado |
| BR-023 | 2026-11-23 | Hospedagem audita apartamentos × diárias × tarifa, ocupação, café, impostos e condições de cancelamento; políticas específicas por cliente são configuráveis, não globais. | Requisito; matriz detalhada pendente |
| BR-024 | 2026-11-23 | Financeiro calcula em centavos com parâmetros de incidência, arredondamento definido, versionamento e segregação NET/venda. Não impor taxa fiscal universal. | Base e testes parciais; modelagem avançada pendente |
| BR-025 | 2026-11-23 | Matriz compara NET, disponibilidade, café, distância, cancelamento e condições; recomendações não se baseiam só no preço. | Home ilustrativa; app pendente |
| BR-026 | 2026-11-23 | Proposta publicada é snapshot imutável; revisões criam nova versão e registram ator, data e decisão. | Base e testes parciais; editor completo pendente |
| BR-027 | 2026-11-23 | Fornecedor vê somente sua RFQ; cliente não vê outros projetos nem valores internos, consultor trabalha em escopo autorizado. | Base/testes parciais |
| BR-028 | 2026-11-23 | Planejamento conecta tarefas, responsáveis, prazos e decisões comerciais do evento. | Snapshot inicial; redesenho pendente |
| BR-029 | 2026-11-23 | Importação Excel nunca altera dados sem prévia, validação e permissão; Excel não é fonte transacional. | Requisito futuro |
| BR-030 | 2026-11-23 | Indicadores exibidos no produto devem refletir dados reais; o marketing identifica claramente dados ilustrativos. | Decidido |

## Processo e critérios de qualidade

| ID | Data | Regra | Estado |
|---|---|---|---|
| BR-031 | 2026-11-23 | Todas as mudanças relevantes passam por branch/PR, teste, registro datado e atualização de brandbook/roadmap quando pertinente. | Implementado na governança |
| BR-032 | 2026-11-23 | Testes obrigatórios: autenticação, autorização, CSRF, links públicos, idempotência, V1/V2, arredondamento, service briefing, regressão de dados públicos. | 39 testes automatizados na rodada anterior; revisão contínua |
| BR-033 | 2026-11-23 | Capturas de telas precisam ser geradas do HTML/servidor real e incluir commit, viewport, data e indicação de ambiente demonstrativo. | Pipeline de evidência em implementação |
| BR-034 | 2026-11-23 | Toda regra, mudança e padrão novo precisa de ID, data da alteração, justificativa, estado, arquivo afetado e PR/teste. | Decidido |
| BR-035 | 2026-11-23 | Não declarar website/app "pronto para produção" sem validação visual, testes end-to-end, LGPD, segurança, carga, observabilidade e aprovação explícita. | Decidido |

## Revisão editorial e operacional — 2026-11-24

| ID | Data | Regra | Estado |
|---|---|---|---|
| BR-036 | 2026-11-24 | Homepage B usa história específica: mudança de briefing → impacto operacional ilustrativo → decisão, cálculo de room nights e visibilidade por perfis. Proibidos painéis falsamente acionáveis. | Implementado em branch; QA pendente |
| BR-037 | 2026-11-24 | Interface ativa do workspace em `workspace-v2/`. Não carregar sidebar azul, DM Sans, Manrope ou classes de `frontend/` histórico. | Implementado em branch |
| BR-038 | 2026-11-24 | Projetos são contexto de trabalho; briefing, RFQ, cotação, proposta e execução usam navegação e histórico do mesmo projeto. | Implementado em branch; testes E2E pendentes |
| BR-039 | 2026-11-24 | Nova versão do briefing só é persistida depois da validação condicional Python. RFQs previamente geradas continuam ligadas à versão original. | Implementado em branch; teste e revisão pendentes |
| BR-040 | 2026-11-24 | Tabela financeira mostra NET, tributos, fee e venda somente ao perfil autorizado; cliente público recebe somente total comercial. Comparação de fornecedores exige escopo equivalente. | Implementado parcialmente; revisão de fórmulas pendente |
| BR-041 | 2026-11-24 | Links criados para RFQ/proposta são mostrados apenas no momento da criação e envio é **manual**, não simular notificações ou disparos automáticos. | Implementado em branch; E2E pendente |
| BR-042 | 2026-11-24 | Mobile deve reordenar informação: painel V1/V2 em leitura vertical e opções de hotel com tarifas/condições completas, sem cortar informação essencial. | Implementado na home; QA de aparelho pendente |
| BR-043 | 2026-11-24 | Captura de workspace deve registrar login de demonstração, visual do projeto, wizard e cotação do código real, sem screenshot sintético de UI futura. | Pipeline ampliado; confirmação pendente |
| BR-044 | 2026-11-24 | Padrões de interface datados são revisáveis. Nova diretriz exige ADR e changelog, com divergências documentadas, não alteração silenciosa. | Decidido |

| BR-045 | 2026-11-24 | Rascunhos são privados por usuário/empresa/projeto; salvar não cria V2, publicar versão válida apaga somente rascunho do autor. Todas as operações usam CSRF e permissão do servidor. | Implementado e testado |
| BR-046 | 2026-11-24 | Texto de apresentação e condições comerciais são integrados ao snapshot imutável da proposta; o público não recebe colunas NET, impostos ou fee internos. | Implementado em branch; revisão editorial pendente |

| BR-047 | 2026-11-24 | Hero pode nomear e-mails, planilhas e digitação repetida **sem alterar layout, cores ou componentes existentes**. A ideia de cenário fictício no primeiro scroll é pesquisa não aprovada. | Somente copy implementada; seção experimental revertida |
| BR-048 | 2026-11-24 | Nunca afirmar integrações automáticas ERP/CRM/e-mail ou substituição dos sistemas existentes enquanto não existirem; diferenciar fluxo Alpha de conectores corporativos futuros. | Decidido; requisitos documentados, sem seção visual adicional |
| BR-049 | 2026-11-24 | Posicionamento pela dor é permitido **como texto no hero existente** e conectado à prova V1/V2 já aprovada. O exemplo “quatro cadastros” é hipótese qualitativa, não percentual de mercado, e não exige criar seção visual. | Copy implementada; demais aplicações dependem de aprovação |
| BR-050 | 2026-11-24 | Antes de publicar prova social/ROI, entrevistar operadores e verificar métricas reais de retrabalho, tempo e erro; dados externos devem conservar amostra, período e geografia. | Pesquisa pendente |

## Contratos de implementação (status atual)

- Frontend homepage: `homepage/dist/index.html`, `styles.css`, `app.js`.
- Workspace **ativo na branch**: `alpha-snapshot/workspace-v2/` (interface nova operacional). `alpha-snapshot/frontend/` é somente histórico e não é carregado.
- API FastAPI/SQLite: `alpha-snapshot/backend/`; rota `/` (home), `/app` (workspace), `/api/auth/login`, `/api/public/demo-requests`, links públicos de RFQ e proposta.
- Fonte visual canônica: `design/brandbook-v2/nexo-tokens.json` / `BRANDBOOK_V2.md`; versão v1 preservada.
- Evidências: GitHub Actions, `evidencias/`; leia o README para ver se capturas e PDF gerado estão presentes.

**Última revisão:** 2026-11-24. Itens P0/P1/P2 e próximos marcos em [ROADMAP.md](ROADMAP.md).
