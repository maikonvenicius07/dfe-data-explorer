# DF-e Data Explorer — NF-e e NFC-e

**Versão do aplicativo:** V2.3.17-beta.1 · **Base embutida:** seleção demonstrativa anterior, 196 nós.

> Projeto independente de documentação técnica. Não é uma publicação oficial do Fisco. A fonte de referência é o [MOC NF-e/NFC-e](https://moc.sped.fazenda.pr.gov.br/NFe_NFCe/Leiaute.html). Nenhum resultado do catálogo parcial deve ser confundido com cobertura oficial completa.

## Abrir imediatamente

Abra o endereço principal `https://maikonvenicius07.github.io/dfe-data-explorer/` no navegador. Em GitHub Pages configurado pela branch `main` e `/ (root)`, o arquivo `index.html` da raiz encaminha automaticamente para `public/`, onde estão as quatro telas principais. Também é possível abrir `public/EXPLORADOR_OFFLINE_COMPLETO.html` no navegador. Não necessita instalar nada. Também é possível executar `python scripts/serve.py` e acessar `http://localhost:8000`, para usar o servidor opcional.

## Recursos preservados e ampliados

- A aplicação abre diretamente no Leiaute do MOC; a tela Visão Geral foi retirada por solicitação do usuário.
- Leiaute MOC nas dez colunas e modo hierárquico com subgrupos.
- Navegação simplificada: MOC, Modelagem Oracle, Atualizações e histórico e Central de impressão. Os módulos de árvore, dicionário, diagrama e XSD permanecem internos para preservar a infraestrutura de relatórios; não são páginas acessíveis pelo menu.
- A impressão agora contém exclusivamente as tabelas do MOC com os registros selecionados. DER **proposto**, não oficial, continua na Modelagem Oracle.
- Seleção exclusivamente no Leiaute do MOC; a Central de Impressão oferece prévia com retirada individual de registros, configurações, conjuntos salvos opcionais e geração do documento.
- Nenhum pai ou filho não selecionado é incluído como linha do relatório. A impressão preserva a profundidade e a ordem hierárquica do MOC, com recuos na coluna Campo e destaques nos grupos/subgrupos. Os títulos editoriais e cabeçalhos repetem-se nas páginas seguintes.
- PDF A4/A3 direto ou pelo navegador, exclusivamente com as linhas selecionadas do MOC; exportação CSV da seleção, modelagem Oracle separada, monitoramento e histórico.

## Repositório permanente e publicação sem reconstruir o projeto

Consulte [docs/PUBLICACAO_GITHUB.md](docs/PUBLICACAO_GITHUB.md) para os passos de instalação, configuração do GitHub Pages, rotina agendada e recuperação de versões. O repositório está em https://github.com/maikonvenicius07/dfe-data-explorer. O projeto inclui workflow de GitHub Actions e entrada compatível com publicação pela branch `/ (root)`. Confirme a configuração em Settings → Pages e teste o endereço público após cada push.

**Fluxo incremental recomendado:** 1. baixar e preservar a última versão; 2. comparar os arquivos; 3. modificar apenas o necessário; 4. testar; 5. atualizar `VERSION`, `CHANGELOG.md` e relatório; 6. enviar commit; 7. publicar; 8. preservar tags de versões anteriores.

## Limitações importantes

1. O catálogo embutido de 196 nós continua demonstrativo. O ZIP recebido contém adicionalmente 1.173 registros da extração HTML do MOC, de 25/11/2026; não equivale à validação do XSD. Os XSD oficiais não foram importados/validados nesta entrega.
2. A rotina agendada está preparada, mas só será executada após a configuração do GitHub e ativação do Actions. A implantação no Render exige configurar `ADMIN_TOKEN` e armazenamento persistente.
3. A seleção salva utiliza `localStorage` do navegador; não é sincronizada entre computadores e pode ser apagada quando os dados locais do navegador forem limpos.
4. O XLSX gerado pelo backend utiliza o catálogo oficial completo armazenado no servidor; **não** aplica a seleção da impressão. Para exportar exatamente os campos marcados, utilize CSV da Central de Impressão.
5. O endereço público foi verificado antes desta correção e estava exibindo o README. A publicação desta atualização e seu funcionamento externo dependem de commit/push no GitHub. Não houve teste em Render nem validação completa da base oficial.

## Verificações

Execute `node tests/test_selection_logic_v23.js`, `python -m pytest -q tests/test_import.py tests/test_publication_v232.py` e `python tests/test_simplified_controls_v2314.py`. O último requer Playwright, Chromium e PyMuPDF. Os testes de interface anteriores que abrem as quatro telas retiradas são históricos e não representam os requisitos de navegação atuais.

Arquivos para manter sincronizados: `public/index.html`, `public/styles.css`, `public/selection.js`, `public/app.js` e `public/EXPLORADOR_OFFLINE_COMPLETO.html`. Ao alterar o código, execute `python scripts/build_offline.py`; ao importar MOC validado, execute `python scripts/build_static.py`.


## Seleção manual para impressão — V2.3.3

No **Dicionário de Dados**, filtre por grupo, subgrupo, texto ou tipo. Filtros **não marcam registros**. Use a caixa da coluna `Imprimir` para marcar campos individualmente; o checkbox do cabeçalho opera apenas sobre os filtrados, apresentando estado parcial. Os botões permitem marcar/desmarcar filtrados ou toda a documentação. `Somente selecionados` facilita a conferência.

O botão **Imprimir selecionados** leva à Central de Impressão e mantém as marcações de outros grupos. Nessa área, configure A4/A3, orientação e colunas; verifique a lista de campos na prévia e retire os indesejados antes de gerar PDF. Sem seleção, a impressão fica bloqueada. As árvores e o diagrama compartilham o estado de marcação, mas selecionar/navegar até um grupo não marca seus campos automaticamente.

**Atenção:** a base embutida ainda cobre 196 nós do catálogo demonstrativo, não o MOC completo.

## Diagrama com expansão progressiva — V2.3.4

Na aba **Diagrama XML**, use `+` para expandir apenas os filhos diretos de cada nó, e `−` para recolher somente aquela ramificação. Os controles da barra permitem abrir/recolher tudo ou apenas o elemento selecionado. Alterar o formato horizontal/vertical/compacto preserva as ramificações já abertas. O documento inicia com a raiz e seus grupos superiores; o filtro `Grupo W` começa apenas com W01. Pesquisar um campo expande seus ancestrais.

Impressão: **visualização atual** (exatamente os nós expandidos/visíveis na árvore, inclusive os fora da área de rolagem), **estrutura completa do catálogo** (todos os 196 nós disponíveis, sem alterar as expansões) e **seleção manual** (somente os campos explicitamente marcados, com pais de contexto). Para manter a legibilidade em A4/A3, o PDF refluí os mesmos nós em **cartões hierárquicos pagináveis**: a distribuição geométrica na tela SVG não é reproduzida pixel a pixel. O conteúdo e os relacionamentos de pai-filho são preservados.

Testes: `node tests/test_diagram_progressive_v234.js` e `python -m pytest -q tests/test_import.py`. Arquivos sincronizados: `public/diagram-state.js`, `public/app.js`, `public/index.html`, `public/styles.css`, `public/EXPLORADOR_OFFLINE_COMPLETO.html`. Execute `python scripts/build_offline.py` após modificações.

**Limite:** os arquivos oficiais XSD ainda não foram importados; a seleção de 196 nós não é o leiaute integral.


## V2.3.5 — uma seleção nas quatro visualizações

- Leiaute do MOC, Explorador Hierárquico, Dicionário de Dados e Diagrama XML compartilham o **mesmo conjunto de identificadores internos**. Em todas essas áreas, marcar um campo é independente de filtrar, expandir e navegar.
- Nas caixas do diagrama (horizontal, vertical e compacto) há controles de marcação; pais e subgrupos são marcados **individualmente**, e o comando **Marcar filhos / Selecionar descendentes** é explícito e separado.
- A **Central de Impressão** inicia no modo **Imprimir selecionados — quatro visualizações**. Quatro caixas de opção ligadas por padrão permitem incluir/excluir MOC, árvore, dicionário e diagrama, sem mudar a seleção. A opção **Documentação disponível completa** é explícita e limita-se ao catálogo carregado (196 nós na base demonstrativa).
- Nas seções MOC e Dicionário, somente registros selecionados são linhas de dados. Árvore e Diagrama incluem os ancestrais indispensáveis, identificados como *PAI / CONTEXTO* e não contabilizados como seleção.
- A pré-visualização usa o mesmo documento que a impressão e permite retirar campos. A impressão é bloqueada sem elementos ou se nenhuma seção estiver marcada.
- O relatório pode ser impresso em A4/A3, retrato/paisagem; existe um exemplo de teste em `docs/EXEMPLO_INTEGRADO_B02_W38_V2_3_5.pdf`, com seis páginas A4 paisagem e texto pesquisável.
- Para validar: `node tests/test_integrated_selection_v235.js`, `python tests/test_cross_view_v233.py`, `python tests/test_custom_print_v233.py` e `python scripts/build_offline.py`. Para publicar, faça commit/push dos arquivos modificados e confira as Actions.

**Limite importante:** a publicação ainda utiliza a base demonstrativa de 196 nós; o projeto não inclui a importação e validação integral do MOC e dos XSD oficiais nesta atualização.

## Seleção e impressão integrada (V2.3.7)

- Marque campos em qualquer uma das quatro telas. Filtros, expansão e seleção são operações independentes.
- **Imprimir selecionados** abre a Central com as quatro seções e o conjunto acumulado. Desabilite as seções que não deseja.
- **Imprimir visíveis (4 visões)** captura os registros da visão atual, incluindo a rolagem, sem marcar outros campos nem alterar a seleção acumulada.
- **Documentação disponível completa** exige escolha explícita e cobre apenas o catálogo carregado.
- Diagrama vetorial com conectores pai-filho e formatos horizontal, vertical e compacto; contextos e referências de continuação não contam como novos campos.
- PDFs demonstrativos em `docs/exemplos_v237/`.
- Teste de navegador opcional: `pip install playwright pymupdf`, `playwright install chromium` e `python tests/test_integrated_print_v237.py` (ou configure `CHROMIUM_PATH`).

## Impressão horizontal e PDF direto (V2.3.8)

O diagrama XML inicia em árvore horizontal. Na Central de Impressão, mantenha **Mesmo formato do Diagrama XML** ou escolha explicitamente a árvore horizontal. Use **Baixar PDF direto** para gerar as quatro seções ou o diagrama sem passar pelo driver Microsoft Print to PDF. A4 paisagem é o padrão; A3 paisagem permite mais nós por página. A seleção e o contexto são preservados. A impressão nativa continua disponível. Os modos legados usam a impressão do navegador. Exemplos reais em `docs/exemplos_v238/`.

## Seleção reversível de ramificações (V2.3.9)

O botão `+ filhos` marca o nó e todos os descendentes; quando a ramificação está completa, muda para `− filhos` e desmarca o mesmo conjunto. Em seleção parcial, completa a ramificação. A caixa individual continua independente e as demais seleções são preservadas. A mesma ação vale na árvore, ficha técnica, diagrama e Central de Impressão.

## V2.3.11 — navegação simplificada

Selecione os campos no MOC ou na Central de impressão. Os botões + filhos e − filhos continuam disponíveis. A Central permite incluir as quatro representações no PDF, sem manter quatro telas separadas. O formato horizontal é o padrão; o botão Baixar PDF direto mantém a orientação escolhida.

## V2.3.12 — seleção progressiva ao expandir no MOC

A seta individual de um grupo XML ou subgrupo marca o próprio registro e os filhos diretos apresentados na tabela. Expanda os níveis seguintes para selecionar seus campos. Recolher mantém a seleção; use as caixas individuais ou − filhos para desmarcar. Filtros, busca, cabeçalhos editoriais e Expandir tudo continuam sendo ações de visualização.

## V2.3.13 — impressão exclusiva do MOC

A Central gera apenas a seção Leiaute do MOC, sem capa, sumário ou outras representações. Selecione registros explicitamente; a impressão vazia é bloqueada. Para imprimir tudo, use Selecionar toda documentação.

## V2.3.14 — interface enxuta

Selecione no MOC, clique em Imprimir selecionados e confira a própria tabela na Central. O botão × de cada linha da prévia retira o registro da seleção, sem entrar no PDF. As opções de papel, fonte, margens, cor e colunas atualizam a prévia automaticamente. Observação é controlada na seleção de colunas. Ações de seleção integral redundantes ficam ocultas quando o filtro abrange toda a base. Testes antigos que dependem dos controles removidos são históricos.

### V2.3.16 — impressão em árvore
A coluna Campo apresenta trilhas verticais contínuas e bifurcações reais da seleção. Pais ausentes são identificados como contexto, sem criar novos registros. A impressão nativa e o PDF direto preservam o mesmo modelo. A4 paisagem é o padrão; para maior legibilidade, prefira A3. O botão **Baixar PDF direto** evita conversões pelo driver de impressão. Exemplos reais em `docs/exemplos_v2316/`.

### V2.3.17 — blocos hierárquicos e versão verificável
A impressão mantém a tabela única de dez colunas, com faixas estruturais, níveis explícitos, trilhos reforçados e linhas de fechamento dos ramos. O mapa hierárquico é opcional e inicia desmarcado; ele usa a mesma seleção e distingue os pais de contexto. O PDF mostra V2.3.17 no cabeçalho/rodapé. Confira essa identificação depois da publicação. Assets possuem `?v=2.3.17`; o HTML offline é reconstruído a partir dos mesmos módulos. Exemplos em `docs/exemplos_v2317/`.
