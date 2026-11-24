# Brandbook v2 — NEXO Alpha (nome provisório)

**Versão:** 2.0 · **Data de edição:** 2026-11-23 (America/Sao_Paulo)  
**Fonte técnica canônica:** [nexo-tokens.json](nexo-tokens.json)  
**PDF gerado:** [NEXO-Alpha-Brandbook-v2.pdf](NEXO-Alpha-Brandbook-v2.pdf)  
**Governança:** [regras BR](../../governanca/PADROES_E_REGRAS.md) · [ADRs](../../governanca/DECISOES_ARQUITETURAIS.md) · [roadmap](../../governanca/ROADMAP.md)

> **Identidade de trabalho, não marca definitiva.** A marca pode mudar para Benexo, Nexobe, Bnexo ou outra após validação de nome, domínio e marca. Não utilizar o domínio `nexo.com.br`. A geometria do símbolo vetorial e o logotipo final ainda dependem de aprovação. Este guia registra a direção **atual** e não substitui a verificação legal de marca.

## 01. Posicionamento

Plataforma B2B para transformar solicitações, briefings e cotações de eventos/grupos corporativos em propostas, decisões e planejamento rastreáveis.

**Promessa descritiva atual:** "Do briefing à proposta aprovada, em uma única trilha".  
**Essência:** clareza operacional + precisão comercial + continuidade entre etapas.  
**Voz:** profissional, consultiva, objetiva, sem jargão gratuito. Mostrar contexto e utilidade, não frases vagas.

**Evitar:** fotos sintéticas de clientes, promessas de funcionalidades inexistentes, métricas sem fonte e imitar marcas concorrentes. Qondor/Perk são referências conceituais de organização e experiência, não fontes de código, marca, textos ou telas para reprodução.

## 02. Direção de homepage aprovada

**Direção A:** o **produto** é o protagonista. A página apresenta:

1. **Hero:** comparação de briefing V1/V2 em HTML semântico (campos participantes, apartamentos, salas, período, transfers), sem hero fotográfico.
2. **Trilha:** 01 briefing, 02 fornecedores, 03 cotação, 04 proposta.
3. **Matriz comercial:** alternativas e trade-offs, com preços fictícios rotulados; custos NET nunca aparecem na visão pública do produto.
4. **Papéis:** solicitante, consultor e fornecedor; permissões diferentes e explicadas.
5. **Conversão:** CTA primário "Solicitar demonstração"; ação de entrar distinta e autenticada.
6. **Rodapé:** nome provisório e referência a ambiente em desenvolvimento, sem depoimentos inventados.

As telas do hero são **demonstrações construídas em HTML**, não capturas do workspace interno. Substituí-las por capturas do aplicativo somente quando o editor definitivo existir, for testado e aprovado. Fotografias reais/licenciadas podem ser introduzidas em seções editoriais futuras, se fizerem sentido.

## 03. Cores — tokens de referência

| Token | Valor | Aplicação |
|---|---|---|
| `graphite` | `#111315` | Fundo principal escuro, textos sobre fundos claros |
| `canvas` | `#0B0D0F` | Fundo profundo, rodapé, rail |
| `surface` | `#1B1D20` | Painéis escuros e cards do produto |
| `raised` | `#25282C` | Elevação e contraste de painéis |
| `border` | `#454A50` | Divisórias sobre fundos escuros |
| `orange` | `#FF850D` | Ação primária, destaque editorial |
| `orange_hover` | `#F5A044` | Hover no laranja |
| `orange_pressed` | `#E77300` | Estado pressionado |
| `cream` | `#F3EFE9` | Seções claras |
| `white` | `#FFFFFF` | Superfícies brancas e texto principal escuro |
| `muted` | `#B8BDC4` | Texto secundário sobre grafite |
| `light_muted` | `#565C63` | Texto secundário sobre off-white |
| `light_border` | `#D9D4CD` | Bordas em temas claros |
| `orange_text` | `#A84800` | Destaque e texto quente sobre off-white |
| `success` | `#B9E56C` | Feedback positivo em superfícies escuras |
| `warning` | `#FFD166` | Avisos |
| `danger` | `#FF9A9A` | Erros em superfícies escuras |
| `info` | `#9DC8FF` | Informação contextual |

