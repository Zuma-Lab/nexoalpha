# Proposta de próximas telas — NEXO Alpha
**Data:** 2026-11-25 · **Estado:** proposta de design para aprovação, **não implementada** · **Referência:** brandbook 2.1.

## Base visual inspecionada
- `assets/visuals/05-briefing-etapas-exploratorio.webp`: workspace de fundo escuro, sidebar grafite com logotipo angular, navegação Início/Briefings/Cotações/Planejamento/Fornecedores/Projetos/Relatórios; stepper horizontal de cinco etapas (Objetivo, Detalhes, Público, Logística, Resumo), cards de objetivo e CTA laranja.
- `assets/visuals/06-briefing-inteligente-exploratorio.webp`: mesma base escura e laranja; stepper em três etapas (Confirmar informações, Detalhar necessidades, Revisar e enviar), painel de evento com tabela de campos e ações editar/confirmar, fundo arquitetônico geométrico. O texto “preenchido com base no seu histórico” é **conceitual**, não comprovação de autofill inteligente na API atual.
- `assets/visuals/01-homepage-primeira-aprovada.webp`: composição editorial escuro/off-white/laranja; imagem de interface; contém logos de terceiros e afirmações de clientes que **não devem** ser tratadas como provas reais.
- Capturas reais em `evidencias/capturas/workspace-fila-desktop.png`, `workspace-briefing-desktop.png`, `workspace-cotacao-desktop.png`: app atual utiliza sidebar grafite, superfície operacional creme, Inter, cards claros e formulário de briefing em **quatro passos** (Evento, Serviços, Especificações, Revisão).
- Diferenciação obrigatória: referências acima são **mockups exploratórios**; capturas do workspace são **código real da branch**, mas não homologação de produto. Não afirmar que o redesign escuro está pronto.

## Decisão proposta de direção (não aprovada)
**Manter uma linguagem operacional única, não obrigar todas as páginas a serem pretas.**
- Navegação lateral grafite, acentos laranja funcionais, Inter, ícones simples e linha/ritmo consistente.
- Superfícies de apresentação e etapas guiadas podem usar fundo grafite, enquanto matrizes/cálculos extensos podem permanecer em off-white para legibilidade; transição sem novos acentos de cor.
- O fundo geométrico laranja da imagem de briefing fica restrito à área de topo/ambientação, jamais atrás de números ou campos. Evitar “cara de IA” (glow em todos os cards, 5 CTAs, badges decorativos, frases vazias).
- Na mesma aplicação, componentes, raio, campos, densidade, navegação e status mantêm convenções repetíveis.
- **Conflito de stepper:** referência 05 mostra 5 etapas, referência 06 mostra 3; o código atual apresenta 4. **Não alterar o fluxo funcional só para copiar um mockup**; avaliar mapeamento antes de revisar o stepper. Proposta inicial: usar 4 etapas reais Evento → Serviços → Especificações → Revisão e adaptar a apresentação visual da referência escura, mantendo seus dados/validações.

## Fluxo principal sugerido
`Fila/Projetos` → `Projeto / Visão geral` → `Briefing por serviço` → `Histórico V1/V2` → `RFQs / Fornecedores` → `Comparativo e orçamento` → `Proposta V1/V2` → `Planejamento`.

