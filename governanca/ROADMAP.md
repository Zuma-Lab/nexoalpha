# Roadmap — do conceito ao lançamento

**Versão:** 1.1 · **Criado:** 2026-11-23 · **Última revisão:** 2026-11-24 · **Nome de trabalho:** NEXO Alpha.  
**Princípio:** trabalho em marcos com **gates de aceite**, sem prometer prazos de calendário antes de dimensionamento técnico.  
**Definição de terminado:** design, backend, frontend, testes, privacidade, documentação e validação do usuário coerentes.

## Visão geral

```text
COMEÇO — Fundação                   MEIO — Produto operacional                    FIM — Lançamento
M0 contexto/ADR -> M1 identidade -> M2 segurança -> M3 briefing -> M4 sourcing -> M5 proposta -> M6 operação -> M7 QA -> M8 deploy
          |                 |                  |               |                  |                    |
        GATE 0            GATE 1             GATE 2          GATE 3             GATE 4               GATE 5
```

### COMEÇO — Fundações e especificação

| Marco | Status em 2026-11-23 | Entregáveis e por quê | Critério de saída |
|---|---|---|---|
| M0. Inventário, decisões, escopo | Em execução | Recuperar requisitos e testes do legado, mapear fluxos, organizar ADR, changelog, responsáveis, riscos e critérios de aceite. Evita repetir o produto antigo. | Regras priorizadas, rastreabilidade e backlog P0/P1/P2 aprovados |
| M1. Identidade e homepage produto | Implementação B em revisão (PR #1) | Brandbook 2.1, tokens, nova home, capturas desktop/mobile, formulário e CTAs; nome/domínio ficam provisórios. | Revisão visual em navegadores; A11y, conteúdos, nome e branding apropriados |
| M2. Plataforma e segurança de base | Implementado parcialmente/testes na branch | Tenancy, sessão HttpOnly, CSRF, rate limit, tokens públicos expirados/revogáveis, backups, auditoria, logs sem dados sensíveis. Segurança precede dados reais. | Testes e revisão de segurança; ambiente de staging isolado, migrações e HTTPS |

### MEIO — Produto e fluxos comercial/operacional

| Marco | Status | Entregáveis e integração | Critério de saída |
|---|---|---|---|
| M3. Briefing inteligente por serviço (P0) | Wizard V2 e rascunho por usuário ligados à API; anexos e QA pendentes | Wizard para aéreo, hospedagem, salas/A&B e transfers, rascunho, anexos, validação, V1/V2, comparação de alterações, permissão por empresa e versão imutável. | E2E criar/editar/versionar; regras do NEXO convertidas em testes de equivalência; dados isolados |
| M4. Rede de fornecedores e RFQ (P0) | API + frontend V2 conectados, envio ainda manual | Cadastro categorizado, seleção, batch, tokens expirados, respostas, disponibilidade, auditoria, idempotência e comunicação real, envio/reenvio controlado. | Ciclo pedido→resposta íntegro e idempotente; concorrência e expiração testadas |
| M5. Comparação e editor de proposta (P0/P1) | Cotação e proposta com apresentação/termos em snapshot, editor avançado e QA pendentes | Matriz com NET, taxas, café, cancelamento, seleção multiopção; editor profissional com agrupamentos, termos, V1/V2 imutáveis, aprovação e rastro de cálculos. | Zero vazamento de NET, arredondamento determinístico e proposta publicada assinada pela versão |
| M6. Planejamento, acessos e operação (P1) | Navegação por projeto e tarefas V2 implementadas; demais rotinas pendentes | Dashboard funcional, perfis por empresa, tarefas, prazos, checklists, notificações, auditoria e visibilidade de clientes. | Fluxo aprovado→planejado auditável, testes de permissão e entregáveis por serviço |

### FIM — Homologação, publicação e evolução

| Marco | Status | Entregáveis | Critério de saída |
|---|---|---|---|
| M7. Qualidade/homologação (P0) | Pendente | Testes E2E, acessibilidade WCAG AA, navegadores/mobiles, desempenho, OWASP, migrações, backup/restore, monitoramento, políticas LGPD e retenção; UAT com fluxos reais de teste. | Evidência registrada, zero bloqueadores P0 e aprovação do usuário |
| M8. Identidade final e lançamento (P1) | Bloqueado por decisões de marca e infra | Nome/domínio escolhidos, verificação de marca, logos finais, URL canonical/OG, branding de app, e-mail/CRM de leads, hospedagem TLS, ambiente de produção, runbook e rollback. | Checklist de go-live assinado, monitoramento ativo e recuperação ensaiada |
| M9. Pós-lançamento / P2 | Não iniciado | Importação/exportação Excel, portal fornecedor avançado, integrações, relatórios, fechamento financeiro, melhorias contínuas. | Métricas reais, feedback e bugs priorizados |

## Sequência de trabalho priorizada

1. **P0 — Segurança:** concluir e revisar autenticação, CSRF, tenant, RFQ, proposta, token e LGPD.
2. **P0 — Jornada funcional:** briefing serviço → RFQ → comparativo → editor de proposta → aprovação; a UI deve nascer do design system, não de CSS legado.
3. **P0 — Testes e QA:** equivalência do legado, regressão, E2E e performance mínima.
4. **P1 — Marketing e operação:** homepage polish, fluxo de demonstração, fonte local, SEO condicionado ao domínio, e-mail/CRM.
5. **P1 — Implantação:** infra, migrações e observabilidade; feedback e suporte.
6. **P2 — Expansão:** integrações e automação avançada.

## Interfaces entre frentes

- M3 determina capturas de briefing real para a homepage.
- M4 determina disponibilidade/respostas para a matriz real.
- M5 determina o editor real e a proposta pública.
- M8 depende da marca e domínio (não assumir `nexo.com.br`).
- Governança, design e segurança atravessam todos os marcos.

## Aceite mínimo por marco

| Eixo | Evidência exigida |
|---|---|
| UX e marca | Screenshots do build real, componentes próprios, estados de erro, desktop e mobile |
| Negócio | Caso de teste de cada regra crítica, cálculo e versionamento |
| Segurança | Autorização multiempresa, tokens expirados/revogáveis, CSRF, cookies, abuso e auditoria |
| Qualidade | CI verde, testes end-to-end, critérios WCAG, avaliação manual |
| Operação | Configuração por ambiente, backup, monitoração, logs, runbook |
| Registro | Changelog, ADR, README e roadmap atualizados, com commit/data |

## Evidência de mercado e posicionamento — 2026-11-24

- Nova seção de dor e retrabalho na homepage logo após o hero, com fontes fictícias 180/210 pessoas; subtítulo de e-mails/planilhas/cadastros repetidos.
- [Pesquisa com fontes e ressalvas](PESQUISA_DORES_E_MENSAGEM_HOME_2026-11-24.md): validar com 5–8 consultores/gestores antes de afirmar resultados.
- **Dependência M4–M9:** sincronização de e-mail, CRM ou ERP externos não existe; priorizar conforme requisitos e segurança, sem prometer centralização de todos os sistemas.
- **Critério de aceite M1:** clareza e compreensão da dor, leitura mobile, ausência de métricas fabricadas e ligação visível com o produto demonstrado.

## Critério de maturidade após direção B (2026-11-24)

- **Implantado no código não significa pronto em produção**: validação manual, teste multitenant, dados reais com autorização, serviço de e-mail e política LGPD continuam como gates.
- **O que avançou**: nova UI funcional de projetos, wizard, RFQs, cotação e proposta, sem stylesheet anterior; nova narrativa editorial da homepage.
- **O que ainda é parcial**: anexos, importação Excel, regras comerciais/sourcing equivalentes ao legado, cálculo fiscal por contrato, editor de termos, portal fornecedor, envio real, observabilidade e acessibilidade homologada.
- **Naming segue em aberto**. Não fazer redesign irreversível do logotipo antes de aprovação.

## Próxima iteração objetiva

- Publicar para revisão screenshots e brandbook v2 **da homepage da branch**, não confundir com UI final do workspace.
- Revisar o wizard V2 no navegador e ampliar paridade das regras do briefing.
- Homologar RFQ, cálculo financeiro e propostas em E2E; usar capturas reais do workspace após verificação visual.
- Guardar decisões abertas OPEN-01 a OPEN-05; não travar naming/domínio nesta etapa.

**Referências de trabalho:** PR #1 e issues #2 (workspace) e #3 (publicação). **Revisão seguinte:** ao aceitar PR ou alterar a marca.
