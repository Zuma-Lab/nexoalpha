# NEXO Alpha — API e workspace recuperados

Aplicação independente em FastAPI/SQLite. Este diretório é um **snapshot de código recuperado**, não um atestado de prontidão para produção nem a interface definitiva da NEXO Alpha.

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

## Testes

```bash
python -m pip install pytest httpx
python -m pytest -q
```

Testes incluem autenticação, CSRF, limite de tentativas, isolamento de cliente, versionamento de briefing/proposta, expiração de links, idempotência do envio de RFQ, arredondamento financeiro e leads.

## Para produção

Necessário configurar infraestrutura de publicação, HTTPS, segredos, observabilidade, backups e políticas de retenção; exigir revisão de segurança. O workspace interno ainda não foi remodelado integralmente no novo design system. As credenciais de demonstração só devem ser ativadas localmente com `NEXO_DEMO=1`.

Para consultar leads da homepage por API, configurar `NEXO_LEADS_ADMIN_EMAIL` com o e-mail exato do operador autorizado; administradores de workspaces de clientes não recebem acesso aos leads globais por padrão.