**Regra de aplicação:** preferir tokens semânticos; nunca inventar novos verdes, azuis ou amarelos porque existam no NEXO legado. Garantir contraste real, incluindo hover, disabled e estados de erro.

## 04. Tipografia

- Família primária: **Inter**, pesos 400, 500, 600, 700; fallbacks system-ui, Segoe UI e Arial.
- Homepage atual: Inter carregada pelo Google Fonts. **Pendente antes de produção:** empacotamento licenciado no próprio site, sem compartilhar arquivos de fonte em mensagens.
- Headline hero: `clamp(38px, 4.55vw, 66px)` desktop; `clamp(34px, 9vw, 46px)` mobile; line-height 1.065; letter-spacing -0.035em.
- Corpo: 16px e line-height 1.6. Destaque/lead: 18px. Navegação: 14px. Controles: 15px.
- Mockup HTML: textos não inferiores a 12px; preferir 13–14px em tabelas e 16px em texto normal. A antiga imagem ilustrativa tinha textos de 7–10px e foi retirada do hero.
- Pesos: 400 texto comum, 500 elementos secundários, 600 títulos, 700 CTAs/etiquetas.

## 05. Grid, espaçamento, raios e bordas

- Conteúdo máximo: **1280px**; container: `calc(100% - 64px)` desktop, -48px tablet, -32px mobile.
- Espaçamento base 4px; escala `4, 8, 12, 16, 24, 32, 48, 64, 96` px.
- Seções: 114px de padding vertical desktop, 80px tablet, 69px mobile (valores da home atual).
- Header: 80px desktop, 68px mobile; gap desktop do hero 66px.
- Raios: input 8px, botão 10px, card 16px, diálogo 18px, pill 999px.
- Bordas padrão 1px; foco visível 3px em laranja com offset 4px.
- Breakpoints efetivos na home: ≤620px, ≤850px, ≤1100px; tokens citam desktop base de referência ≥1200px. Não confundir com os breakpoints históricos da v1.

## 06. Componentes e microinterações

**Header:** logotipo provisório; nav âncora; CTA demo; login distinto; menu mobile via `aria-expanded`.  
**Hero:** texto em coluna + demonstração em HTML; tabela tem cabeçalhos semânticos e dados ilustrativos.  
**Tabelas:** cabeçalhos com escopo, números alinhados e cálculo exibido em moeda; rolagem horizontal quando necessário sem esmagar o texto.  
**Botões:** foco visível, estados hover/disabled/loading, mínimo de 44px para alvos críticos.  
**Formulários:** labels explícitos, obrigatório indicado, `type=email`, feedback `aria-live`, limite de envio e proteção antiabuso.  
**Diálogos:** `<dialog>` nativo, fechar por botão e Escape, foco adequado; homologar leitor de tela.  
**Motion:** transições curtas ~180–220ms, sem movimentos gratuitos e com `prefers-reduced-motion`.

## 07. Acessibilidade e responsividade

**Alvo:** WCAG 2.2 AA. Texto normal ≥4,5:1; texto grande ≥3:1. Componentes e limites visuais relevantes ≥3:1. Sem depender exclusivamente de cor para mudanças de estado. Usar `lang=pt-BR`, skip link, HTML semântico, texto alternativo relevante, estados de foco e teclado, validação compreensível e `aria-live`.

**Telas de referência:** desktop 1440×960; mobile 390×844. Verificar também 1280px e 768px, zoom 200%, sem overflow lateral na página e com scroll interno apenas em tabelas quando intencional.

