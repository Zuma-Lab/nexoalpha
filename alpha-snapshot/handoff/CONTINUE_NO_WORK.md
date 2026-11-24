# Orientação de continuidade — colar no ChatGPT Work

Quero continuar o **Projeto NEXO ALPHA**, uma reconstrução independente da NEXO, sem reutilizar o layout/código do sistema legado. O arquivo de referência é o pacote `NEXO_ALPHA_HANDOFF_2026-11-23.zip` salvo na Biblioteca ChatGPT em `/NEXO/ALPHA` (ou este pacote anexado).

**LEIA PRIMEIRO, nesta ordem:**
1. `docs/homepage/HOMEPAGE_V1_APROVACOES.md`
2. `docs/homepage/REGISTRO_DE_DECISOES.md`
3. `docs/homepage/DESIGN_SYSTEM_V1.md`
4. `docs/homepage/PLANO_DE_IMPLEMENTACAO.md`
5. `README.md` e `docs/ARCHITECTURE.md`
6. `assets/homepage/01-referencia-aprovada.png`

**A primeira imagem é a direção visual APROVADA.** Preserve o hero cinematográfico com executivo de costas diante da cidade, mockup de dashboard NEXO, grafite/laranja/off-white e linguagem clean. A segunda imagem é uma exploração considerada mais carregada e não deve orientar o layout. Mova “Empresas que utilizam/confiam” para perto do final; coloque “Mais controle, eficiência e economia” no meio. Não fabrique marcas de clientes ou depoimentos.

**OBJETIVO AGORA:** transformar essa homepage aprovada em frontend responsivo real (HTML/CSS/JS/componentes), sem renderizar a screenshot inteira como página. Separar a entrada pública do dashboard autenticado; manter os fluxos de briefing, cotação, planejamento, acessos, fornecedores, proposta e aprovação já existentes na Alpha. Abrir/navegar/testar a página em desktop/mobile e produzir screenshots para revisão. Trabalhar somente numa cópia/pasta ALPHA, nunca alterar o sistema anterior.

**ESTADO DO CÓDIGO:** existe uma Alpha em FastAPI/SQLite/JS no pacote. Os 3 testes automatizados existentes passaram em 23/11/2026, mas a aplicação não está pronta para produção, os recursos listados como pendentes em README ainda faltam e o layout atual do dashboard é provisório. Não reescrever do zero outra vez sem necessidade: a instrução original de 'do zero' significa NÃO reaproveitar o projeto legado; a Alpha nova aqui é a base separada.

**COMO REPORTAR:** ao implementar, diga precisamente o que funciona, o que é apenas visual e o que falta. Atualize os documentos de decisões e checklist com cada novo alinhamento.