# Brandbook v2.1 — NEXO Alpha (nome provisório)

**Versão:** 2.1 · **Data de edição:** 2026-11-25 (America/Sao_Paulo)  
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

## 02. Direção B — narrativa operacional editorial (vigente em 2026-11-24)

A direção A, com painel V1/V2 isolado à direita de um grande título, tornou-se **histórica** após auditoria crítica. A direção atual é **B**: contar uma decisão comercial de modo específico e verificável, sem layout padronizado de marketing SaaS.

1. **Hero editorial:** “O briefing mudou. A operação continua.” Título assimétrico, hierarquia clara e princípio operacional no lugar de screenshot decorativo ou foto.
2. **Caso de uso contextual:** alteração de participantes, apartamentos e salas; painel de impacto; próxima ação. **Os impactos ainda são demonstrativos e não automações de produção.**
3. **Raciocínio financeiro:** 315 room nights (105 apartamentos × 3 diárias), tarifa NET, café e cancelamento; Hotel A/B/C fictícios e com fórmula explicada. Proibido recomendar automaticamente pela tarifa unitária.
4. **Permissões em matriz:** mesmo projeto, três visões — consultor, cliente e fornecedor — em vez de cartões idênticos.
5. **Contato e login funcionais:** formulários com status real; não transformar texto decorativo em falso botão.
6. **Mobile específico:** painéis empilhados e opções de hospedagem em cartões legíveis, sem recortar informações decisivas.

O laranja identifica uma ação, campo alterado ou algo que exige atenção; não deve colorir palavras aleatórias dos títulos. Ilustrações sem resultado real devem ser explicitamente rotuladas.

**Importante:** a nova homepage ainda é material do Alpha, não a confirmação de que todas as automações de impacto/cotação estão implementadas. O workspace V2 tem backend funcional parcial, mas demanda homologação.

## 02B. Refinamento editorial autorizado em 25/11/2026 — sem alterar identidade

- **Título do hero:** “O evento é um só. A informação não deveria estar em tantos lugares.” com texto curto sobre e-mails, planilhas e versões desencontradas.
- **Primeira rolagem:** “Sua equipe precisa conduzir eventos. Não reconstruir informações.” e imagem existente de briefing, mantendo a prova V1/V2 logo abaixo.
- **Visual de sistema** entra no hero. **Fotografia 01 da pessoa** fica como material opcional, não forçar terceiro bloco visual.
- **Preservados:** grafite `#111315`, laranja `#FF850D`, creme `#F3EFE9`, fonte Inter, botões existentes, cenário fictício e ressalvas comerciais.
- **Redução de densidade:** títulos A/B fazem papéis distintos, os parágrafos de apoio são curtos e as seções de cotações e permissões mantêm dados de negócio essenciais.
- Não é aprovação de brandbook final/naming; screenshots reais devem ser gerados e revisados antes de merge.

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

## 04. Tipografia e voz editorial

- Fonte primária: **Inter** 400/500/600/700; fallback system-ui/Segoe UI/Arial. Evitar apenas aumentar pesos 700 para disfarçar falta de hierarquia.
- **Homepage B:** headline 52–90px desktop, ~42–61px mobile; line-height 1.01; letter-spacing -0.064em. Texto de apoio 16–19px desktop, 15px mobile. Labels editoriais de 10–11px somente quando tiverem contraste e não forem o único acesso à informação.
- **Workspace V2:** corpo 14px, títulos de 26–35px, controles de 12–14px, tabelas de 12px, apoio 11–12px, sempre verificando contraste e zoom 200%.
- Labels em maiúsculas são coordenadas operacionais: **etapa / contexto / tipo de documento**. Evitar “a sua jornada conectada” e títulos sem objeto concreto.
- Inter continua carregada do Google Fonts na branch; hospedagem local e análise de licença/privacidade seguem bloqueios antes do go-live.
- Evitar incluir dados pessoais em capturas ou exemplos de marketing.

## 05. Layout, densidade, componentes e contraste

- Conteúdo máximo: **1340px** na homepage; margem lateral 96px desktop, 48px tablet e 32px mobile (somatório das duas bordas).
- Seções: 113px desktop, 82px tablet, 62px mobile, conforme contexto e não simplesmente repetidas em todos os blocos.
- Header: 76px desktop, 65px mobile. Menu responsivo por volta de 650px; reordenar informação, não apenas encolher colunas.
- Hierarquia: narrativa editorial pode usar superfícies escuras; operação interna usa superfícies claras para leitura prolongada e navegação grafite para orientação.
- Raios: botões/inputs 5px; superfícies e diálogos até 8px; reduzir sombras decorativas, manter bordas de separação de 1px.
- Fonte de cor: `nexo-tokens.json`, com grafite `#111315`, laranja `#FF850D`, creme `#F3EFE9`, cinzas neutros e estados não exclusivos da cor.
- Alvo WCAG 2.2 AA, foco por teclado, regiões com `aria-live` e tabela ou lista semanticamente rotulada. Padrões de fonte e tamanho mínimo dependem da importância e do contexto, não de um número único universal.

