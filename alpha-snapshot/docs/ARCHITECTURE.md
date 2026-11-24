# NEXO Alpha — Arquitetura funcional e técnica

## Contrato de reconstrução

Reaproveitar conceitos e regras de negócio, **nunca** layout, código, API ou banco de dados existentes. Raiz isolada: `NEXO/ALPHA`. Manter o projeto original intacto. Não copiar telas de Qondor/Perk: aproveitar apenas padrões de UX operacional (contexto, aprovação, visibilidade financeira).

## Papéis

| Perfil | Direitos na Alpha |
| --- | --- |
| Administrador | gerencia empresas clientes, usuários, projetos, fornecedores, RFQs, orçamento, propostas e cronograma |
| Consultor | gerencia solicitação, fornecedores, RFQs, orçamento, proposta e planejamento |
| Cliente | cria projeto, complementa o próprio briefing e visualiza somente seus projetos; não acessa NET, fees, RFQs internas ou auditoria privada |
| Leitura | acompanha o workspace, sem operações de escrita |
| Fornecedor sem conta | responde somente a RFQ específica por link público não adivinhável |
| Aprovador externo | vê a proposta publicada por link específico e registra decisão única |

## Fluxos

1. Solicitante cria `Project` e `BriefingVersion(1)`.
2. Consultor qualifica o pedido, criando `BriefingVersion(n+1)`; versões anteriores não são editadas.
3. Consultor seleciona fornecedores e cria `RFQBatch` associado a exatamente uma versão do briefing.
4. Uma `RFQ` por fornecedor possui token aleatório cujo hash é persistido. A ação de marcar envio é idempotente e **não envia e-mail nesta Alpha**.
5. Fornecedor envia resposta única pelo link e condições padronizadas são preservadas.
6. Consultor lança `QuoteItem`, armazenando entradas inteiras para cálculo determinístico de preço.
7. Uma `ProposalVersion` congela um JSON completo de itens e totais (snapshot imutável). Publicação a torna acessível por token.
8. Cliente aprova, rejeita ou solicita ajustes. O sistema registra `ApprovalDecision` e `AuditLog`.
9. Planejamento vinculado ao projeto organiza atividades e prazos.

## Entidades persistentes

`Company`, `Client`, `User`, `Session`, `Project`, `BriefingVersion`, `Supplier`, `RFQBatch`, `RFQ`, `RFQResponse`, `QuoteItem`, `Proposal`, `ApprovalDecision`, `PlanTask`, `AuditLog`.

Índices e FKs habilitados. WAL e busy timeout configurados explicitamente. Todas as consultas e mutações internas relevantes dependem de `company_id`. Em operações na borda pública, o token é resolvido apenas pelo hash SHA-256; `scrypt` protege senhas.

## Cálculo da cotação

As unidades monetárias são centavos (`int`) e percentuais são `basis points` inteiros. Para cada linha:

```text
NET = quantidade * unit_net_cents
tributos = arredondar(NET * tax_bps / 10000)
fee = arredondar((NET + tributos) * fee_bps / 10000)
VENDA = NET + tributos + fee
```

`quote_total` é a soma dos valores de venda. O snapshot comercial preserva o cálculo da versão, mesmo quando itens são alterados depois. A política de incidência de fee e impostos deve tornar-se configurável por cliente/contrato na evolução.

## API principal

| Grupo | Rotas |
| --- | --- |
| Auth | `/api/auth/login`, `/api/auth/me`, `/api/auth/logout` |
| Workspace | `/api/dashboard`, `/api/clients`, `/api/users` |
| Projetos | `/api/projects`, `/api/projects/{id}` |
| Briefing | `/api/projects/{id}/briefings` |
| Fornecedores | `/api/suppliers` |
| RFQ | `/api/projects/{id}/rfq-batches`, `/api/rfq-batches/{id}/send`, `/api/public/rfq/{token}` |
| Cotação | `/api/projects/{id}/quote-items` |
| Proposta | `/api/projects/{id}/proposals`, `/api/proposals/{id}/publish`, `/api/public/proposal/{token}` |
| Planejamento | `/api/projects/{id}/tasks`, `/api/projects/{id}/tasks/{task}` |

Documentação interativa `/docs` servida pelo FastAPI.

## Roadmap priorizado

**P0 — para piloto**: cadastro, permissões, briefing granular para aéreo/hospedagem/salas/A&B/transfers; RFQ real por e-mail com entregabilidade, prazo/expiração de links, matriz de fornecedores, edição de orçamento com negociação, aprovação de propostas, auditoria e testes completos.

**P1 — operação**: importação/exportação Excel, anexos versionados, custos e políticas por empresa, aprovação multinível, notificações, filtros avançados, configuração de marca, implantação PostgreSQL e migrações.

**P2 — expansão**: portal de fornecedores, múltiplas moedas, financeiro previsto × realizado, contratos, rooming list, automações e integração de viagens.

## Design system Alpha

Nova linguagem visual: navegação lateral escura, superfícies claras, tabelas de operação de alta densidade, tipografia Manrope/DM Sans, acento azul e padrões consistentes para estado/feedback. Os valores ficam concentrados em `frontend/styles.css` com tokens CSS. Branding é provisório até validação do brandbook NEXO.