| Tela | Mensagem e dados essenciais | Composição de referência | Estado funcional atual e dependências | Prioridade |
|---|---|---|---|---|
| **01. Projeto / Visão geral** | Título do evento, cliente, destino, período, participantes, serviços, responsável, status, versão ativa, RFQs em andamento, próxima ação | Sidebar fixa; cabeçalho editorial compacto; faixa com contexto; uma lista de decisões/tarefas e um resumo do histórico, sem painel decorativo | Projeto e fila V2 existentes; ajustar IA e hierarquia após revisar dados | P0 UX |
| **02. Histórico de briefing** | V1→V2, campos alterados, autor, data, escopos afetados, RFQs que usam cada versão, ação de gerar versão | Tabela/diff em duas colunas; laranja para diferenças, cinza para antigo; sem editar versão publicada | Snapshot e versões existem; impacto integral e reenvio automatizado ainda pendentes | P0 |
| **03. Fornecedores e RFQs** | Filtro por serviço/local; seleção de fornecedores; lote/versão de briefing, prazo, estado de cada pedido, resposta, link por token e condições | Área operacional de lista com filtros, tabela e painel lateral de detalhes; CTA primário “Criar lote de RFQs” | Cadastro, batches e respostas por token existem; envio por e-mail ainda manual; garantir estados honestos | P0 |
| **04. Cotação e comparativo** | Serviços e unidades (apartamentos × diárias), NET, impostos, fee, venda, cancelamento, café, disponibilidade, escopo equivalente | Matriz comparativa em tabela de alto contraste; resumo financeiro lateral/abaixo, sem caixas genéricas repetidas | Quantidade genérica e cálculo centavos/bps existem; itens tipados por serviço não concluídos | **P0 issue #4** |
| **05. Proposta comercial** | Serviços selecionados, valor de venda, apresentação, cláusulas, anexos, versão, prévia de cliente, publicação e decisão | Editor com estrutura de documento + painel de configuração; ação Publicar em etapa clara, preview fiel ao cliente | Versões e termos básicos existem; editor avançado/anexos faltam; NET nunca público | P0 |
| **06. Planejamento** | Entregas por serviço, responsáveis, prazos, status, histórico, tarefas decorrentes da aprovação | Lista/timeline de tarefas e calendário apenas se data/uso validar; evitar dashboards vazios | PlanTask básico existe; automações, relatórios e linha do tempo aprimorada pendentes | P1 |

## Primeiro conjunto de protótipos (sem alterar o código)
1. **Projeto / Visão geral — desktop 1440×960**, e depois mobile 390×844.
2. **Fornecedores e RFQs — desktop**, com escolha de serviço e estado do convite, sem alegar envio por e-mail.
3. **Cotação e comparativo — desktop**, com tabela financeira realista por unidade, cálculo verificável.
4. Apenas após validar as 3, projetar **Editor de propostas** e **Planejamento**.

A tela de briefing existente será a **âncora visual** (não precisa ser redesenhada já); é útil construir ao lado dela, comparar e extrair tokens/componentes, respeitando o estado de aprovação das imagens.

## Regras de uso e microcopy
- Uma ação principal por contexto. Estados: vazio, carregando, erro, sem acesso, concluído, link expirado. Não destacar como “enviado” RFQ sem entrega real.
- Evitar repetição de descrições; títulos operacionais nomeiam tarefa e objeto: “Cotação do evento”, “Comparar fornecedores”, “Revisar proposta”.
- Dados reais ou sintéticos coerentes; never usar logotipos de terceiros, depoimentos, métricas ou clientes reais sem autorização.
- Tabelas financeiras especificam a unidade e permitem rastrear valores; não inferir melhor fornecedor só por tarifa menor.
- UI acessível: contraste AA, foco visível, teclado, responsive real (não miniaturizar desktop), labels, alvos e status legíveis.

## Gate de aprovação e implementação
**Nesta etapa, apenas projeto de UX. Não alterar `homepage/`, `alpha-snapshot/workspace-v2/`, CSS ou tokens.**

Para cada tela futura: 1) wireframe/texto; 2) protótipo visual usando referências inspecionadas; 3) revisão com proprietário; 4) inventário de campos/estado e contrato API; 5) branch isolada; 6) implementação; 7) testes funcionais, permissões, capturas Chromium desktop/mobile; 8) PR draft, governança e aceite.

Links de dependências: [issue #2](https://github.com/Zuma-Lab/nexoalpha/issues/2), [issue #4](https://github.com/Zuma-Lab/nexoalpha/issues/4), [issue #5](https://github.com/Zuma-Lab/nexoalpha/issues/5), [Roadmap Work/Claude](../handoff/ROADMAP_WORK_CLAUDE_2026-11-25.md).
