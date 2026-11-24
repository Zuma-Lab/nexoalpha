# NEXO ALPHA — Cronologia, decisões e status

Data de referência: **23/11/2026**. Esta cronologia **resume** os acontecimentos; não é transcrição literal das respostas.

## Recuperação e recomeço

- O usuário perguntou sobre acesso a conversas antigas. Foi explicado que há contexto/memórias e arquivos, não garantia de transcrição integral.
- O usuário decidiu **recriar NEXO do zero**, reaproveitando **conceitos, processos e regras de negócio**, mas sem usar o layout/código anteriores como base obrigatória. Preservar projeto anterior.
- Foram recuperados documentos da Biblioteca, em especial *Nexo — Mapeamento competitivo e desenho do motor de cotações MICE*, com foco em briefing, RFQ, fornecedores, comparação, orçamento, proposta e aprovação. A referência a Qondor/Perk é conceitual, sem direitos de cópia de telas/marca.
- Identificado repositório antigo `Zuma-Lab/nexo`. Criada a branch `nexo-alpha` nesse repositório em 23/11, mas o usuário **depois criou repositório novo `Zuma-Lab/nexoalpha`**, que deve ser a fonte oficial para a reconstrução. Não alterar `Zuma-Lab/nexo`.

## Homepage e identidade

- Usuário solicitou homepage comercial e institucional de alto padrão semelhante à percepção premium de Perk, sem copiar a identidade.
- **Imagem A** (primeira prévia): hero com executivo diante de skyline ao entardecer, mockup de dashboard NEXO à direita, logo laranja/branco, tipografia clara, grafite, acento laranja e seções claras. Usuário disse que **amou** cores, layout e o homem olhando a cidade.
- **Imagem B** (refino): adicionou seções, depoimento e maior densidade. Usuário preferiu a **A por ser mais clean**; logos de empresas e prova social só no fim; benefícios “Mais controle, eficiência e economia...” no meio da página.
- **Imagem C** (comparativo): hero com executivo sentado, painel à direita, benefícios e módulos. Usuário marcou hero em marrom e seções abaixo em vermelho e confirmou o princípio de **rolagem vertical**: no primeiro viewport deve aparecer prioritariamente hero; as demais seções surgem **ao rolar**, com distâncias maiores.
- As seções recomendadas: hero; plataforma/módulos; benefícios; como funciona; tela em ação; prova social **somente com clientes reais**; CTA final/footer. Os logotipos de marcas reais nas imagens geradas são **ilustrativos, não endossos**.
- Usuário aprovou conceitualmente **ícone angular laranja + “nexo” em letras minúsculas brancas**, em fundo escuro, e solicitou imagem em alta definição. A imagem HD foi gerada; ainda não é um SVG/código de marca vetorial validado.

## Skills / referências

- `interfaces-that-feel` (owl-listener): estado emocional, microinteração e mensagens por estado.
- `parallel-concepts` (owl-listener): propostas que diferem em comportamento, não apenas estética; teste de conceitos paralelos.
- `gpt-taste` (Leonxlnx): referências de composição, hierarquia e movimento; a skill foi movida para `taste-skill-classics`.
- A leitura e o registro destas referências **não equivalem à instalação global** no ChatGPT. Um pacote portátil foi preparado; nenhuma alteração na interface aprovada foi autorizada pelo simples registro das skills.
- Teste visual subsequente gerou imagens internas de briefing guiado (passos, cards de tipo de evento) e briefing inteligente (dados pré-preenchidos, confirmação). **São conceitos, não funcionalidades garantidamente implementadas.**

## Código e continuidade

- Um pacote `NEXO_ALPHA_HANDOFF_2026-11-23.zip` da Biblioteca contém backend Python, frontend estático, testes, documentação, imagens originais e instruções Work. É um **instantâneo preexistente** distinto dos mockups posteriores.
- Foram reportados três testes automatizados aprovados anteriormente; **o código transferido precisa ser validado novamente** no novo ambiente antes de presumir prontidão.
- Criada pasta persistente `/NEXO/ALPHA` na Biblioteca com especificação da homepage, design system, plano de implementação, decisões, pacote de código e referências visuais.
- Tentativas de transferência automática para Work não foram concluídas. O presente repositório novo é a base independente do projeto.

## Próximos passos com autorização

1. Conferir inventário dos arquivos, repositório e integridade dos assets.
2. Formalizar brand assets reais a partir do logo aprovado; vetorização deve ser conferida visualmente.
3. Implementar homepage responsiva real, seguindo arte aprovada, com conteúdo legítimo e sem clientes/depoimentos fictícios.
4. Implementar/testar os fluxos de negócio de ponta a ponta, sem alterar o repositório anterior.
5. Adicionar exportação oficial de conversa caso usuário forneça; não chamar resumo de transcrição integral.