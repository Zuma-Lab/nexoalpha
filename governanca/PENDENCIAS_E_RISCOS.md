# Pendências, bloqueios e riscos

**Criado:** 2026-11-23 · **Última revisão:** 2026-11-24 · **Escopo:** NEXO Alpha. A prioridade considera o produto para produção; home está em revisão.

| ID | Criticidade | Estado | Risco / pendência | Ação de mitigação | Dependência |
|---|---|---|---|---|---|
| R-001 | P0 crítico | Aberto | Snapshot SQLite e autenticação ainda requerem hardening para implantação real. | Revisão de segurança, banco transacional/infra, TLS, segredos, migrations, backups e E2E. | M2/M7 |
| R-002 | P0 crítico | Parcial | BR de tenant/perfil deve ser validada em todos os endpoints, não apenas nos testes correntes. | Testes de autorização cruzada e análise de queries/escopos. | M2-M6 |
| R-003 | P0 alto | Parcial | Portabilidade do legado ainda cobre só briefing em Python, não toda a lógica de `workflow.cjs`, `commercial.cjs` e `sourcing.cjs`. | Inventariar cenários, implementar Python independente, testes de paridade. | M3-M5 |
| R-004 | P0 alto | Parcial | Sem editor visual definitivo de briefing/proposta no layout Alpha. | Wizard por serviço + editor novo com testes E2E. | M3/M5 |
| R-005 | P0 alto | Parcial | Link de RFQ/proposta expira; política operacional de renovação e reenvio ainda precisa desenho e teste. | Criar fluxo de renovação auditável sem reutilizar token vencido. | M4/M5 |
| R-006 | P0 alto | Parcial | Privacidade de transcrições no histórico do Git público. | Avaliar tornar privado e/ou reescrever histórico com backup e aviso a colaboradores. | Aprovação |
| R-007 | P1 alto | Bloqueado | Marca e URL final indefinidas; `nexo.com.br` indisponível segundo o proprietário. | Pesquisa marcária/domínio de Benexo/Nexobe/Bnexo e alternativa, aprovação do nome. | OPEN-01/02 |
| R-008 | P1 alto | Aberto | Homepage com formulário coleta leads sem política de privacidade/retenção publicada, canal de destino e consentimento definido. | Revisar LGPD, retenção, CRM/e-mail e política antes de go-live. | OPEN-03 |
| R-009 | P1 médio | Aberto | Fonte Inter é carregada pelo Google Fonts, não empacotada. | Hospedar fonte licenciada em assets e revisar fallback/licenças. | M1/M8 |
| R-010 | P1 médio | Em revisão | Identidade gráfica ainda tem geometria vetorial pendente e brandbook v1 usa logo raster antigo. | Validar marca final, recriar logo e regenerar kit após naming. | OPEN-05 |
| R-011 | P1 médio | Em revisão | Screenshot visual e contraste precisam inspeção em navegadores; CI de pytest não prova qualidade visual. | Capturas reais, testes mobile/desktop, inspeção manual e acessibilidade. | M1/M7 |
| R-012 | P1 médio | Pendente | Open Graph sem `og:url` definitivo e PNG social ainda é provisório. | Configurar domínio canônico depois de escolher marca; imagem social apropriada. | M8 |
| R-013 | P1 médio | Pendente | Sem serviço de e-mail/CRM configurado para demo e disparo de RFQ. | Escolher serviço, integração segura, testes de entrega e monitoramento. | OPEN-03/M4 |
| R-014 | P2 | Planejado | Excel, portal completo fornecedor, analytics e fechamento financeiro avançado. | Priorizar após ciclo comercial completo validado. | M9 |

## Gates bloqueantes para produção

- [ ] Nome e domínio aprovados e verificados
- [ ] TLS/cookies Secure, segredos, banco e backup/restore configurados
- [ ] Política LGPD e fluxo de contato de leads aprovados
- [ ] App completo (briefing, RFQ, cotação, proposta, aprovação) validado
- [ ] Testes de papéis, concorrência, dinheiro, links e CSRF aprovados
- [ ] QA visual e acessibilidade com evidências
- [ ] Métricas, logs, monitoramento, recuperação e rollback
- [ ] Aprovação de lançamento pelo proprietário

**Referência de execução:** [roadmap](ROADMAP.md), PR #1, issues #2/#3.
