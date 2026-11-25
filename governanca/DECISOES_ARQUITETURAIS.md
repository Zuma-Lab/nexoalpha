# Registro de decisões (ADR)

Data base: **2026-11-23** · Fuso: **America/Sao_Paulo**. Revisar este arquivo a cada mudança de escopo.

| ID | Data | Decisão / razão | Estado | Aplicação |
|---|---|---|---|---|
| ADR-001 | 2026-11-23 | **Alpha independente do NEXO legado**. O usuário rejeitou reaproveitar layout, frontend, API e estrutura do produto anterior. Reaproveitar somente conceitos, regras de negócio e testes como especificação. | Decidido | `Zuma-Lab/nexoalpha` |
| ADR-002 | 2026-11-23 | **Homepage centrada no produto (direção A)**, com briefing V1/V2 como peça principal, sem hero de executivo artificial. | **Substituído em 2026-11-24 por ADR-015** | `homepage/dist/` |
| ADR-003 | 2026-11-23 | **Identidade temporária grafite/laranja/off-white/Inter**, usando `design/brandbook-v2/nexo-tokens.json` como fonte canônica de novas telas. | Decidido como direção, marca provisória | Design system |
| ADR-004 | 2026-11-23 | **Autenticação por cookie HttpOnly e proteção CSRF**, no mesmo domínio; nunca token de sessão em `sessionStorage`. | Implementado em branch; precisa homologação | API/frontend |
| ADR-005 | 2026-11-23 | **RFQs e propostas públicas com prazo e revogação**, tokens aleatórios armazenados como hash, permissão mínima. | Implementado em branch; precisa homologação | API |
| ADR-006 | 2026-11-23 | **Propostas públicas não expõem NET, fee, tributos internos ou IDs internos.** | Implementado em branch e testado | API |
| ADR-007 | 2026-11-23 | **Documentação versionada e regenerável no GitHub**, PDF derivado de fonte, capturas reais geradas pelo navegador, CI como evidência. | Em implementação | `governanca/`, `design/`, `evidencias/` |
| ADR-008 | 2026-11-23 | **NEXO é nome de trabalho, não marca final registrada**. Não usar `nexo.com.br` no código nem fixar domínio. Alternativas: Benexo, Nexobe, Bnexo; avaliar naming, marca, domínio e identidade após escolha. | Em aberto | Marca/SEO |
| ADR-009 | 2026-11-23 | **Preservar histórico v1, sem confundir snapshot e sistema final**. O `alpha-snapshot` é base recuperada, não interface nova homologada. | Decidido | Documentação |
| ADR-010 | 2026-11-23 | **Sem dados de clientes reais nos mockups**. Gráficos, números, propostas e perfis demonstrativos são rotulados como ilustração. | Decidido; implementado na homepage | Marketing |
| ADR-011 | 2026-11-23 | **Fotografias de IA do lote antigo não são necessárias** para homepage centrada no produto. Se usar fotografia depois, exigir material real/autorizado/licenciado. | Decidido para home atual | Conteúdo |
| ADR-012 | 2026-11-23 | **Nada será mesclado à `main` sem revisão.** Pull request em draft é o caminho auditável para a entrega entre computadores. | Decidido para esta rodada | Git |
| ADR-013 | 2026-11-23 | **A identidade pode mudar após validação do nome.** Até lá, não alterar logos em massa, nem adquirir/dominar uma marca sem checagem. | Pendente de decisão | Marca |
| ADR-014 | 2026-11-23 | **Prioridade de produto:** briefing por serviço, sourcing/RFQ, matriz, editor de proposta, operação e aprovação; segurança e autorização são transversais. | Decidido como ordem | Roadmap |

