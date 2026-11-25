# NEXO Alpha — API e workspace operacional V2

Aplicação independente em FastAPI/SQLite. O backend FastAPI/SQLite ainda é uma base de desenvolvimento; a interface ativa em `/app` foi reconstruída em `workspace-v2/`, sem o CSS/layout do diretório `frontend/` histórico. **Não é sistema homologado para produção.**

## Executar

```bash
python -m pip install -r requirements.txt
NEXO_DEMO=1 uvicorn backend.main:app --reload
```

Por padrão, `/` serve a homepage baseada no produto e `/app` serve o workspace. Os assets são separados em `/assets` (homepage) e `/app-assets` (workspace).

## Segurança

- Autenticação via cookie `HttpOnly`, `SameSite=Strict`; API exige cabeçalho `X-Nexo-CSRF` em operações autenticadas de alteração. No ambiente HTTPS, configurar `NEXO_SECURE_COOKIES=1`.
- Sessões de 12 horas; limite de 5 tentativas de login por e-mail e 30 por IP em 15 minutos, registrados em SQLite.
- Definir `NEXO_RATE_LIMIT_SECRET` estável e secreto em ambientes de múltiplos workers.
- RFQs públicas expiram em 14 dias; propostas públicas, em 30 dias. Links revogáveis por administradores/consultores; links legados sem expiração são invalidados pela migração.
- Pedidos de demonstração ficam armazenados em `demo_requests` e são acessíveis via `GET /api/demo-requests` por usuários administradores.
- RFQs são marcadas como enviadas manualmente, sem disparo real de e-mail.

## Central do consultor — atualização isolada de 2026-11-25

Na branch `feat/consultor-fluxo-prioritario-20261125` foi adicionada uma fila operacional de prova de conceito:
- `GET /api/consultant/queue`: só `admin` e `consultant`; agrega decisões por empresa, sem tokens ou custos NET.
- `workspace-v2/app.js`: a fila apresenta um próximo passo por projeto (briefing, RFQ, orçamento, proposta ou planejamento) e abre a aba correspondente; a visão geral do projeto utiliza a mesma fonte para sua ação principal.
- O algoritmo é determinístico baseado em dados persistidos, **não é previsão de IA**. O campo `owner_is_me` só ajuda a ordenar, não restringe acesso.
- Limitações P0 registradas: links de convite/proposta não retomáveis, diff incompleto de serviços, unidade financeira genérica, e-mail manual; o MVP sinaliza problemas, não os corrige.
- Nenhuma modificação em homepage, tokens, tabelas ou endpoints públicos. **Somente para revisão; não pronto para produção.**

## Testes

```bash
python -m pip install pytest httpx
python -m pytest -q
```

Testes incluem autenticação, CSRF, limite de tentativas, isolamento de cliente, versionamento de briefing/proposta, expiração de links, idempotência do envio de RFQ, arredondamento financeiro e leads.

## Para produção

Necessário configurar infraestrutura de publicação, HTTPS, segredos, observabilidade, backups e políticas de retenção; exigir revisão de segurança. O workspace V2 utiliza o design system operacional editorial, mas não possui editor avançado de propostas, anexos nem homologação completa. As credenciais de demonstração só devem ser ativadas localmente com `NEXO_DEMO=1`.

Para consultar leads da homepage por API, configurar `NEXO_LEADS_ADMIN_EMAIL` com o e-mail exato do operador autorizado; administradores de workspaces de clientes não recebem acesso aos leads globais por padrão.

**Portabilidade:** `backend/briefing_rules.py` valida e normaliza o formato detalhado por serviço (aéreo, hospedagem, salas/A&B e transfers); a API aceita esse formato e preserva versões anteriores. As regras de `commercial.cjs` e `sourcing.cjs` ainda não foram inteiramente portadas e precisam de cobertura de equivalência.

**Privacidade comercial:** a API pública de proposta entrega apenas descrição, quantidade e total de venda de cada item. Custos NET, tributos e fees permanecem no snapshot privado do consultor.

## Interface operacional V2 — 2026-11-24

- `workspace-v2/index.html`: shell semântico e página de autenticação.
- `workspace-v2/styles.css`: layout independente, navegação grafite, leitura em superfícies claras, componentes de formulário, cotação, versão e estados, mobile adaptado.
- `workspace-v2/app.js`: usa as rotas reais de autenticação, projetos, briefing validado, fornecedor, lote RFQ, quote items, proposta, tarefa e links públicos. HTML dinâmico escapado para evitar injeção em conteúdo de negócio.
- `frontend/`: frontend antigo preservado em Git para auditoria histórica, sem ser servido em `/app`.

O wizard registra **novas versões imutáveis**, e agora permite **salvar/retomar rascunho privado por usuário/projeto** no servidor. Alterações não salvas ainda podem se perder ao fechar a página. O envio real de RFQ/proposta permanece **manual**, sem envio de e-mails.

**Validação:** `scripts/capture_screens.py` agora também executa login, cria V2 e captura telas reais do workspace (CI). Contratos API, permissões por empresa e cálculos exigem revisão adicional antes do lançamento.