## 06. Componentes e microinterações

**Header:** logotipo provisório; nav âncora; CTA demo; login distinto; menu mobile via `aria-expanded`.  
**Hero:** título editorial orientado a problema real; o caso em três etapas fica numa seção independente, com rótulos de demonstração.  
**Tabelas e cartões de opção:** no workspace, tabela densa com cabeçalho, unidades e totais. Na homepage mobile, comparação por fornecedor em cartões com tarifa, café, cancelamento e total; não cortar colunas sem sinalização.  
**Botões:** foco visível, estados hover/disabled/loading, mínimo de 44px para alvos críticos.  
**Formulários:** labels explícitos, obrigatório indicado, `type=email`, feedback `aria-live`, limite de envio e proteção antiabuso.  
**Diálogos:** `<dialog>` nativo, fechar por botão e Escape, foco adequado; homologar leitor de tela.  
**Motion:** transições curtas ~180–220ms, sem movimentos gratuitos e com `prefers-reduced-motion`.

## 07. Acessibilidade e responsividade

**Alvo:** WCAG 2.2 AA. Texto normal ≥4,5:1; texto grande ≥3:1. Componentes e limites visuais relevantes ≥3:1. Sem depender exclusivamente de cor para mudanças de estado. Usar `lang=pt-BR`, skip link, HTML semântico, texto alternativo relevante, estados de foco e teclado, validação compreensível e `aria-live`.

**Telas de referência:** desktop 1440×960; mobile 390×844. Capturar também o workspace V2 autenticado. Verificar 1280px e 768px, zoom 200%, sem overflow lateral na página e com scroll interno apenas em tabelas quando intencional.

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

## 11. Aplicação atual e divergências conhecidas

| Elemento | Implementação em PR #1 | Pendência |
|---|---|---|
| Homepage B | Narrativa de briefing alterado, cálculo de room nights, matriz de acesso, contato e login | QA visual final, fontes locais, domínio/SEO e LGPD |
| Workspace V2 | `alpha-snapshot/workspace-v2/`, interface própria clara com navegação grafite, operações por projeto, fila, wizard, RFQs, cotação, propostas, tarefas | Testes end-to-end amplos, segurança multiempresa e homologação de regras |
| Wizard de briefing | Criação real de versões imutáveis e campos condicionais, reaproveitando somente regras do negócio | Anexos, categorias adicionais e paridade total do legado |
| Cotação | Quantidade, custo NET em centavos, bps de imposto e fee, total da API | Harmonização de unidades/tributação por contrato, importação Excel e seleção com escopos equivalentes |
| Propostas | Versões e links públicos com custos internos filtrados pela API | Editor de cláusulas avançado; apresentação e condições já integram o snapshot. Envio real e fluxo de renovação de links |
| Identidade | Paleta e tipografia de trabalho | Nome/dominio e logo final; não adotar `nexo.com.br` |
| Screenshots | Chromium autenticado com dados locais fictícios | Auditoria manual de UX, WCAG e múltiplos navegadores |
| Branding | Manual e tokens 2.1 como fonte canônica | PDF regenerado pela CI, suporte a marca definitiva |

**Arquivo histórico:** `alpha-snapshot/frontend/` continua em Git, mas não é servido em `/app`. Não tratá-lo como a interface ativa.

## 12. Critérios de aceite e próximos passos

**Aprovar visual:** revisar capturas desktop/mobile; revisar tipografia, contraste e comportamento do menu/formulário.  
**Aprovar funcional:** aplicar design ao workspace novo, executar testes de permissão, cálculo e fluxo completo.  
**Aprovar marca:** escolher nome/dominio, verificar legalidade/identidade, completar logo.  
**Aprovar lançamento:** produção segura, LGPD, monitoramento, backups, SEO, QA e consentimento.

**Histórico:** v1 preservada; v2 de 2026-11-23 (direção A) substituída pela **v2.1 em 2026-11-24 (direção B)**. Toda alteração posterior deve atualizar `governanca/REGISTRO_DE_ALTERACOES.md` e a data no JSON.
