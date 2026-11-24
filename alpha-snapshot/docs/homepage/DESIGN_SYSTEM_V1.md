# NEXO Alpha — Direção visual homepage (v1)

**Estado:** tokens propostos por aproximação visual da primeira prévia aprovada, **não são valores extraídos de um brandbook oficial**.

## Personalidade

Premium, corporativa, editorial e contemporânea. Contraste entre uma imagem humana/cinematográfica na primeira dobra e interfaces funcionais de alto rigor. O produto deve parecer construído para pessoas que gerenciam operações complexas, e não um site montado com widgets genéricos.

## Paleta proposta

| Uso | Token | Valor inicial |
| --- | --- | --- |
| Fundo escuro principal | `--nexo-ink` | `#101214` |
| Grafite de superfície | `--nexo-charcoal` | `#1B1F23` |
| Laranja CTA | `--nexo-orange` | `#FF850B` |
| Laranja interação | `--nexo-orange-hover` | `#E66F00` |
| Fundo claro quente | `--nexo-paper` | `#FAF8F4` |
| Card claro | `--nexo-white` | `#FFFFFF` |
| Texto principal | `--nexo-text` | `#171A1C` |
| Texto secundário | `--nexo-muted` | `#61666B` |
| Borda clara | `--nexo-border` | `#E8E5E1` |
| Sucesso operacional | `--nexo-success` | `#297B58` |

### Tipografia

- Interface: `Manrope` ou `DM Sans` (escolher 1 para consistência); fallback system sans.
- Headline: peso 700–800, tracking levemente negativo, linhas curtas e ritmo editorial.
- Texto comum: 16–18px no desktop; blocos de corpo com comprimento moderado.
- Evitar usar mais de duas famílias tipográficas no site.

### Geometria e espaçamento

- Container de página 1200–1280px, com margens laterais fluidas.
- Espaçamento entre seções 88–128px no desktop, 56–80px no mobile.
- Grid 12 colunas para hero e apresentações; módulos 3x2 em desktop, 2/1 coluna em telas menores.
- Raios: CTA 999px, cards 14–20px, mockup 20–26px.
- Sombras sutis, profundidade maior reservada ao mockup do hero.
- Borda de 1px de contraste suave, especialmente nos cards claros.

### Direção de fotografia

- Primeiro plano humano com executivo de costas ou três-quartos; vista urbana no entardecer; luz quente, sombras profundas e composição crível.
- Hero com overlay suficiente para legibilidade e posição do personagem que **não concorra com o texto**.
- Seção intermediária de benefícios pode usar viagem corporativa/avião **provisoriamente**, mas evitar limitar a marca exclusivamente a viagens: NEXO também atende grupos e eventos.
- Nada de imagens stock genéricas de reunião com pessoas sorrindo à câmera.

### Composição-chave

**Hero:** cabeçalho discreto; esquerda para título/descrição/CTA; centro para personagem; direita para mockup de painel operacional. Em mobile, reordenar como título → CTA → preview, sem sobreposição ilegível. Dashboard não precisa mostrar dados reais até integrar a aplicação, mas suas amostras devem ser identificadas como ilustrativas em contexto de demonstração.

**Módulos:** ícones pequenos de traço consistente, texto conciso, muito respiro; nada de seis cards espremidos em uma única linha se reduzir a legibilidade.

**Benefícios:** faixa cinematográfica que aparece depois dos módulos; deve quebrar a monotonia sem multiplicar cards.

**Rodapé:** preto/grafite, texto discreto, páginas reais e sem redes sociais inventadas.

## Componentes planejados

`PublicHeader`, `HeroSplit`, `ProductPreview`, `FeatureCard`, `BenefitPanel`, `ProcessSteps`, `PlatformTour`, `SocialProof`, `DemoCTA`, `PublicFooter`, `MobileNavigation`.

## Garantias de implementação

- Não usar a screenshot como imagem de fundo com textos embutidos. Recriar semanticamente com HTML/CSS e assets independentes.
- A landing **pública** terá arquitetura visual distinta do workspace **autenticado**, com tokens compartilhados seletivamente.
- Não reaproveitar CSS nem componentes do sistema anterior; implementar no diretório ALPHA e manter o legado intacto.
- Documentar decisões e atualizar esta especificação em vez de depender apenas da memória da conversa.