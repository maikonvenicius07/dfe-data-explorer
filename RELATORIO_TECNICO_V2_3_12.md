# DF-e Data Explorer — V2.3.12-beta.1

Data: 26/11/2026. Base: ZIP completo V2.3.11. Escopo: seleção progressiva pela seta de expansão individual do Leiaute MOC.

## Diagnóstico e correção

O evento `data-moc-toggle` alterava somente `mocNodeOpen`, sem atualizar a seleção compartilhada. Agora, ao abrir um nó pela seta individual, são marcados o próprio nó e seus filhos diretos que constam na tabela hierárquica (respeitando grupo editorial e pesquisa). Os próximos níveis são marcados à medida que suas respectivas setas são abertas. Não é feita seleção recursiva automática. A seleção continua acumulativa e é sincronizada com a Central de Impressão e os módulos internos por `syncPrintSelection()`.

Recolher um nó preserva as marcações. A caixa de seleção individual e o botão reversível +/− filhos continuam disponíveis para desmarcar ou marcar explicitamente. A ação coletiva Expandir tudo, a pesquisa, os filtros e os cabeçalhos editoriais permanecem independentes da seleção, para evitar uma marcação integral não solicitada. O comportamento de abertura automática de caminhos durante a pesquisa e a abertura inicial do catálogo não foram modificados. A dica da seta e a descrição da tela explicam a nova regra.

## Preservação

Sem alteração na base de informações, arquitetura da seleção, menu, hierarquia, motor de PDF, orientação, formatos de diagrama ou critérios de impressão. O HTML offline foi regenerado. Nenhum arquivo excluído.

## Arquivos novos ou modificados

- `public/app.js`: evento de expansão individual e rótulos acessíveis.
- `public/index.html`: versão e instrução de uso.
- `public/EXPLORADOR_OFFLINE_COMPLETO.html`: versão offline regenerada.
- `VERSION`, `README.md`, `CHANGELOG.md`, `docs/FUNCIONALIDADES_APROVADAS.md`: versão e regra registrada.
- `tests/test_moc_expand_select_v2312.py`: novo teste de integração em Chromium.
- `RELATORIO_TECNICO_V2_3_12.md`: relatório.
- `ARQUIVOS_SHA256.txt`: manifesto atualizado.

## Testes executados

- Sintaxe de `public/app.js`: aprovada.
- Importação e publicação (pytest): 9 aprovados.
- Quatro testes JavaScript de seleção e diagrama: aprovados.
- Novo teste Chromium: expansão progressiva de W01, W34, W36 e W37; filhos diretos selecionados sem marcar níveis ocultos; seleção prévia de B02 preservada; recolhimento sem perda de seleção; reabertura; desmarcação individual; alternância +/− filhos; pesquisa e expansão global sem marcação; modo técnico Oracle; quatro seções com exatamente o mesmo conjunto selecionado; geração real de PDF horizontal sem W04a e W39: aprovado.
- Regressão Chromium da navegação simplificada: quatro telas, ausência da faixa removida, seleção individual, alternância de filhos, quatro seções, PDF direto A4 paisagem, A4 retrato e A3 paisagem com rotação zero e texto horizontal: aprovado.

## Limitações e implantação

Testes locais com o catálogo embutido de 196 nós. A imagem do usuário indica um catálogo carregado mais amplo, que não está no ZIP-base; não foi testado diretamente. A validação dos PDFs foi estrutural e textual, não uma nova auditoria visual. Não houve publicação remota ou impressão física. Não altere nem apague os catálogos externos. Se a versão publicada for V2.3.11, aplique o ZIP incremental preservando os caminhos; caso contrário use o ZIP completo. Depois da publicação, Ctrl+F5. Para uso offline, abra `public/EXPLORADOR_OFFLINE_COMPLETO.html` atualizado.
