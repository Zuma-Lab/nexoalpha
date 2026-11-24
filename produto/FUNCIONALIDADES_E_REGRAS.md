# NEXO — Inventário funcional e regras para recriação

**Princípio:** manter os processos e regras de negócio da NEXO anterior, sem reaproveitar automaticamente seu layout e suas telas. Este inventário combina decisões recuperadas, requisitos da conversa e sugestões documentadas. Itens futuros estão explicitamente marcados como tal.

## Atores e acessos

- **Administrador da plataforma:** configuração de empresas, permissões, operação e auditoria.
- **Administrador da empresa:** cria usuários, atribui perfis, administra seus próprios dados.
- **Consultor/operador:** qualifica briefings, seleciona fornecedores, dispara RFQs, cria e publica cotações/propostas.
- **Solicitante/cliente:** cria demanda, acompanha status, comenta, aprova/rejeita ou pede ajustes.
- **Fornecedor:** responde pedidos por link seguro/portal restrito, informa disponibilidade, preço, condições e anexos.

**Regras:** segregação de dados por empresa; autorização do lado do servidor em toda mutação; perfis com acesso mínimo; não revelar custos NET ao cliente se não autorizado; ações importantes com autor, timestamp e histórico; segurança/retenção LGPD e minimização de dados.

## 1. Solicitações e briefings

- Cadastro de projeto/evento: nome, cliente, destino, período, nº de participantes, orçamento indicativo, contexto, responsável, prioridade e prazo de retorno.
- Categorias configuráveis: aéreo, hospedagem/rooming, salas e A&B, transfer/transporte, audiovisual, equipe, extras.
- Formulário progressivo por categoria, com validação, salvamento de rascunho, resumo e anexos.
- **Versionamento:** criar briefing V2 sem reescrever V1 enviada; guardar diferenças/autor/data. RFQ recebe snapshot da versão exata.
- Estados sugeridos: rascunho → enviado → qualificação → sourcing → em cotação → proposta → decisão → confirmado/encerrado. Refinar os estados na implementação, com transições explícitas.

## 2. Cadastro de fornecedores

- Empresa fornecedora, categorias, regiões/cidades atendidas, contatos, canal preferido, status comercial, observações e documentos.
- Busca por categoria/localização, seleção para um lote de RFQs, histórico de respostas e negociações.
- Fornecedor sem login obrigatório no MVP; página de resposta por token aleatório, expirável, armazenado apenas como hash.
- Portal completo do fornecedor: **evolução posterior**, não requisito da primeira versão.

## 3. RFQs e sourcing

- O consultor seleciona múltiplos fornecedores para **mesma versão** do briefing.
- Um lote gera RFQ individual por fornecedor e registro de entrega; envio idempotente (`idempotency_key`) para impedir disparo duplicado.
- Estados: criado, enviado, visualizado, respondido, declinado, vencido e revisão solicitada, com prazo, lembretes e trilha.
- Recebimento de resposta estruturada por link e fallback manual para respostas via e-mail/Excel/PDF.
- Fornecedor só enxerga seu pedido e valores; não enxerga concorrentes.

## 4. Hospedagem e grupos

- Tipo e quantidade de apartamentos, single/twin, check-in/out, diárias, room nights, tarifa NET, café, impostos, taxas, estacionamento, upgrade, política de cancelamento, disponibilidade parcial/total, validade da proposta e observações.
- **Auditoria básica:** apartamentos × diárias × tarifa NET; destacar diferença entre quantidade de quartos, pessoas e noites.
- Restrições por cliente/projeto parametrizáveis: rooming list, quartos por perfil/gênero, coordenador, água/conta master, lavanderia/autorização, pagamento e faturamento, sempre por política cadastrada, não geral.
- Equipes esportivas e executivas podem ter regras comerciais específicas, mas só ativar templates quando o usuário configurar condições do cliente.

## 5. Financeiro / planilha nativa

- Grade com itens tipados por serviço; quantidade, unidade, multiplicador de diárias, custo NET, impostos, taxas, comissões, fee/markup, valor de venda e total.
- As fórmulas devem ser explícitas e consistentes, inclusive incidência de impostos e política de arredondamento; não usar exemplo ilustrativo como regra fiscal universal.
- Guardar insumos, resultados e revisões; totais recalculáveis, histórico, validações e aprovação antes da publicação.
- Diferenciar moeda, taxa, fee calculado sobre NET/venda e margem; regras de clientes (por exemplo, percentuais comerciais) são parametrizadas por empresa/contrato.
- Importação Excel com mapeamento → prévia → validação → persistência; Excel não é banco de dados.

