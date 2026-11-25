# DF-e Data Explorer — V2.3.7-beta.1

Data: 25/11/2026. Base: `DFE_DATA_EXPLORER_V2_3_6_REVISADO_COMPLETO.zip`, recuperado da biblioteca. Atualização incremental; catálogo e infraestrutura não modificados.

## Objetivo e diagnóstico

A V2.3.6 já tinha um estado compartilhado em `public/selection.js`, controles de marcação nas quatro telas e um relatório integrado. Entretanto, nem todos os atalhos levavam ao mesmo modo de impressão: o Dicionário podia reutilizar um tipo anterior, o Explorador não possuía um atalho direto para imprimir a seleção acumulada e o Diagrama enviava os registros a um relatório isolado. O diagrama impresso usava cartões indentados, sem desenhar efetivamente as conexões XML. A impressão da visualização atual estava limitada ao diagrama. Foram preservadas as bases de seleção e expansão existentes e corrigidas essas lacunas.

## Implementação

- Estado de seleção compartilhado, por chave individual; filtro, pesquisa, navegação e expansão não marcam filhos. A seleção de descendentes e do catálogo inteiro requer ação explícita. A seleção pode reunir registros de grupos diferentes.
- Atalhos Imprimir selecionados nas quatro telas direcionam ao relatório integrado, sem reutilizar um tipo anterior. O cabeçalho também abre a seleção integrada. Sem registros selecionados, a impressão é bloqueada.
- Modo Imprimir visíveis (4 visões) captura o conjunto visível da tela de origem, inclusive registros acessíveis por rolagem, sem alterar a marcação manual. O modo Documentação disponível completa exige ação explícita e abrange o catálogo carregado, não uma promessa de cobertura integral do MOC.
- Central com quatro seções habilitadas inicialmente, controles independentes, contagem por tipo, revisão/remoção individual, prévia integral. A mudança de seções não modifica a seleção.
- MOC mantém dez colunas por padrão, na ordem oficial; Dicionário respeita suas próprias colunas configuradas. Apenas registros efetivamente incluídos no escopo entram como linhas de dados.
- Árvore ordenada por parentesco e diagrama SVG com conectores que representam vínculos do catálogo. Ancestrais não marcados são identificados como contexto; referências repetidas de continuidade não são novas seleções. O desenho é reorganizado para impressão, mantendo o formato horizontal, vertical ou compacto, não reproduzindo literalmente as coordenadas de tela. DER Oracle não é o diagrama XML oficial; na impressão XML integrada, aplica-se horizontal caso o DER esteja ativo.
- Ajustes de paginação, quebra de texto, tamanho das caixas, cabeçalhos repetidos, metadados e controle de colunas. O PDF é produzido pelo mecanismo de impressão do navegador; o usuário escolhe Salvar como PDF. A prévia usa o mesmo conteúdo e a paginação física depende do navegador.
- Geração do HTML independente a partir dos arquivos web atualizados, preservando funcionamento offline.

## Validação

| Verificação | Resultado |
|---|---|
| Sintaxe de app.js, selection.js e diagram-state.js | Aprovada |
| Testes Node de seleção, expansão e integração (3 scripts) | Aprovados |
| Pytest: importação e publicação (9 casos) | Aprovados |
| Teste de seleção cruzada V2.3.3 em Chromium | Aprovado |
| Novo teste integrado V2.3.7 em Chromium | Aprovado |
| PDF real A4 horizontal (paisagem) | 5 páginas |
| PDF real A4 vertical (retrato) | 4 páginas |
| PDF real A4 compacto (paisagem) | 6 páginas |

O teste novo marcou W38 no MOC e B02 no Dicionário; confirmou a sincronização na árvore e no diagrama, desmarcação e remarcação, filtro sem seleção, marcação isolada de grupo sem marcar filhos, preservação dos campos entre telas, os quatro atalhos, quatro seções com exatamente as mesmas duas chaves de dados, conexão W37–W38 e ausência de W39 e W03. Conferiu impressão de uma única chave, duas seções, captura da visualização atual nas quatro telas sem modificar a marcação, catálogo completo de 196 chaves, remoção na prévia e bloqueio sem seleção. Inspecionou os PDFs quanto a texto pesquisável, ausência dos campos não selecionados, páginas com conteúdo e limites físicos do texto. Também foi realizada inspeção visual das páginas dos três formatos em imagens reduzidas. Os exemplos reais estão em `docs/exemplos_v237/`.

Ressalvas: o teste gráfico legado `test_custom_print_v233.py` excedeu o limite de execução e não foi contabilizado como aprovado; as principais funções são cobertas pelo teste atualizado. A impressão A3 e todos os navegadores/impressoras físicos não foram testados de ponta a ponta. Os exemplos têm páginas separadas por seção, com espaço livre em relatórios curtos. A paginação e a escala podem variar no navegador do usuário. Não foi publicada nenhuma alteração remotamente nem testada a produção nesta execução. A base embutida continua sendo uma seleção técnica de 196 nós, sem certificação de cobertura integral oficial ou validação XSD completa. Não foram realizadas atualização remota do MOC, alteração de banco Oracle ou alteração do monitoramento.

## Arquivos e publicação

Arquivos modificados: `public/app.js`, `public/index.html`, `public/styles.css`, `public/EXPLORADOR_OFFLINE_COMPLETO.html`, `VERSION`, `README.md`, `CHANGELOG.md`, `ARQUIVOS_SHA256.txt`.

Arquivos criados: este relatório; `tests/test_integrated_print_v237.py`; três PDFs em `docs/exemplos_v237/`. Nenhuma exclusão. Dados, scripts de importação, seleção base, diagrama interativo, workflows de publicação e infraestrutura preservados.

1. Faça backup do repositório local e confirme a versão de partida. Para atualizar a V2.3.6 revisada, extraia o ZIP de modificados sobre a raiz, mantendo os caminhos. Se houver alterações mais recentes ou uma versão anterior, compare os arquivos ou utilize o completo, preservando `.git` e as configurações locais.
2. Faça commit e push pelo GitHub Desktop; verifique as Actions e o GitHub Pages. Não é necessário alterar o mecanismo de publicação previamente configurado.
3. Alternativamente abra `public/EXPLORADOR_OFFLINE_COMPLETO.html` localmente, sem instalar dependências. Os arquivos de exemplo são demonstrativos, não documentos oficiais.
4. Para executar o teste de navegador: `pip install playwright pymupdf`; `playwright install chromium`; `python tests/test_integrated_print_v237.py`. O teste também aceita `CHROMIUM_PATH` e `DFE_PDF_DIR`.
5. Confirme na interface: selecione um campo de dois grupos distintos, navegue entre as quatro telas, abra Imprimir selecionados, confira a prévia, escolha as seções e use Imprimir/Salvar PDF.
