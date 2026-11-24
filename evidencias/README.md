# Evidências visuais e de validação

**Criado em:** 2026-11-23 (America/Sao_Paulo). Os artefatos são gerados a partir do **código real da branch** usando Chromium/Playwright e a API FastAPI local.

- [Galeria da homepage (desktop e mobile)](capturas/README.md)
- [Manifesto das capturas](capturas/manifest.json) com data de execução UTC, commit, viewport e verificação de overflow
- [Brandbook v2 PDF](../design/brandbook-v2/NEXO-Alpha-Brandbook-v2.pdf)
- [Fonte do brandbook](../design/brandbook-v2/BRANDBOOK_V2.md)
- [CI de testes](../.github/workflows/alpha-ci.yml)

**Limite da evidência:** screenshots mostram HTML/CSS renderizados com dados de exemplo, não provam funcionalidade de ponta a ponta ou conformidade WCAG. O aplicativo interno `alpha-snapshot` ainda aguarda remodelagem.

**Regra:** ao alterar homepage, componentes visuais ou brandbook, regenerar capturas/PDF e atualizar o registro de alterações. Não manter screenshot de versão anterior rotulado como atual.
