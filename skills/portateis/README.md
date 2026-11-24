# Três skills de design — fontes prontas para ambiente de desenvolvimento

Este pacote contém cópias de `SKILL.md` obtidas do GitHub em 23/11/2026, para referência e eventual instalação em um agente compatível. Não altera o código da NEXO nem o design aprovado. Esta entrega NÃO instala as skills globalmente no ChatGPT nem no computador do usuário.

## Fontes

1. [interfaces-that-feel](https://github.com/owl-listener/designer-skills/blob/9a6930cf84a822eb458624bd11c61aac5bbdf224/interaction-design/skills/interfaces-that-feel/SKILL.md) — referência fixada no commit `9a6930cf84a822eb458624bd11c61aac5bbdf224`.
2. [parallel-concepts](https://github.com/owl-listener/designer-skills/blob/9a6930cf84a822eb458624bd11c61aac5bbdf224/prototyping-testing/skills/parallel-concepts/SKILL.md) — referência fixada no mesmo commit.
3. [gpt-taste](https://github.com/Leonxlnx/taste-skill-classics/blob/main/skills/gpt-tasteskill/SKILL.md) — a skill foi movida de `taste-skill` para `taste-skill-classics`; arquivo consultado no GitHub com blob SHA `c9a72395c9024d4d2398238f0d8b37495228fb7d`.

## Instalação pelo terminal de um agente compatível

Use em seu computador ou no ambiente com acesso ao GitHub:

```bash
npx skills add https://github.com/owl-listener/designer-skills --skill interfaces-that-feel
npx skills add https://github.com/owl-listener/designer-skills --skill parallel-concepts
npx skills add https://github.com/Leonxlnx/taste-skill-classics --skill gpt-taste
```

O `npx` pode pedir confirmação de instalação do executor. Antes de executar código de terceiros, revise o repositório e suas dependências. Para selecionar o agente ou escopo, consulte `npx skills add --help`.

## Instalação manual alternativa

Copie as três pastas com `SKILL.md` deste pacote para o diretório de skills do agente indicado na documentação do seu ambiente. Reinicie a sessão se o agente exigir. Isso não ativa automaticamente essas skills na conta do ChatGPT.

## Regra NEXO

Ao consultar as skills para o produto NEXO, preservar as decisões de interface já aprovadas. São recursos opcionais de design, não autorização para redesenhar ou editar o projeto existente.