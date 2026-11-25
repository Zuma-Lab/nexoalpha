# Governança do produto — NEXO Alpha

**Marco de referência:** 2026-11-23 (America/Sao_Paulo).  
**Escopo:** repositório `Zuma-Lab/nexoalpha`; o legado `Zuma-Lab/nexo` permanece intocado.  
**Nome:** **NEXO Alpha é provisório**. A marca definitiva e o domínio ainda não estão decididos.

## Fonte única para continuar em outro computador

1. [Padrões e regras](PADROES_E_REGRAS.md) — requisitos normativos com identificador, status, data e motivo.
2. [Decisões e alternativas](DECISOES_ARQUITETURAIS.md) — decisões tomadas e aquelas que ainda exigem aprovação.
3. [Registro cronológico](REGISTRO_DE_ALTERACOES.md) — mudanças da execução, arquivo/PR, motivo e data.
4. [Roadmap completo](ROADMAP.md) — começo, meio, fim, marcos, dependências e critérios de aceite.
5. [Pendências e riscos](PENDENCIAS_E_RISCOS.md) — prioridades, proprietário de decisão e bloqueios.
6. [Processo de versionamento](CONTRIBUICAO_E_VERSIONAMENTO.md) — como alterar o projeto sem perder rastreabilidade.
7. [Brandbook v2.1](../design/brandbook-v2/BRANDBOOK_V2.md) e [tokens canônicos](../design/brandbook-v2/nexo-tokens.json).
8. [Pesquisa e mensagens de dor na homepage (24/11/2026)](PESQUISA_DORES_E_MENSAGEM_HOME_2026-11-24.md) — fontes de mercado, dores qualitativas, exemplos, copy e limites funcionais.
9. [Guia Editorial e Controle de Mudanças](GUIA_EDITORIAL_E_APROVACAO_HOMEPAGE.md) — limites de escopo, controle de densidade e ritmo, status de aprovação e checklist antes de editar a homepage.
10. [Auditoria crítica pós-reformulação (24/11/2026)](AUDITORIA_CRITICA_POS_REFORMULACAO_2026-11-24.md) — notas comparativas, evidências reais, limitações e pendências.

**Hierarquia:** decisões expressas pelo proprietário > ADR vigente > regras do produto > brandbook/tokens vigentes > código validado > documentos históricos. Nenhum resumo equivale a uma transcrição integral. Sempre confrontar regras com o código e a CI.

## Interpretação de status

- **Decidido:** orientação confirmada; não equivale a implementação.
- **Implementado em branch:** código existe na branch de PR; ainda não está em `main`/produção.
- **Validado:** testes automáticos ou inspeção indicada na evidência.
- **Pendente:** depende de desenvolvimento, homologação ou escolha.
- **Substituído:** manter histórico e apontar substituto.

## Registro obrigatório de alterações

Cada mudança relevante deve registrar ID, descrição, data local (AAAA-MM-DD), motivo, arquivos impactados, status, evidência/PR, risco e alternativa considerada quando houver. Incluir também o resultado dos testes. Não reescrever o histórico de decisões; adicionar um novo registro que substitua o anterior.

**Criado:** 2026-11-23. **Última verificação da estrutura:** 2026-11-24.