## 6. Matriz comparativa

- Comparar alternativas lado a lado: NET, preço total, disponibilidade, café, distância, impostos, prazo de resposta, cancelamento, condições e observações.
- Evitar recomendação automática por menor preço apenas; permitir trade-offs, comentários e escolhas de combinações de fornecedores.
- Produzir orçamento de projeto a partir das linhas selecionadas, sem redigitação.

## 7. Propostas e aprovações

- Editor de proposta estruturado a partir do orçamento; dados do evento, escopo, serviços, termos e condições.
- Proposta V1 publicada fica imutável; V2 é criada como nova versão se houver alterações.
- Cliente visualiza versão publicada em página segura, aprova, rejeita ou pede ajustes; guardar usuário, data e comentário.
- Permissões controlam quem pode publicar/alterar proposta e ver custos NET.
- Exportação PDF opcional; HTML responsivo para apresentação/decisão.

## 8. Planejamento e execução

- Cronograma por projeto (tarefas, etapas, responsáveis, prazos, dependências, status), checklist, entregas por serviço, agendas e avisos.
- Conexão entre itens aprovados e tarefas operacionais: confirmar fornecedor, rooming, transfer, briefing técnico, marcos de evento, documentação.
- Visões lista, calendário e timeline podem ser consideradas conforme evidência de uso.
- Fechamento financeiro detalhado (previsto vs realizado, notas, conciliação): **futuro**, apesar da arquitetura poder prever expansão.

## 9. Comunicação e notificações

- Histórico único do projeto: ações, comentários, anexos, mensagens e alterações de status.
- E-mail de RFQ e aprovação; notificações de prazo, resposta recebida, alteração crítica e pedido de revisão.
- Evitar expor dados sensíveis em e-mails e logs. Consentimento, retenção e auditoria.

## 10. Analytics e gestão

- Dashboard executivo e do consultor com solicitações, cotações em andamento, propostas pendentes, conversão e tempo de resposta.
- Indicadores devem ser derivados de dados reais; a homepage pode usar UI **ilustrativa**, mas não apresentar números como métricas de clientes reais.

## Modelo conceitual mínimo

`Company`, `User`, `Membership`, `Role`, `EventRequest`, `BriefingVersion`, `Supplier`, `SupplierContact`, `RFQBatch`, `RFQ`, `SupplierResponse`, `SupplierResponseItem`, `Quote`, `QuoteItem`, `Comparison`, `Proposal`, `ProposalVersion`, `Approval`, `Task`, `Attachment`, `AuditEvent`.

Relacionamentos: `EventRequest` pertence a empresa; `BriefingVersion` pertence a solicitação; `RFQBatch` referencia versão congelada; `RFQ` é por fornecedor; resposta alimenta comparação e item de orçamento; proposta publicada referencia snapshot de orçamento; aprovação referencia versão publicada.

## APIs conceituais sugeridas (verificar no código antes de assumir implementadas)

- `POST /api/events`, `POST /api/events/:id/briefing/versions`
- `GET /api/suppliers`, `POST /api/events/:id/rfq-batches`, `POST /api/rfq-batches/:id/send`
- `GET /api/rfq/:token`, `POST /api/rfq/:token/response`, `POST /api/rfq/:token/attachments`
- `GET /api/events/:id/comparison`, `POST /api/events/:id/quotes`, `PATCH /api/quotes/:id/items/:itemId`
- `POST /api/events/:id/proposals`, `POST /api/proposals/:id/publish`, `POST /api/proposals/:token/decision`

## Fases de implementação

**P0:** autenticação e segregação; briefings versionados; fornecedores; RFQ em lote; resposta segura; planilha nativa; matriz.
**P1:** propostas versionadas; aprovação; Excel; respostas manuais; histórico; planejamento operacional básico.
**P2:** portal avançado de fornecedor; integrações; dashboards avançados; fechamento/conciliação pós-evento.

## Qualidade e testes necessários

Tests de autorização por empresa/perfil; idempotência de RFQs; V1/V2 imutáveis; cálculo financeiro; importação de dados; responsividade; acessibilidade; fluxo completo (briefing → resposta → cotação → proposta → decisão).