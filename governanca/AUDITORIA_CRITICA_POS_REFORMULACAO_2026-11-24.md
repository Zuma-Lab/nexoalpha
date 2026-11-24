# Auditoria crítica pós-reformulação — NEXO Alpha

**Data:** 2026-11-24 (America/Sao_Paulo)  
**Natureza:** análise editorial crítica de UX e produto baseada em **código da PR #1 + 14 screenshots reais Chromium**. Não é certificação WCAG, pentest ou pesquisa com usuários.  
**Escopo:** homepage Direção B, workspace V2, briefings/versionamento, RFQ, cotação, proposta e governança. O nome NEXO Alpha é provisório.

## Sumário executivo

**Melhorou de modo substancial**: a home não depende mais do hero "título à esquerda + mockup à direita", o negócio é demonstrado por impacto V1/V2, a cotação apresenta cálculo por room nights e políticas, permissões foram explicadas em matriz, e o workspace abandonou o CSS azul antigo e usa o projeto como unidade de trabalho. As telas novas foram testadas em navegador com login e persistência de uma mudança real (participantes 120→130).

**Ainda não está pronto para lançamento nem encerrou o risco de interface genérica.** A fila do workspace tem muito espaço vazio com só um projeto e colunas laterais explicativas; a aplicação atual está num único arquivo JS extenso; faltam unidades financeiras tipadas (apartamentos × noites), comparação de escopos completos, automação auditável do impacto de revisão e QA especializado. Não transformar "código implementado" em alegação de funcionalidade homologada.

## Antes × depois (notas críticas subjetivas)

| Critério | Auditoria anterior | Após refatoração | Mudança observada | Limite |
|---|---:|---:|---|---|
| Clareza da proposta | 7/10 | 8/10 | Texto e caso concretos substituem slogans amplos. | Copy precisa ser testada com clientes. |
| Identidade visual própria | 4/10 | 7/10 | Estrutura editorial assimétrica, densidade e composição mais ligadas à operação. | Logo e tipografia não são exclusivos; refinamento autoral possível. |
| Profundidade demonstrada | 3/10 | 6/10 | V2 real, grade financeira, RFQ e proposta com conteúdo. | Regra de negócio de room nights e incidência tributária ainda parcial. |
| Consistência home/workspace | 2/10 | 8/10 | Ambos usam grafite, laranja restrito, off-white e Inter; workspace não carrega CSS legado. | Diferenças de componentes ainda exigem uma biblioteca compartilhada. |

> Notas são **avaliação editorial**, não métricas de satisfação ou pontuações objetivas.

## Análise visual real

### Homepage B — pontos fortes

- Hero “O briefing mudou. A operação continua.” e lista de três princípios são mais específicos do que “uma única trilha”.
- Caso de uso apresenta V1→V2, escopo afetado e ação subsequente; a indicação de *exemplo ilustrativo* é visível.
- Finanças explicam `105 apartamentos × 3 diárias = 315 room nights`, comparando Hotel A/B/C e café com totais coerentes nos exemplos. A diferença entre NET e preço de venda é reconhecida.
- Matriz de acessos ensina o isolamento de custos internos e respostas concorrentes sem três cartões promocionais idênticos.
- Mobile reordena o conteúdo em vez de cortar a tabela: leitura vertical e alternativas completas.
- Após a auditoria visual, corrigidos contraste de introdução na seção escura e texto de contato para não solicitar documentos confidenciais.

### Homepage B — problemas residuais

- Ainda usa layout editorial de coluna, Inter genérica, formulário padronizado e um logo provisório; coerência profissional aumentou, personalidade de marca ainda pode amadurecer.
- O bloco V1→V2 da home ainda é demonstração, **não** tela de automação de impacto funcional. Isso está rotulado, mas deve ser substituído por material real após implementado o impacto em RFQs e orçamento.
- Texto de cláusulas de dados e política LGPD não está formalizado; não implantar captação de lead em produção sem tratamento.
- Não houve teste humano de conversão, SEO público, mobile real, múltiplos navegadores e WCAG completo.

### Workspace V2 — pontos fortes

- Saiu o azul `#4068D6`/DM Sans/Manrope do frontend histórico; grafite + superfícies claras permitem uso intensivo.
- Fila e projeto têm ações coerentes, com separação de briefings, RFQs, cotação, propostas e execução **dentro de um mesmo contexto**.
- Wizard de 4 etapas usa validação condicional do servidor, cria versão imutável e suporta rascunho privado recuperável.
- Propostas permitem texto de apresentação e condições no snapshot imutável; links públicos omitem custos NET, taxas e fee.
- Screenshot de 2026-11-24 mostra comparação real de **participantes 120→130** após V2 gravada; não somente uma tabela cenográfica.
- Após inspeção, removido botão de menu mobile do desktop e tabs mobile organizadas em 2 × 3 sem esconder seções.

### Workspace V2 — problemas residuais

