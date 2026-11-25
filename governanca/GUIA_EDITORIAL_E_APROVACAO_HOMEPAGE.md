# Guia editorial e controle de mudanças — Homepage NEXO Alpha

**Registro:** 2026-11-24 · America/Sao_Paulo  
**Status:** princípios de preservação do layout/identidade já confirmados; recomendações de redução de densidade **propostas, aguardando aprovação**.  
**Referências:** `PADROES_E_REGRAS.md`, `DECISOES_ARQUITETURAIS.md`, `design/brandbook-v2/`, `homepage/dist/` e `governanca/PESQUISA_DORES_E_MENSAGEM_HOME_2026-11-24.md`.

## 1. Invariantes já confirmadas pelo proprietário (não negociar silenciosamente)

1. **Não mudar layout, paleta, tipografia, logotipo, espaçamentos ou estrutura** quando o pedido for apenas de copy, mensagem, análise ou pesquisa. Uma aprovação de texto **não autoriza** inserir nova seção.
2. Manter a direção aprovada do brandbook **2.1**: grafite `#111315`, laranja `#FF850D`, off-white `#F3EFE9`, Inter e componentes atuais. Referência técnica canônica: `design/brandbook-v2/nexo-tokens.json`.
3. Rascunho por geração de imagem **não é screenshot nem aprovação de uma nova identidade**. Identificar claramente como conceito. Não usar elementos sintéticos como se fossem recursos já existentes da interface.
4. Reusar as **três imagens originais fornecidas** (sistema, briefing, pessoa + sistema), após verificá-las no próprio arquivo e avaliar legibilidade e direitos de uso. Não substituí-las por imagens geradas ou reconstruídas sem pedido específico.
5. Para mudança de layout: apresentar diff/preview e marcar os itens como **proposta sujeita a aprovação**; só depois alterar HTML/CSS da homepage.
6. Qualquer decisão nova precisa de ADR/BR/CHG datados; **registro de proposta não equivale a aceite**. Preservar código do NEXO legado e não realizar merge/deploy sem aprovação explícita.

## 2. Diagnóstico da crítica visual — rascunhos, não produção

**Observação do proprietário:** composição de cores e tipografia agradou, mas os rascunhos ficaram “carregados de informação, muito texto”.  
**Leitura editorial:** problema prioritário é **densidade e ritmo**, não identidade. Três títulos grandes, três parágrafos de dor e três imagens de grande porte acabam competindo entre si. A versão mobile tende a comprimir a mesma quantidade de conteúdo numa área menor.

**Não confundir:** essa crítica refere-se às prévias visuais geradas na conversa; elas não são a homepage HTML já aprovada, nem capturas de novas telas implementadas.

## 3. Tratamento editorial proposto (ainda NÃO autorizado para implementação)

### Hero / primeira dobra
- Papel: reconhecer uma dor principal e indicar o produto sem esgotar a explicação.
- Sugestão de título A: **“O evento é um só. A informação não deveria estar em tantos lugares.”** (copy ainda sujeita a aprovação final).
- Uma frase de apoio com e-mails/planilhas/versões, preferencialmente curta; usar voz corporativa e linguagem concreta.
- Apenas um CTA primário em destaque; CTA secundário discreto se tiver destino real.
- Preferir imagem **02 — sistema** como prova visual, desde que a imagem seja legível e se integre ao layout existente.
- **Não inserir imagem ou deslocar colunas no hero existente sem autorização de layout.**

### Primeira rolagem
- Papel: mostrar o custo operacional e a consequência de uma alteração, sem repetir a explicação do hero.
- Título B sugerido: **“Sua equipe precisa conduzir eventos. Não reconstruir informações.”**
- Texto de apoio curto, direcionado ao que mudou, ao que permanece válido e à próxima ação.
- Preferir imagem **03 — briefing** e comparação V1/V2 **se a composição real comportar**, sem entulhar com cards de efeito ou dados não demonstrados.
- Manter a seção V1/V2 existente como padrão até aprovação de nova distribuição.

