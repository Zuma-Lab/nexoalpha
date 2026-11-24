# Homepage NEXO — Especificação para reconstruir as imagens em código

## Fonte da verdade e status

A imagem **A** foi a direção aprovada. A imagem **B** é uma exploração mais densa; **C** é um comparativo, e o usuário marcou na **C** que o hero deve ocupar a primeira dobra. A implementação no código ainda não corresponde necessariamente a essas imagens. Todas as imagens são **referências estáticas**, não código ou design system fiel exportado.

## Objetivo da página

Apresentar uma plataforma B2B para eventos, grupos, solicitações, cotações, planejamento e controle; gerar confiança e incentivar demonstração/acesso sem a aparência de template genérico. Público: gestores corporativos, organizadores, agências, consultores.

## 1 — Hero (primeiro viewport; prioridade máxima)

- Barra de navegação com símbolo + wordmark NEXO à esquerda; itens como Produto, Soluções, Recursos, Sobre; botão Entrar e CTA `Solicitar demonstração`. Não assumir planos/preços publicados até serem definidos.
- Plano de fundo com executivo contemplando o horizonte urbano ao entardecer, luz quente e composição em profundidade; contraste suficiente para texto branco.
- Cabeçalho conciso em 2–3 linhas **quando couber**: “Da solicitação à execução do evento, em um só lugar.” O trecho final é laranja.
- Subtexto: centralização de briefing, cotação, planejamento, fornecedores e acompanhamento em uma plataforma. Curto, sem promessas quantitativas não medidas.
- Primário: Solicitar uma demonstração. Secundário: Ver como funciona.
- À direita, mockup de interface realista da NEXO em grafite: sidebar com Início, Briefings, Cotações, Planejamento, Fornecedores, Projetos/Relatórios; indicadores e projetos recentes **somente como exemplo ilustrativo**.
- No desktop, foco em experiência editorial e respiro. Hero deve ocupar aproximadamente a altura disponível do navegador; conteúdo posterior **não precisa** caber na primeira tela.
- No celular: evitar texto sobreposto ao rosto e ao dashboard; stack vertical, tipografia adaptativa, imagem de fundo reposicionada, mockup dimensionado. Sem rolagem horizontal.

## 2 — Plataforma e funcionalidades

Seção clara com títulos curtos, 6 módulos distribuídos com bastante espaçamento (2×3 ou 3×2 conforme a largura): Briefings, Cotações, Planejamento, Fornecedores, Acessos & Times e Relatórios. Cards com ícones discretos, títulos legíveis, descrições de 1–2 linhas. Fornecedores e RFQs devem ser tratados no mesmo ecossistema, não como planilhas isoladas.

## 3 — Benefícios no meio

Colocar “Mais controle, eficiência e economia para o seu time” **no meio da rolagem**, preferencialmente com fotografia cinematográfica em tons quentes e ícones discretos. Benefícios: agilidade nas cotações; controle de custos; colaboração entre áreas. Não usar percentuais de economia sem validação.

## 4 — Como funciona

Explicar o ciclo sem excesso de texto: Solicitação/Briefing → Cotação/fornecedores → Planejamento/proposta → Aprovação/execução. A operação real inclui RFQs, retorno estruturado, matriz comparativa, planilha nativa, versões e trilha de auditoria; não simplificar a lógica interna para adequar a arte da landing.

## 5 — O produto em ação

Prévia maior do sistema/fluxo, com narrativa visual mais útil do que dezenas de cards. Pode destacar tela de cotação ou fluxo de briefing. Evitar usar dados demonstrativos como se fossem clientes/projetos reais.

## 6 — Prova social somente no final

“Empresas que confiam na NEXO” perto do fechamento **somente quando houver autorização e evidência real**. Antes disso, omitir logos e depoimentos de marcas/pessoas identificáveis presentes nas imagens geradas. É melhor usar mensagem sobre segurança, governança e processo do produto, com claims verificáveis.

## 7 — CTA final e rodapé

Chamada curta com contraste grafite/laranja: conhecer a plataforma/solicitar demonstração. Rodapé com Produto, Soluções, Recursos, Sobre, política e contato apenas quando canais e documentos forem definidos.

## Interação e acessibilidade

- Rolagem vertical normal; não empilhar três seções inteiras no mesmo viewport.
- Microanimações apenas quando ajudam a compreensão; `prefers-reduced-motion: reduce` deve neutralizar movimentos.
- CTAs reais: não criar botões sem destino funcional; enquanto não houver integração, rota ou aviso claramente provisório.
- Responsividade desktop/tablet/mobile e contraste.
- Não copiar layout, logo ou ilustrações da Perk; Perk e Qondor são referências de padrão de acabamento.

## Tipos de assets disponíveis

- Geração A — inspiração primária aprovada.
- Geração B — refino com densidade maior, não escolhida.
- Geração C — alternativa comparativa, imagem anotada pelo usuário.
- Duas imagens de briefing interno exploratório.
- Recorte de logo do usuário e logo de alta resolução gerado.

Confira `../assets/ASSETS_MANIFESTO.md` para correspondência entre nomes, status e acervo da Biblioteca.