A validação por captura demonstra aparência em determinada resolução, **não substitui auditoria WCAG, teste E2E e QA manual**.

## 08. Logo e fotografia

- **Conceito atual:** símbolo angular laranja + wordmark branco/minúsculo em fundo grafite. Arquivos vetoriais preliminares em `assets/brand/nexo-logo-v1/` e `homepage/dist/assets/`.
- **Ainda não aprovado:** geometria definitiva, proporção de símbolo, tipografia do wordmark e versões de aplicação após naming. Não afirmar que o SVG é marca registrada ou logotipo final.
- Área de proteção e tamanhos mínimos serão definidos após homologação do logo; na homepage atual a imagem do header usa aproximadamente 120px de largura.
- A fotografia antiga do executivo foi rejeitada como artificial. O acervo de IA é histórico; não o utilizar como evidência de clientes, eventos ou usuários reais.
- O PDF v1 permanece preservado; o v2 é nova fonte de referência, não edição silenciosa da versão anterior.

## 09. Segurança, UX de dados e conteúdo comercial

- Cookies de sessão HttpOnly/Strict/Secure (HTTPS) com CSRF para mutações.
- Exibir versão de briefing e histórico; nunca mudar retroativamente V1 ou proposta publicada.
- Fornecedor vê apenas a própria RFQ; cliente só dados autorizados da própria empresa/projeto.
- Não renderizar NET, taxas internas, fee ou margens em rota pública de proposta.
- Expiração proposta dos links: RFQ 14 dias e proposta 30 dias; necessidade de renovar é risco operacional documentado.
- Formulário demo armazena dados na base Alpha. Antes de produção: aviso LGPD, política, retenção, e-mail/CRM e consentimento, sem declarar conformidade jurídica concluída.

## 10. Marca e domínio — decisão em aberto

**Nome provisório:** NEXO Alpha; **não usar `nexo.com.br`**. Considerar Benexo, Nexobe, Bnexo ou alternativa, após pesquisa de disponibilidade e conflitos marcários, análise de pronúncia e posicionamento. Não registrar `og:url`/canonical até a URL final. Adapte cores e logo somente após decisão explícita e ADR novo.

## 11. Aplicação e divergências conhecidas

| Parâmetro | Especificação v2 | Situação atual |
|---|---|---|
| Paleta | Tokens v2 | Homepage majoritariamente alinhada |
| Tipografia | Inter local + fallbacks | Google Fonts na home; local pendente |
| Logo | Identidade definitiva | Geometria provisória |
| Produto no hero | Briefing V1/V2 HTML | Implementado como demonstração |
| Imagens reais do produto | Captura do workspace final | Pendente |
| Login | Sessão segura e fluxo real | API integrada na branch, teste E2E pendente |
| Lead demo | Persistência + consentimento e destino | Persistência sim, CRM/LGPD pendentes |
| OG/canonical | URL pública do domínio final | Em aberto por naming |
| Capturas | Executadas com código da branch | Automatização e revisão visual |
| Acessibilidade | WCAG 2.2 AA | Boas práticas implementadas, auditoria pendente |

## 12. Critérios de aceite e próximos passos

**Aprovar visual:** revisar capturas desktop/mobile; revisar tipografia, contraste e comportamento do menu/formulário.  
**Aprovar funcional:** aplicar design ao workspace novo, executar testes de permissão, cálculo e fluxo completo.  
**Aprovar marca:** escolher nome/dominio, verificar legalidade/identidade, completar logo.  
**Aprovar lançamento:** produção segura, LGPD, monitoramento, backups, SEO, QA e consentimento.

**Histórico:** versão v1 de 2026-11-23 preservada. **Esta versão v2 registrada em 2026-11-23**, para a direção A e exigências do Claude. Toda alteração posterior deve atualizar `governanca/REGISTRO_DE_ALTERACOES.md` e a data no JSON.
