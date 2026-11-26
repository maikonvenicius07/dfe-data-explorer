# DF-e Data Explorer — V2.3.13-beta.1

Data: 26/11/2026. Base: ZIP completo V2.3.12. Escopo: impressão exclusiva do Leiaute do MOC.

## Alterações

A impressão anterior oferecia múltiplas seções e modos. A rotina `printable()` agora gera somente a tabela MOC com as linhas de `buildPrintSelectionData().rows`, agrupadas pelos títulos editoriais. Não inclui automaticamente ancestrais, filhos, campos filtrados ou visíveis. Não utiliza os renderizadores de árvore, dicionário, diagrama, Oracle ou histórico. A capa e o sumário foram retirados; o cabeçalho da seção, fonte, versão, data e rodapé permanecem. A Central de impressão não oferece mais seleção de tipos de relatório, seções ou formato de diagrama. Os controles legados necessários à inicialização foram mantidos ocultos; mesmo que seus valores sejam alterados, não modificam a saída. A opção de imprimir visíveis foi retirada do MOC: a impressão é exclusivamente dos marcados. Para imprimir todo o catálogo, selecione explicitamente toda a documentação.

Permanecem a seleção progressiva da seta, +/− filhos, filtros, seleção individual, revisão dos registros, configuração de colunas, observações, papel A4/A3, orientação, margens, fonte, modo de cores e PDF direto. Nenhuma alteração nos dados do catálogo, menu ou modelagem Oracle. HTML offline regenerado. Não houve exclusão de arquivos.

## Arquivos novos e modificados

- `public/app.js`, `public/index.html`, `public/styles.css`, `public/EXPLORADOR_OFFLINE_COMPLETO.html`: saída única, interface simplificada e versão offline.
- `VERSION`, `CHANGELOG.md`, `README.md`, `docs/FUNCIONALIDADES_APROVADAS.md`: versão e nova regra.
- `tests/test_moc_only_print_v2313.py`: teste específico.
- `tests/test_moc_expand_select_v2312.py`, `tests/test_simplified_navigation_v2310.py`: expectativas de impressão atualizadas para a regra nova, mantendo os testes de seleção e navegação.
- `RELATORIO_TECNICO_V2_3_13.md`, `ARQUIVOS_SHA256.txt`: documentação e manifesto.

## Testes efetivamente executados

- Sintaxe JavaScript: aprovada.
- Importação/publicação: 9 testes pytest aprovados.
- Quatro testes JavaScript de seleção e diagrama: aprovados.
- Três testes de navegador Chromium: impressão exclusiva (incluindo controles legados), expansão progressiva e menu simplificado: aprovados.
- PDF direto real A4 paisagem, A4 retrato, A3 paisagem e PDF nativo Chromium A4 paisagem: verificados com PyMuPDF. Para dois registros de grupos distintos, uma página, dez colunas, somente uma seção, texto pesquisável, dimensões corretas e rotação zero. PDF A4 paisagem também renderizado e inspecionado visualmente.
- Prévia e documento usam os mesmos registros; seleção vazia bloqueia a impressão; retirar registro na prévia atualiza a saída.

Testes históricos que exigem quatro seções ou modos de impressão removidos não foram executados, pois documentam um comportamento substituído por solicitação expressa. Não houve validação de impressora física, publicação GitHub ou catálogo oficial completo. Testes locais com a base embutida de 196 nós.

## Publicação

Se a versão instalada for V2.3.12, aplicar ZIP incremental preservando os caminhos; caso contrário, usar ZIP completo. Não apagar catálogos externos. Após publicar, Ctrl+F5. Para uso local, abrir `public/EXPLORADOR_OFFLINE_COMPLETO.html`.