- Em fila com poucos registros, a coluna esquerda fica visualmente vazia, enquanto a lateral acumula textos de orientação e indicadores. Rever estados de operação inicial e melhor preencher com atividades úteis, sem métricas fictícias.
- Os textos explicativos repetem conceitos como versão, persistência e link manual. Reduzir redundância conforme novas tarefas ativas tornarem o sistema autoexplicativo.
- O wizard é funcional, mas a gestão de erros por campo, anexos, duplicação controlada e navegação antes/depois precisa de ensaio com operadores reais.
- A grade financeira aceita quantidade genérica, NET unitário e porcentagens, mas falta modelo tipado de unidade e auditoria **apartamentos × diárias × tarifa** por serviço. Isso é um requisito P0 de negócio, não só estética.
- O arquivo `workspace-v2/app.js` concentra muitos módulos em um único arquivo. Para manutenção profissional, dividir em domínio, API/estado, componentes e fluxos, preservando testes. Evitar reescrita desnecessária.
- Acessibilidade é alvo WCAG 2.2 AA, **não auditada** com leitor de tela; 390px e 1440px são evidências, não cobertura de todas as telas e contextos.
- As permissões dependem do servidor; revisão completa de segregação multitenant, logs/segredos, migrações, concorrência e testes E2E de RFQ→cliente permanece bloqueante.

## Priorização das pendências, por gravidade

| Fila | Tipo | Problema | Próxima ação concreta | Critério de aceite |
|---|---|---|---|---|
| P0 | Negócio | Quantidade/diária/unidade são genéricas no orçamento. | Modelar unidade de serviço, room nights, ocupação, multiplicadores e incidência por contrato. | 105×3×tarifa consistente, idêntico na API, editor, comparativo e snapshot. |
| P0 | Segurança | Produto com dados persistentes e links públicos sem pentest/QA abrangente. | Revisar tenancy, CSRF, links, logs, concorrência, infraestrutura. | Testes cruzados e revisão especializada aprovados. |
| P0 | Jornada | Mudança de briefing não produz mapa automatizado de fornecedores/itens afetados. | Gerar diff por serviço e checklist vinculado ao lote de RFQ. | V1/V2 identifica mudanças, efeitos e reenvios sem perda do histórico. |
| P0 | Cotação | Comparativo comercial não normaliza plenamente tarifa, café, tributos, disponibilidade, cancelamento. | Harmonização de fornecedores por serviços/unidades e auditoria de custo total. | Alternativas reproduzíveis e critérios de escolha documentados. |
| P1 | Produto | Propostas ainda não têm editor avançado de cláusulas/anexos/templates. | Editar conteúdo estruturado, anexos e layout imprimível/PDF, mantendo snapshots. | Proposta profissional validada com usuários e políticas. |
| P1 | UX | Fila com baixa densidade de registros é vazia; explicações repetitivas. | Estado inicial de onboarding, atividades e pendências reais; teste de uso. | Usuário sabe a próxima ação sem leitura redundante. |
| P1 | Engenharia | JS monolítico de interface. | Separar módulos e componentes reutilizáveis com testes. | Testes e navegação preservados após modularização. |
| P1 | Marketing | Marca/nome/dominio/SEO/LGPD/CRM pendentes. | Decisão de naming, política e notificações; fonte hospedada localmente. | Go-live só com checklist formal. |
| P1 | Qualidade | Não há validação manual cross-browser, leitores de tela, zoom e contraste AA completa. | Testar fluxos desktop/mobile, teclado e zoom 200%. | Evidência WCAG/QA registrada. |
| P2 | Expansão | Integrações/Excel avançado, portal completo, analytics. | Iterar após ciclo ponta a ponta robusto. | Backlog baseado em demanda e métricas reais. |

## Evidência técnica verificável

- PR #1: https://github.com/Zuma-Lab/nexoalpha/pull/1
- Capturas e manifesto: `evidencias/capturas/README.md`, `manifest.json` (14 PNGs, 1440×960 e 390×844, sem overflow lateral externo).
- CI Python/JS/governança: execução em verde após refactor (42 testes Python, 1 aviso conhecido de depreciação).
- Pipeline visual Chromium: 14 imagens reais, login de demonstração, alteração 120→130 e brandbook PDF regenerado (10 páginas).
- Arquivos de produto: `homepage/dist/`, `alpha-snapshot/workspace-v2/`, `alpha-snapshot/backend/`, `design/brandbook-v2/`.
- `alpha-snapshot/frontend/` preservado em Git mas **não servido em `/app`**.

## Veredito e limites

**Homepage:** apropriada como direção de marca em revisão; não anunciar como site aprovado para produção. Visualmente mais distintiva que a v1, mas ainda depende de identidade final e prova do produto real.

**Workspace:** um MVP operacional real em desenvolvimento, com navegação e interfaces próprias; **não** uma cópia visual do frontend antigo. Ainda precisa transformar lógica comercial profunda em modelo transacional robusto e reduzir código monolítico antes de operação em escala.

**Não mesclar ou publicar automaticamente**. Revisar a PR com o proprietário, depois fechar gates P0 e P1 com evidências.

**Atualizado em 2026-11-24.** Critérios e roadmap detalhados em `governanca/ROADMAP.md`.