| ADR-015 | 2026-11-24 | **Direção editorial B substitui o template SaaS da direção A.** Hero orientado ao problema real; caso V1→V2→impacto→próxima decisão; cálculo de room nights e matriz de permissões em vez de cartões idênticos. | Implementado na branch; QA de navegador pendente | `homepage/dist/` |
| ADR-016 | 2026-11-24 | **Workspace operacional V2 criado do zero**, sem carregar CSS/HTML do `alpha-snapshot/frontend/`. Projeto é a unidade de navegação: briefing, fornecedores, comparativo, proposta e execução como etapas de uma operação. | Implementado na branch; homologação pendente | `alpha-snapshot/workspace-v2/` |
| ADR-017 | 2026-11-24 | **Funcionalidade antes de decoração.** O wizard chama validação Python real, as tabelas usam totais da API, links RFQ/proposta informam envio manual, e estados de erro e leitura ficam explícitos. | Implementado parcialmente; E2E em execução | `workspace-v2/app.js` e API |
| ADR-018 | 2026-11-24 | **Identidade continua provisória**; aplicar brandbook 2.1 no Alpha sem fixar nome, domínio ou logo geométrico final. A marca pode mudar após decisão posterior. | Decidido | Design e governança |

| ADR-019 | 2026-11-24 | **Rascunhos de briefing pertencem ao usuário e projeto**, são persistidos na API sob CSRF e autorização, e são eliminados quando a versão definitiva é registrada. Nenhuma versão publicada pode ser sobrescrita. | Implementado na branch; teste automatizado | API e workspace V2 |
| ADR-020 | 2026-11-24 | **Conteúdo comercial estruturado na proposta** (apresentação e termos) é congelado junto aos itens e valores por versão; API pública só expõe campos apropriados ao cliente. | Implementado na branch; revisão de segurança adicional pendente | API/propostas V2 |

| ADR-021 | 2026-11-24 | **Mensagem de dor no início da homepage**: fragmentação entre e-mails, planilhas, sistemas internos e versões contraditórias. A resposta do produto deve ser contextual e verificável, sem prometer sincronização automática de sistemas externos. | Decidido para teste editorial; implementado na branch | `homepage/dist/`, pesquisa de dores |
| ADR-022 | 2026-11-24 | **Proposta não aprovada:** criar seção na primeira rolagem com quatro registros contraditórios. O proprietário reafirmou que pediu mudança de mensagem, não de layout ou paleta. | Revertido no mesmo dia; hipótese somente na pesquisa | Homepage e comunicação |

| ADR-023 | 2026-11-24 | **Regra de autorização por dimensão:** copy, layout, tipografia, cor, imagem e funcionalidade são escopos separados. A alteração de copy não autoriza modificar os demais. Guardar estado de aprovação no PR e registrar rollback. | **Confirmado** pelo proprietário após erro de escopo; referência obrigatória | [Guia editorial](GUIA_EDITORIAL_E_APROVACAO_HOMEPAGE.md) |
| ADR-024 | 2026-11-24 | **Reduzir densidade nas primeiras dobras preservando a identidade aprovada.** Direção sugerida: título A no hero, título B na primeira rolagem, menos copy redundante, imagens 02/03 em destaque e 01 opcional. | **Proposta em análise**, não autorização de alterar o runtime | Homepage e prévias |

## Decisões pendentes de aprovação

| ID | Assunto | Opções/impacto | Dependência |
|---|---|---|---|
| OPEN-01 | Marca final | NEXO Alpha (provisório), Benexo, Nexobe, Bnexo ou novo nome. Requer pesquisa marcária e domínio. | Antes de publicar URL canônica |
| OPEN-02 | URL pública | Domínio a contratar/hospedar. Não assumir `nexo.com.br`. | SEO, OG, cookies, ambiente |
| OPEN-03 | Captação de leads | E-mail, CRM, consentimento, política LGPD e prazo de retenção. | Go-live da home com formulário |
| OPEN-04 | Stack da produção | FastAPI + banco transacional definitivo, filas, hospedagem, observabilidade. SQLite continua somente base de desenvolvimento até decisão. | Lançamento |
| OPEN-05 | Marca gráfica | Validar geometria vetorial, proporções e versão final dos logos. | Antes do kit comercial definitivo |

**Última revisão documental:** 2026-11-24. As datas das ADRs são datas das decisões e não dos commits de documentação.
