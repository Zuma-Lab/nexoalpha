# NEXO Homepage v1

Site estático independente. Fonte em `dist/`. Não altera o repositório legado.

## Prévia local

Execute `python -m http.server 4173 --directory dist` e abra http://127.0.0.1:4173.

## Escopo

Homepage responsiva, hero fotográfico, dashboard ilustrativo em HTML, módulos, fluxo com abas, conceitos de briefing com ampliação, menu mobile, modal de acesso ainda não conectado e movimento reduzido.

Não contém autenticação, envio de leads, clientes fictícios ou métricas apresentadas como reais. O painel tem dados demonstrativos. As imagens de briefing são conceitos de design, identificados na interface.

## Identidade e fontes

Paleta e logo: Brandbook NEXO v1 e reconstrução vetorial da marca. Referências 01, 05 e 06 de Zuma-Lab/nexoalpha, commit 7dfa55bc2c477912254fcf56f8687f4477544219. Fonte local Inter quando disponível; fallback Arial. Nenhuma requisição de fonte externa.

Hero criado com a ferramenta nativa ImageGen: fotografia cinematográfica horizontal de executivo de costas em escritório grafite diante da cidade ao pôr do sol; espaço negativo à esquerda e à direita; luz âmbar; sem texto, marca ou interface. Prompt integral em `image-prompt.txt`.

O layout usa HTML e CSS reais. A imagem de referência completa não é usada como homepage.

## Hero v2
Composição corrigida a partir da referência 03: executivo sentado e parcialmente enquadrado, painel nivelado à direita e reflexo decorativo sem interação. Verificado em desktop e 390 px, sem rolagem horizontal. O reflexo é oculto no mobile e excluído da árvore de acessibilidade.
