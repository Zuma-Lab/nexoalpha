# NEXO / ALPHA — Homepage v1.0

**Registro consolidado em 23/11/2026**  
**Status:** direção criativa aprovada pelo usuário; homepage ainda não implementada no código.  
**Fonte de verdade visual:** `assets/homepage/01-referencia-aprovada.png`.  
**Exploração posterior:** `assets/homepage/02-exploracao-nao-aprovada.png` — manter somente para documentar a iteração; NÃO usar como layout final.

## Objetivo da página

A homepage será a apresentação pública e comercial da NEXO e o caminho de entrada para o sistema. Deve explicar a proposta da plataforma, mostrar benefícios e funcionalidades, inspirar confiança e levar a uma demonstração ou ao login. Não confundir com o dashboard autenticado.

**Posicionamento:** Plataforma premium de gestão e cotação de eventos corporativos, grupos e demandas relacionadas; briefing, sourcing, comparação, proposta, aprovação e planejamento integrados em um fluxo único.

## O que o usuário aprovou explicitamente

- A **primeira** prévia visual é a referência central. O usuário gostou das cores, do layout inicial e, especialmente, da imagem do executivo olhando para a cidade junto a um mockup do sistema.
- Visual **clean, espaçado, executivo, premium e cinematográfico**, sem excesso de informação.
- Paleta de **grafite/escuro + laranja quente + superfícies claras creme/off-white**; alto contraste, sem retornar à identidade Paytrack (navy/amarelo).
- Manter destaque visual para mockup NEXO à direita do hero, sem deixar o conteúdo mais denso.
- Levar a seção **“Empresas que utilizam/confiam na NEXO” para o final** da página, não imediatamente abaixo do hero.
- Trazer **“Mais controle, eficiência e economia para o seu time” para o meio** da homepage, como respiro/interrupção visual entre módulos e etapas do produto.
- A segunda prévia ficou **muito carregada**, portanto NÃO usar a densidade, o agrupamento excessivo nem o bloco de depoimento inventado como referência final.
- Não usar logotipos ou depoimentos fictícios como se fossem clientes reais.

## Hierarquia definitiva proposta para implementação

1. **Hero institucional premium**: header minimalista + headline, subtítulo, dois CTAs, imagem do executivo em cenário urbano ao entardecer e mockup NEXO flutuante. O hero é o foco da página.
2. **Conheça a plataforma**: breve proposta de valor e grade de 6 módulos, preferencialmente 3 por linha no desktop, com espaçamento generoso. Módulos: Briefings, Cotações, Planejamento, Fornecedores, Acessos e equipes, Relatórios. Em mobile, 1 coluna ou scroll de cards acessível.
3. **Benefícios / seção de impacto**: “Mais controle, eficiência e economia para o seu time”, com visual cinematográfico. A imagem da janela de avião é **referência provisória**, ainda não uma escolha definitiva; alternativa coerente é fotografia de cenário executivo realista. Benefícios: agilidade nas cotações, visibilidade de custos e colaboração entre equipes.
4. **Como funciona**: quatro fases claras — Solicitação/Briefing → Cotação e comparação → Proposta e aprovação → Planejamento e execução. O produto precisa preservar etapas internas mais granulares, como RFQ e sourcing, sem poluir a mensagem pública.
5. **Veja a NEXO em ação**: mockup grande e fiel de interfaces reais, idealmente com abas/etapas que evidenciem briefing, matriz de fornecedores, orçamento e aprovação. Substituir renderizações conceituais por screenshots reais assim que existirem.
6. **Confiança e credibilidade (perto do fim)**: incluir marcas, case e depoimentos apenas com autorização e informação comprovável. Se ainda não houver prova social, substituir por conteúdo factual, como processos, controles e segurança, sem fabricar métricas ou endossos.
7. **CTA final + rodapé**: convite para demonstração, acesso ao sistema, contato, páginas legais e principais categorias.

## Copywriting de referência (a validar na implementação)

**Eyebrow:** GESTÃO DE EVENTOS E GRUPOS CORPORATIVOS  
**Título principal:** Da solicitação à execução do evento, em um só lugar.  
**Subtítulo:** A NEXO centraliza briefings, cotações, fornecedores e planejamento para transformar demandas corporativas em projetos mais organizados, transparentes e fáceis de acompanhar.  
**CTA primário:** Solicitar uma demonstração  
**CTA secundário:** Conheça a plataforma  
**Link de conta:** Entrar

**Módulos / título:** Tudo o que você precisa para planejar, cotar e acompanhar.  
**Benefícios / título:** Mais controle, eficiência e economia para o seu time.  
**Fluxo / título:** Do briefing à aprovação, com tudo conectado.  
**Demonstrativo / título:** Conheça a operação por dentro.  
**CTA final / título:** Sua próxima operação começa com mais clareza.

Notas: “execução” é visão de produto e posicionamento; a Alpha técnica não implementa ainda toda a operação de pós-evento. Não apresentar como funcionalidade já entregue algo que esteja apenas no roadmap. Evitar números absolutos de economia/tempo sem estudo e evitar citar clientes que não são reais.

## Navegação proposta

**Produto** (Funcionalidades, Como funciona, Plataforma) | **Soluções** (Agências e organizadores, Empresas, Grupos, Eventos) | **Sobre** | **Entrar** | **Solicitar demo**.  
Não exibir “Planos”, “Carreiras”, “Integrações” ou “Central de ajuda” como páginas funcionais antes de existirem; podem ser adicionadas quando houver conteúdo real.

## Comportamento e acessibilidade

- CTA primário deve levar a um formulário real de contato/demonstração ou caminho integrado; secundário navega para seção interna.
- Login aponta para app com autenticação, nunca para link falso.
- Header com navegação acessível, menu mobile, foco visível, áreas de clique generosas.
- Alternância coerente de seções claras/escuras; sem carrosséis automáticos ou animações invasivas.
- Respeitar `prefers-reduced-motion`, contraste WCAG AA, textos legíveis e sem texto inserido dentro de imagens como implementação final.
- Fotografia autoral/licenciada e assets otimizados, responsivos (AVIF/WebP), lazy-load abaixo da dobra; hero otimizado para LCP.
- Sem logotipos/nomes de empresas de terceiros usados como endosso sem autorização.

## Critérios de aceite visual

- A primeira dobra comunica o produto e sua proposta de valor em poucos segundos.
- A relação texto/fotografia/mockup no hero preserva sensação de amplitude e foco.
- Funcionalidades são fáceis de escanear, mas não dominam a página.
- A seção de benefícios está **no meio**, não na penúltima posição.
- Prova social (se houver) está **no final**, não após o hero.
- Sem dados, logotipos, depoimentos e métricas falsas na página publicada.
- Validar desktop 1440px e mobile 390px, com testes adicionais de tablet.

## Referência e origem

Inspiração de qualidade/organização: Perk. **Não copiar layout ou assets proprietários**, apenas o grau de acabamento, storytelling e usabilidade.

Material gerado por IA é **conceitual**: tipografia, números de dashboard, logos e CTAs nas imagens podem não corresponder à implementação e não devem ser tratados como dados reais. O brandbook definitivo da NEXO não foi confirmado neste ciclo; tokens abaixo são uma proposta para o visual aprovado, sujeitos a refinamento.