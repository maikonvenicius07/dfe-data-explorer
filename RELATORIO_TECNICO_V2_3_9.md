# DF-e Data Explorer — V2.3.9-beta.1

Data: 25/11/2026. Base: ZIP completo da V2.3.8. Escopo: seleção reversível dos filhos.

## Diagnóstico

Os botões coletivos do MOC, árvore, ficha técnica, diagrama e Central de Impressão chamavam `changeKeys(descendants(key), true)` incondicionalmente. Assim, repetir a ação apenas marcava a mesma ramificação. Não havia comando inverso nesse controle.

## Correção

- `HierarchicalSelection.toggleNode(key)` consulta o estado atual do conjunto formado pelo nó e todos os descendentes. Se completo, desmarca o conjunto. Se vazio ou parcial, marca o conjunto. Chave inexistente não altera a seleção.
- MOC e árvore alternam o rótulo `+ filhos` / `− filhos`. Ficha técnica, diagrama e Central de Impressão alternam `Selecionar descendentes` / `Desmarcar descendentes`. Os títulos e rótulos acessíveis acompanham a ação.
- Mantida a semântica anterior da ação coletiva: ela inclui o próprio grupo e todos os descendentes, inclusive recolhidos. O checkbox individual continua marcando apenas o nó. Não se alteram irmãos, ancestrais, filtros nem expansão. O botão separado de seleção editorial de grupo inteiro continua como antes.
- Todos os controles utilizam a mesma seleção compartilhada; a impressão é recalculada após a ação.
- HTML offline regenerado a partir dos arquivos atuais. Nenhuma mudança nos algoritmos de diagrama, impressão ou PDF, catálogo MOC, CSS ou dados.

## Testes executados

| Teste | Resultado |
|---|---|
| Sintaxe JS app e selection | OK |
| Quatro arquivos de testes Node (incluindo novo teste de alternância) | 4 aprovados |
| pytest de importação e publicação | 9 aprovados |
| Novo teste de interface em Chromium offline | Aprovado |
| Regressão de orientação/diagrama e PDF direto V2.3.8 | Aprovado |

O teste de interface marcou e desmarcou ICMSTot (W02), verificou seleção parcial, ramo recolhido, sincronização MOC/árvore/ficha/diagrama/Central, preservação de B02 e ausência dos registros desmarcados nas quatro seções de impressão. Nenhum erro JavaScript no teste.

O teste de PDF anterior reproduziu 13 registros W; A4 paisagem (6 páginas), A4 retrato (7 páginas) e A3 paisagem (5 páginas), rotação zero e texto horizontal pesquisável; também verificou PDF nativo, formato gráfico e catálogo completo.

## Arquivos

- `public/selection.js`: operação reversível.
- `public/app.js`: rótulos e eventos compartilhados.
- `public/index.html`, `VERSION`: identificação da versão.
- `public/EXPLORADOR_OFFLINE_COMPLETO.html`: compilação offline.
- `tests/test_branch_toggle_v239.js`, `tests/test_branch_toggle_v239.py`: novos testes.
- `.github/workflows/validar.yml`: inclui novo teste Node.
- `README.md`, `CHANGELOG.md`: documentação.
- `RELATORIO_TECNICO_V2_3_9.md`, `ARQUIVOS_SHA256.txt`: relatório e manifesto atualizado.

Nenhum arquivo excluído. O ZIP incremental contém exatamente os arquivos novos ou modificados em relação ao ZIP completo V2.3.8, com caminhos originais e bytes idênticos ao novo ZIP completo.

## Atualização

Se o GitHub já estiver na V2.3.8, extraia o ZIP incremental e substitua os arquivos correspondentes, preservando as pastas. Caso contrário, use o ZIP completo. Aguarde a publicação e recarregue a página (Ctrl+F5 no Windows). Para uso local, abra `public/EXPLORADOR_OFFLINE_COMPLETO.html`.

Teste: filtre W, expanda total e clique `+ filhos` em ICMSTot; o botão muda para `− filhos`. Clique novamente e verifique a desmarcação. Seleções de outros ramos permanecem. A Central deve imprimir somente o que continuar marcado.

## Limitações

Não houve publicação remota nem teste em impressora física. Foram executados os testes locais descritos acima, não toda a suíte gráfica histórica. Catálogo de 196 nós demonstrativos preservado; cobertura integral do MOC não faz parte desta correção.
