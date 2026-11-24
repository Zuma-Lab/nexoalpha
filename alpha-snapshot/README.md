# NEXO — Alpha 01

Nova implementação do zero para a central de gestão de briefings, cotações, RFQs, propostas, planejamento e acessos.

**Esta pasta é independente do sistema NEXO anterior.** Nenhum arquivo, componente, endpoint, migration ou layout do legado foi importado. Os requisitos funcionais foram reconstruídos a partir dos fluxos definidos para o produto.

## Iniciar localmente

Requisitos: Python 3.11+ e dependências `requirements.txt`.

```bash
cd NEXO/ALPHA
python -m venv .venv
source .venv/bin/activate    # Windows: .venv\Scripts\activate
pip install -r requirements.txt
NEXO_DEMO=1 python -m uvicorn backend.main:app --reload
```

Abra `http://127.0.0.1:8000`.

**Acesso somente para demonstração local:** `admin@nexo.local` / `NexoDemo!2026`.

No Windows PowerShell:

```powershell
$env:NEXO_DEMO="1"
python -m uvicorn backend.main:app --reload
```

Para testes:

```bash
pip install pytest httpx
pytest -q
```

Dados persistem em `data/nexo-alpha.sqlite3` (arquivo gerado ao executar). Para um ambiente vazio, rode sem `NEXO_DEMO=1` e implemente o provisionamento inicial de administradores antes de comercializar.

## Funcionalidades implementadas

- Login com senha derivada via `scrypt`, sessões aleatórias de duração limitada e RBAC server-side.
- Estrutura multiempresa com clientes vinculados a projetos e acesso de usuários clientes limitado aos próprios projetos.
- Projetos com protocolo, status, escopo e informações de evento.
- Briefing estruturado com versões **imutáveis**.
- Diretório de fornecedores e lotes RFQ que referenciam versão fixa do briefing.
- Links públicos de resposta por token armazenado somente como hash; respostas padronizadas e prevenção de duplicatas.
- Lançamento de itens de cotação com cálculo de NET, tributos, fee e total em centavos inteiros.
- Propostas com snapshots imutáveis, versões e publicação; link de avaliação, aprovação, rejeição e solicitação de ajustes.
- Planejamento com atividades, prazos e estados.
- Trilha de auditoria e perfis de acesso (admin, consultant, client, viewer).
- Interface responsiva inédita com dashboard, projeto em abas, modais, tabelas e fluxos integrados.

## Limites da Alpha

Este é **um primeiro incremento funcional**, não o sistema completo pronto para produção. O registro de envio de RFQ é manual: o link é produzido, mas não dispara e-mail. Ainda não há SMTP/ESP, importação/exportação Excel, upload de documentos, integração financeira, portal de fornecedores autenticado, matriz avançada de comparação, notificações, rate limiting, recuperação de senha, token com expiração/revogação, convites por e-mail, SSO, 2FA, provisionamento SaaS, observabilidade nem testes de carga. O briefing contempla o núcleo do escopo e precisa ganhar os campos operacionais granulares de hotelaria, rooming, alimentação, aéreo e transfers para implantação real.

**Não use os dados de demonstração, conta padrão ou configuração de desenvolvimento em produção.** Pré-requisitos para implantação: cookies HttpOnly com CSRF protegido (ou mecanismo autenticador equivalente), TLS, gestão segura de segredos, política de retenção LGPD, backups, migrações versionadas, autorização ampliada e revisão de segurança.

## Estrutura

```text
ALPHA/
├── backend/
│   ├── db.py           # esquema relacional independente
│   ├── security.py     # derivação de senha e hashes de tokens
│   └── main.py         # API, regras e montagem da SPA
├── frontend/
│   ├── index.html      # estrutura do app
│   ├── styles.css      # design system original
│   └── app.js          # componentes e interações independentes
├── tests/
│   └── test_workflow.py
├── docs/
│   └── ARCHITECTURE.md
├── requirements.txt
└── run.sh
```

A marca visual em Alpha usa **tokens provisórios**, pois o brandbook NEXO definitivo não estava entre os materiais recuperados. Nenhum ativo Paytrack foi reproduzido.