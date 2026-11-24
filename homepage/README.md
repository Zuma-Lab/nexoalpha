# NEXO — Homepage centrada no produto (nome provisório)

## Direção B — revisão crítica 2026-11-24

Homepage em HTML/CSS/JavaScript sem runtime do mockup exportado. A narrativa começa na dor da fragmentação (e-mails, planilhas, sistemas e informação duplicada), mostra cenários fictícios conflitantes na primeira rolagem e segue para alteração de briefing, impactos operacionais ilustrativos, comparação financeira de 315 room nights e uma matriz de visibilidade por perfil. Composição e cores seguem `../design/brandbook-v2/nexo-tokens.json`.

- `dist/index.html`: documento semântico, navegação, simulações com dados fictícios e formulários.
- `dist/styles.css`: sistema editorial responsivo em grafite/creme, sem painel SaaS genérico. Textos secundários de 10–11px ainda devem passar por auditoria visual e zoom.
- `dist/app.js`: menu, diálogo, login via `/api/auth/login` com cookie de sessão e pedido de demo via `/api/public/demo-requests`.
- `dist/assets/`: identidade visual e arquivos históricos ainda presentes; o hero fotográfico não é utilizado.

## Mensagem de dor — revisão de 24/11/2026

- **Hero:** “O briefing mudou. A operação continua.” com subtítulo de e-mails, planilhas e cadastros repetidos.
- **Primeiro scroll / `#retrabalho`:** 4 registros de um mesmo evento ilustrativo com 180/210 participantes, mostrando perda de contexto entre caixa de entrada, planilha, sistema comercial e sistema operacional.
- **Ponte:** a plataforma estrutura briefing, RFQ, comparação e proposta em um projeto, mas **não** sincroniza automaticamente sistemas externos ou e-mails.
- Pesquisa qualitativa, fontes e limites: [pesquisa e arquitetura editorial](../governanca/PESQUISA_DORES_E_MENSAGEM_HOME_2026-11-24.md).
- Imagens reais do novo trecho: [desktop e mobile](../evidencias/capturas/README.md) após CI.

## Visualizar

```bash
python -m http.server 4173 --directory homepage/dist
```

A prévia estática permite avaliar o layout, mas **não autentica ou recebe pedidos de demonstração** sem API na mesma origem. Para testar fluxos reais, usar o servidor FastAPI descrito na raiz.

## Pendências antes da publicação

1. Configurar domínio público e inserir `og:url` + canonical definitivo; imagem Open Graph já é acessível publicamente, mas deverá ser substituída por card PNG específico do produto.
2. Configurar notificações / CRM para leads: pedidos são persistidos no banco Alpha e consultáveis por administradores; não há e-mail automático.
3. Hospedar Inter localmente (esta versão carrega a fonte pelo Google Fonts).
4. Homologar responsividade, contraste, leitores de tela e fluxo de login em navegador real.
5. Substituir exemplos ilustrativos por capturas **reais** após implementação e aprovação do novo workspace.
6. Publicar política de privacidade e retenção de dados antes de capturar leads em produção.

A direção A e o mockup exportado permanecem históricos, não são o runtime da direção B. A seção de fotos reais fica para quando houver acervo com licença/autorização. Não gerar fotografias artificiais para simular clientes.

## Evidências e identidade atualizada

As capturas reais em desktop e mobile ficam em [evidencias/capturas](../evidencias/capturas/README.md). O brandbook atualizado (v2) está em [design/brandbook-v2](../design/brandbook-v2/BRANDBOOK_V2.md), e todas as regras/alterações/roadmap ficam em [governanca](../governanca/README.md). Nenhum domínio está definido; `nexo.com.br` não deve ser usado. Nome atual apenas de trabalho.