### Demais seções
- Tratar um benefício/decisão por vez: contexto comercial, cotação, visibilidade, prova funcional e CTA.
- Imagem **01 — pessoa + sistema** é opcional e secundária; incluí-la apenas se melhorar o ritmo visual; caso contrário, reservá-la para peça institucional.
- Não repetir os mesmos conceitos (“fragmentação”, “tudo em um lugar”, “histórico”) com palavras diferentes em todas as seções.
- Usar conteúdo detalhado nas áreas adequadas, sem esconder regras importantes do produto.

## 4. Testes de revisão de copy (heurísticas, NÃO limites rígidos)

1. **Teste da leitura de 5 segundos:** sem rolar, é possível entender a dor e o que o produto organiza?
2. **Teste de redundância:** cada seção acrescenta informação nova ou repete a anterior?
3. **Teste de escaneabilidade:** título, frase principal, imagem e ação têm hierarquia clara; ninguém precisa ler parágrafo inteiro para prosseguir.
4. **Teste de imagem:** a imagem comprova algo? Se removida, perderíamos informação importante? Se não, pode sair.
5. **Teste mobile:** texto não compete com mockups, comparação e CTAs; incluir margens de respiro, legibilidade, foco, sem cortar colunas essenciais.
6. **Teste de precisão:** não prometer integração automática, envio de e-mails, ROI ou funções não implementadas. Diferenciar conceito, funcionalidade em desenvolvimento e homologação.
7. **Teste visual comparativo:** preservar screenshot **antes/depois** 1440px e 390px, comparar mesmas áreas e documentar redução de ruído sem mudança inadvertida de cor/estrutura.
8. **Teste de público:** apresentar a copy a consultor e gestor para validar se ambos reconhecem a dor, sem induzir resposta.

**Hipótese a testar, não regra aprovada:** reduzir aproximadamente 30–50% da copy de apoio das primeiras dobras dos rascunhos. Preservar conteúdo necessário para decisão e obrigações de privacidade.

## 5. Gate de aprovação por tipo de mudança

| Pedido | Pode executar sem aprovar novo layout? | O que deve permanecer intacto |
|---|---|---|
| Corrigir/melhorar copy | **Sim, apenas texto explicitamente solicitado** | HTML estrutural, CSS, cores, fontes, posições e imagens |
| Revisão crítica e estratégia | **Sim, como análise ou documentação** | Não alterar runtime da homepage |
| Rascunho visual | **Sim, como conceito identificado** | Não confundir com código/captura nem substituir imagens originais |
| Inserir/reordenar imagens, redimensionar, mover seções | **Não. Apresentar proposta e obter aceite.** | Identidade e elementos aprovados até decisão |
| Trocar cor, fonte, marca, logotipo ou layout | **Não. Exige pedido ou aprovação expressa.** | Todos os tokens atuais |
| Integrar ferramentas externas / afirmar automações | **Não sem escopo e testes reais.** | Limites das capacidades do Alpha |

## 6. Evidência mínima em PR

- Escrever: **pedido original → arquivos autorizados → o que foi alterado → o que NÃO foi alterado**.
- Registrar IDs BR/ADR/CHG, data local, motivo, status aprovado/proposto, testes e links das imagens reais.
- Se a modificação afetar apenas copy, verificar que `styles.css` e tokens **não foram modificados**.
- Se houver alteração visual autorizada, comparar telas antes/depois e validar desktop/mobile.
- Não dar como “feito” um rascunho de imagem, um experimento ou uma regra que ainda aguarda aprovação.

## 7. Situação atual

**Confirmado:** a identidade de trabalho existente é preservada e o proprietário rejeitou mudanças visuais não solicitadas (rollback anterior documentado em CHG-035).  
**Proposto, ainda sem aceite de implementação:** simplificação das três primeiras dobras, títulos A e B, protagonismo da imagem 02, imagem 03 e uso opcional da imagem 01.  
**Próximo passo recomendado:** revisar a proposta de copy com o proprietário, montar prévia fiel às imagens originais, obter aceite específico da distribuição e só então alterar o runtime na branch PR #1.

Este documento deve ser lido antes de qualquer nova alteração de conteúdo/visual de `homepage/dist/`.
