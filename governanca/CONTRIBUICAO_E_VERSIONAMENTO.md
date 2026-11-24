# Contribuição, revisão e governança de alterações

**Criado em:** 2026-11-23 · **Última modificação:** 2026-11-23.

## Fluxo obrigatório

1. Ler `governanca/README.md`, ADRs, padrões e roadmap antes de editar.
2. Criar branch de trabalho a partir de `main` ou seguir a branch de revisão já aberta; não alterar `Zuma-Lab/nexo`.
3. Identificar IDs de regra afetados e registrar alterações em `REGISTRO_DE_ALTERACOES.md` com **data local**, motivo, risco e link/commit.
4. Atualizar o documento canônico (tokens, API/arquitetura, testes) e incrementar versão relevante; não apagar regras antigas sem ADR substitutivo.
5. Rodar `python -m pytest`, verificações de sintaxe, QA visual e segurança conforme escopo. Não declarar teste sem evidência.
6. Gerar capturas a partir da aplicação real e brandbook PDF a partir do gerador versionado; registrar commit e viewport.
7. Abrir PR com checklist, riscos, pendências e rollback; exigir revisão antes de merge.
8. Manter nome/domínio provisional até decisão explícita do proprietário.

## Versionamento de artefatos

- **Brandbook:** `design/brandbook-vN/`; v1 histórica, v2 atual. Nenhum PDF editado manualmente sem atualizar gerador e Markdown.
- **Regras e ADR:** IDs estáveis `BR-###`, `ADR-###`, com data e status. Substituição cria novo registro e remissão.
- **Changelog:** entradas em ordem cronológica reversa, cada uma com data, arquivos e validação.
- **Screenshots:** `evidencias/capturas/` com nomes estáveis e metadados do commit, sem dados reais.
- **Roadmap:** versão atual e atualização sempre que marco ou escopo mudar.

## Restrição de acesso e privacidade

O repositório está público. Não versionar senhas, segredos, dados pessoais, transcrições de chat ou nomes de clientes reais. Remover um arquivo do HEAD **não remove seu histórico**; limpeza histórica requer estratégia aprovada em separado. Limitar o acesso e o uso dos dados de demonstração a ambientes locais. Se o produto for renomeado, preservar rastreabilidade da marca anterior no ADR e no roadmap.

## Checklist do PR

- [ ] Sem mudanças no NEXO legado
- [ ] Regras/ADRs e changelog atualizados com data
- [ ] Identidade e tokens canônicos usados
- [ ] Sem dados pessoais ou credenciais
- [ ] Testes automáticos passaram
- [ ] Capturas reais verificadas; exemplos rotulados
- [ ] Dependências externas registradas
- [ ] Critérios de aceite e rollback documentados
