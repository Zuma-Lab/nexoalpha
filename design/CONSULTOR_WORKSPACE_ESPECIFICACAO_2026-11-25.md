# NEXO Alpha — Sistema operacional do consultor | auditoria e padrão de telas

**Data:** 2026-11-25 (America/Sao_Paulo)  
**Branch de trabalho:** `feat/consultor-fluxo-prioritario-20261125` (derivada da branch-base do PR #1).  
**Estado:** auditoria baseada no código + refinamento funcional experimental da fila; **não aprovado para merge ou produção**.  
**Objetivo real:** reduzir reentrada, busca e decisão sem contexto. Não criar “um dashboard” só para ostentar indicadores.

## 1. Fontes e distinção de evidências

**Confirmado no código da branch-base (inspecionado):**
- `alpha-snapshot/workspace-v2/app.js`: `queue()`, `nextAction()`, `projectOverview()`, `rfqPage()`, `quotePage()`, `proposalPage()`, `planningPage()`, `wizard()`, `action()`.
- `alpha-snapshot/backend/main.py`: endpoints `/api/dashboard`, `/api/projects`, `/api/projects/{pid}`, briefing-draft, RFQ batches/send, quote-items, propostas, tarefas e permissão de perfil/tenant.
- `alpha-snapshot/backend/db.py`: `owner_id` em `projects` e `plan_tasks`; `supplier_id` em `quote_items`; versões em `briefing_versions` e `proposals`.
- `evidencias/capturas/workspace-fila-desktop.png`, `workspace-briefing-desktop.png` e `workspace-cotacao-desktop.png` são screenshots da UI real na branch-base (não homologação).
- `assets/visuals/05-briefing-etapas-exploratorio.webp` e `06-briefing-inteligente-exploratorio.webp` são **conceitos estáticos** escuros, não recursos implementados nem permissão para refazer o workspace.
- `design/brandbook-v2/nexo-tokens.json` e `BRANDBOOK_V2.md` são regras visuais canônicas (marca provisória).

**Pesquisa externa, sem extrapolação estatística para o Brasil:**
- Cvent, *How Venue Sourcing is Changing in 2026*, baseado em 1.650 planners: especificações e atrasos em respostas de RFP são obstáculos, e a pressão por orçamento é relevante. https://www.cvent.com/en/blog/events/venue-sourcing-trends
- Qondor, *8 event agency workflows to centralise in 2026*: valor vem de **compartilhar dados entre proposta, orçamento e fornecedores**, não de colocar oito menus independentes lado a lado. É posicionamento do próprio fornecedor, não estudo independente. https://qondor.com/blog/8-event-agency-workflows-to-centralise-in-2026

**Hipótese de produto a validar:** consultor prioriza resposta pendente, mudança de escopo, negociação financeira e proposta; não uma tela com métricas de marketing. Entrevistar 5–8 usuários reais e medir tarefas antes de afirmar ganho de tempo.

## 2. Auditoria crítica com impacto operacional

| ID | Severidade | Evidência na base | Problema observado | Consequência | Decisão |
|---|---|---|---|---|---|
| C-01 | **P0** | `nextAction(p)` usa apenas `p.status`; `queue()` inclui notas estáticas e contadores | Fila não mostra motivos de prioridade derivados de RFQs, propostas e histórico | Consultor abre projeto sem saber o próximo passo | **Primeira correção nesta branch:** inbox derivada de fatos por tenant |
| C-02 | **P0** | `rfqPage()` conserva links em `state.rfqBatch`; token só retorna uma vez | Ao sair/recarregar, links preparados não são recuperáveis; UI de marcar envio depende do lote temporário | Convites presos sem envio ou recuperação clara | Rotação/renovação auditável de token e retomar lote; issue dedicada antes do piloto |
| C-03 | **P0** | `proposalPage()` mantém `state.proposalLink` temporariamente | Draft publicado em DB pode perder a via de revisão/compartilhamento ao atualizar a página | Consultor não consegue completar ou retomar versões sem contorno | Editor persistente + reemissão segura de links; não expor hash/token persistido |
| C-04 | **P0** | `changes()` compara somente participantes, destino, datas, singles, twins e plenária | Exibir “não houve alteração” quando mudou outro campo é possível | Cotação baseada em escopo divergente | Diff semântico completo dos campos por serviço e versionamento RFQ |
| C-05 | **P0** | `quotePage()` cria item sem selecionar `supplier_id`, apesar do backend suportar o campo | Resposta do fornecedor e item financeiro ficam desconectados | Retrabalho e comparativo não auditável por fornecedor | Importar/selecionar resposta e condições ao criar item |
| C-06 | **P0** | Modelo `quote_items` guarda `quantity` genérica; issue #4 aberta | Apartamentos × diárias, ocupação, taxas e unidades não são campos tipados | Totais financeiros potencialmente incomparáveis | Priorizar issue #4 antes de recomendar o melhor fornecedor |
| C-07 | **P1** | `plan_tasks.owner_id` existe, mas `planningPage()` cria tarefa sem responsável | Atribuição e acompanhamento por consultor ainda não são eficazes | Pendências não pertencem claramente a alguém | Adicionar responsável por tarefa, permissão e filtro |
| C-08 | **P1 / política** | `projects.owner_id` registrado; `/api/projects` lista todos da empresa; `canSeeMoney()` oculta NET apenas de `client` | “Minha fila” e papel viewer não possuem política granular completa | Mistura de “meus” e “da equipe”; visibilidade financeira do viewer precisa ser validada | Definir matriz RBAC antes de alterar acesso do viewer |
| C-09 | **P1** | `projectOverview()` mostra CTA de briefing/quotes fixos | CTA pode não corresponder à situação ou ao bloqueio principal do projeto | Cliques desnecessários e confusão de fluxo | Usar mesma origem factual da inbox no resumo do projeto |
| C-10 | **P1** | Screenshots e app demonstram conteúdos genéricos repetidos em sidebar/painéis | Densidade informativa competindo com itens operacionais | Baixa escaneabilidade | Uma ideia por área; avisos só quando alterarem uma decisão |
| C-11 | **P1** | Stepper real 4 etapas; imagens conceituais 3 e 5 etapas | Referências visuais divergem do fluxo real | Copiar mockups pode quebrar validações | Preservar quatro etapas reais: Evento → Serviços → Especificações → Revisão |
| C-12 | **P0 para lançamento** | Envio RFQ e proposta por link manual, sem e-mail integrado | Uma tag “Enviado” não comprova entrega externa | Falsa expectativa sobre automação | Separar “Preparado”, “Entrega manual registrada” e “Resposta recebida” |

**Nota de segurança:** não classificar a visibilidade de `viewer` como vazamento comprovado sem decisão de política; o backend também permite leitura de itens para o viewer atual. É uma **decisão de escopo/RBAC** de alta prioridade. Nunca “corrigir” acesso de um perfil no frontend somente — validar autorização no backend.

## 3. Jobs-to-be-done do consultor (prioridade real)

1. **Agora:** “Em quais projetos preciso agir e por quê?” — ações vindas de estados verificados, ordenadas por impacto; nada de cards decorativos.
2. **Antes de cotar:** “Qual briefing vale e o que mudou?” — versão vigente, impacto em convites existentes e mudanças por serviço.
3. **Durante sourcing:** “Quem recebeu, quem ainda não respondeu e qual condição falta?” — RFQ por serviço/fornecedor/versão, prazo e prova de entrega.
4. **Ao negociar:** “Estamos comparando a mesma unidade de serviço?” — quartos/noites, participantes, café, disponibilidade, cancelamento e impostos.
5. **Antes de enviar proposta:** “O orçamento fecha e não vai expor meus custos internos?” — propostas derivadas do orçamento, com preview fiel e snapshot.
6. **Depois da decisão:** “O que minha equipe precisa executar, até quando e quem é o responsável?” — tarefas com owners e marcos derivados de serviços aprovados.
7. **A qualquer momento:** “Onde encontro a decisão, o arquivo e a versão que originaram este valor?” — trilha auditável do mesmo evento.

## 4. Arquitetura de informação aprovada vs proposta

**Navegação global recomendada para o consultor (mantendo a sidebar já existente):**
- `Fila de trabalho`: motivos de atenção e prioridade, **não** indicadores genéricos.
- `Projetos`: carteira, pesquisa e filtros (meus / equipe após política de ownership).
- `Fornecedores`: cadastro/rede, fora da execução de uma RFQ específica.
- No futuro, itens globais de administração/documentos/relatórios somente após função, política e dado reais.

**Dentro de um projeto (manter tabs locais existentes):**
`Visão geral` → `Briefing` → `Fornecedores / RFQs` → `Comparativo` → `Propostas` → `Planejamento`.

Não criar um menu “Cotações” global duplicado com a aba do projeto sem uma decisão explícita entre visão transversal e contextual.

### Contratos de tela

| Tela | Informação primária (primeira dobra) | Uma ação principal | Visual / estados |
|---|---|---|---|
| Fila | Ação necessária, motivo, projeto, responsável e status verificável | **Abrir etapa** | Itens ordenados por risco; sem painéis didáticos longos |
| Visão do projeto | Contexto do evento, versão, etapa e decisão pendente | **Próxima ação real** | Histórico secundário; preserva visão de etapas |
| Briefing | Formulário por serviço, versão, mudanças e validação | **Salvar rascunho / Registrar versão** conforme estado | 4 etapas reais e avisos de impacto em RFQs |
| RFQs | Versão enviada, fornecedor, serviço, resposta e prazo | **Gerar/regularizar convites** | Mensagens explícitas sobre envio manual e expiração |
| Comparativo | Fornecedores por serviço e mesma unidade, NET privado, condições e preço | **Selecionar e revisar orçamento** | Tabela legível, detalhe de impostos, room nights |
| Propostas | Versão comercial, condições e prévia do cliente | **Revisar / Publicar versão** | Snapshot e permissões; link renovável |
| Planejamento | Entregas e responsáveis por serviço, marcos e dependências | **Atribuir / concluir tarefa** | Lista/timeline baseada em datas reais |

## 5. Design system que NÃO deve ser reinventado

**Congelado:** grafite `#111315`, laranja `#FF850D`, creme `#F3EFE9`, Inter, logotipo angular provisório, bordas neutras e sidebar grafite. Fonte: `design/brandbook-v2/nexo-tokens.json`.

**Harmonização proposta, sujeita à aprovação visual:** telas operacionais extensas podem manter superfícies claras (workspace real) para leitura de tabela; imagens de briefing escuras servem de referência para hierarquia e atmosfera, não autorização para converter todas as telas em preto. Um shell/sidebar, breadcrumb e tabs consistentes.

**Componentes únicos:** `ProjectContextHeader`, `PriorityActionRow`, `StatusTag`, `VersionDiff`, `SupplierRFQRow`, `FinancialComparison`, `ProposalSnapshot`, `TaskRow`, `AsyncState`. São **contratos propostos**; o JS atual ainda é monolítico, não há biblioteca de componentes criada.

**Densidade:** mais espaço para tabelas e ações, menos textos explicando princípios básicos. Sem “AI glow”, sem chips com números fabricados, sem imagens de marketing ocupando área de cálculo.

**Acessibilidade e mobile:** CTA real, foco, teclado, alt-text relevante, mensagens de erro vinculadas, contraste AA, scroll de tabela intencional, viewport 390×844 sem esconder NET/taxas para quem tem acesso.

## 6. Implementação experimental limitada nesta branch

- `alpha-snapshot/backend/consultant_queue.py`: cálculo das prioridades em consultas agregadas por `company_id`, uma ação factual por projeto aberto. Não contém tokens nem NET.
- `GET /api/consultant/queue`: exige papel `admin` ou `consultant`; `client`/`viewer` recebem 403; não altera nenhuma entidade.
- `workspace-v2/app.js`: usa endpoint na fila interna **e na ação principal do projeto**, navegando até `briefing`, `rfq`, `quotes`, `proposal` ou `planning`, preservando grid, cores e tipografia atuais. Perfis não internos mantêm fila simples existente.
- Segurança: toda leitura é escopada por empresa; `owner_is_me` é **marcador de ordenação**, não substituto de ACL; nenhum dado financeiro confidencial vai ao endpoint.
- Limitação: ações informam problemas, mas **não** fingem resolver token perdido, entrega de e-mail, comparativo tipado ou renovação de proposta. Priorização é heurística determinística, não IA e não substitui revisão humana.

**Escopo explicitamente NÃO alterado:** homepage, fotos/notebook, brandbook, tokens, modelos de dados, cálculos ou rotas públicas de clientes/fornecedores.

## 7. Cenários de aceite obrigatórios antes do merge

1. Admin/consultor vê apenas projetos da própria empresa; client/viewer recebem 403; sem login 401.
2. Projeto em qualificação apresenta **Validar escopo**; clicar abre a aba Briefing correta.
3. RFQs preparadas informam **registro de envio manual pendente**; o sistema não afirma envio automático.
4. Briefing V2 com RFQ anterior sinaliza revisão de impacto sem alterar a RFQ original.
5. Resposta recebida sem orçamento apresenta **Conferir respostas**; não cria cotação automaticamente.
6. Orçamento existente sem proposta informa **Revisar orçamento**, sem recomendar menor tarifa.
7. Proposta em draft/published mantém status fiel e não promete link recuperável.
8. Publicação/decisão e tarefas não mostram dados de outros tenants; status atualizado com dados da API.
9. Reentrar na fila atualiza consultas e ordenação, inclusive após mudar projeto.
10. Capturas reais: 1440×960 e 390×844; navegação e dados mantidos, sem regressão visual de cores/fontes.
11. A11y manual, zoom 200%, foco, estados vazios/erro, sem duplicação desnecessária de painéis.
12. Não liberar piloto até resolver C-02..C-06, segurança e governança de links.

## 8. Ordem das próximas tarefas

**P0.0** Validar inbox experimental (testes, navegação, dados sintéticos, multiempresa); aprovar o contrato de ações.  
**P0.1** Recuperação/reemissão auditável de tokens para RFQs e propostas; corrigir fluxos que param ao recarregar a página.  
**P0.2** Diff completo do briefing por serviço e associação RFQ↔briefing; não reportar falsos “sem alterações”.  
**P0.3** Modelagem financeira tipada (issue #4), vínculo de fornecedor por item, comparação por serviço e condições equivalentes.  
**P0.4** Editor de propostas retomável, snapshot privado/público e decisões; tests.  
**P1.1** Owners e prazos de atividades; filtros da fila; estados de erro/empty/loading.  
**P1.2** Modularização `workspace-v2/app.js` e revisão WCAG 2.2 AA (issue #5).  
**P1.3** Discovery de integração para eliminar redigitação (issue #6).  
**P2** Dashboards gerenciais, relatórios e gráficos — só com dados e finalidade real.

## 9. Gate de publicação

Nova branch e PR draft para revisão. Executar testes Python, JS e análise de diferenças antes de qualquer merge. Uma screenshot gerada por IA é **mockup**, nunca comprovação de funcionalidade. Não mudar `Zuma-Lab/nexo`, homepage, brandbook ou produção. Registrar BR/ADR/CHG correspondentes.

**Próxima decisão do proprietário:** confirmar o conceito de fila orientada a ações e as permissões de owner/viewer, antes de expandir a implementação para o workspace inteiro.
