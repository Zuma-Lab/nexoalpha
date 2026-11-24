# NEXO ALPHA — Plano de execução da homepage

**Próxima etapa imediata:** desenvolver uma landing HTML/CSS/JS (ou componentes na stack escolhida) responsiva, seguindo `HOMEPAGE_V1_APROVACOES.md` e `DESIGN_SYSTEM_V1.md` e tendo `assets/homepage/01-referencia-aprovada.png` como diretriz de composição.

## Prioridades por sequência

### Fase A — Fundação da página
- [ ] Confirmar a nomenclatura, as rotas públicas (`/`) e a rota autenticada (`/app` ou equivalente) sem alterar o sistema original.
- [ ] Criar componente de navegação pública, hero de destaque e CTAs reais.
- [ ] Implementar tokens, tipografia, grid e responsividade 1440/768/390px.
- [ ] Otimizar hero: asset fotográfico separado da interface mockup (não use screenshot inteira como página).

### Fase B — Narrativa completa
- [ ] Integrar seis módulos em grade 3x2 com textos curtos.
- [ ] Construir seção de benefícios no meio da página.
- [ ] Exibir fluxo de quatro etapas com imagens/ícones acessíveis.
- [ ] Criar tour de produto com screenshots da Alpha, sempre deixando claro quando forem demonstrativos.
- [ ] Inserir CTA final e footer.
- [ ] Social proof real somente após validação de autorização; caso contrário criar bloco de credibilidade factual.

### Fase C — Operacionalizar e revisar
- [ ] Implantar envio de formulário demo com validação e mensagem de sucesso; destino e consentimento LGPD.
- [ ] Conectar botão “Entrar” à autenticação da Alpha.
- [ ] Testes de teclado/semântica/contraste, performance e responsividade.
- [ ] QA visual versus a primeira prévia em desktop e mobile.
- [ ] Atualizar documentação, checklist e changelog após cada revisão do usuário.

## Backlog do produto preservado

**Já existe em implementação Alpha inicial (testada em API):** login e papéis, projetos, briefing versionado, cadastro de fornecedores, RFQ por link, resposta estruturada, itens de cotação, propostas versionadas, aprovação, tarefas e auditoria.

**Ainda pendente ou incompleto:** envio real por e-mail, matriz comparativa avançada, importação/exportação Excel, anexos, detalhes operacionais de hotelaria/aéreo/rooming/A&B/transfers, segurança de produção, escalabilidade e gestão de usuários avançada. Não prometer recursos não concluídos na landing como se estivessem disponíveis hoje.

**Produto original:** não tocar no projeto anterior. O código atual está em `NEXO/ALPHA/` e serve como ponto de continuidade, com visual provisório que será substituído gradualmente pela direção aprovada.

## Critério para considerar a próxima etapa concluída

Landing navegável e responsiva em desktop/mobile com hero fiel à primeira prévia, estrutura aprovada, links/CTA funcionando, nenhum dado fictício apresentado como real, sem alteração no legado e revisão por screenshot.