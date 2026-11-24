# RELATÓRIO TÉCNICO — DF-e Data Explorer V2.3.1-beta.1

Data: 24/11/2026  
Base: V2.3.0-beta.1 com o workflow de publicação GitHub Pages já corrigido pelo usuário.

## Solicitação
Remover a tela e a opção **Visão Geral**, mantendo as demais funcionalidades e passando o **Leiaute do MOC** a abrir automaticamente.

## Diagnóstico
A tela de Visão Geral era marcada com `active` em `public/index.html`; o menu possuía `data-view="resumo"`. O JavaScript preenchia os indicadores e gráficos em elementos específicos dessa tela. Eliminar somente o menu deixaria a página inicial visível, e eliminar apenas o HTML sem remover as chamadas de JavaScript causaria exceções por elementos inexistentes.

## Mudanças implementadas
- Removido o menu Visão Geral e o bloco da página correspondente em `public/index.html`.
- O menu **Leiaute do MOC** e sua seção passaram a ser os itens ativos iniciais.
- Removidas as inicializações do dashboard e do modo apresentação exclusivo da tela removida, inclusive a chamada posterior à consulta de dados.
- Mantidos dados, navegação, ficha técnica, diagrama, dicionário, Oracle, seleção hierárquica para impressão, controles A4/A3 e histórico.
- Sincronizado o arquivo HTML offline com `python scripts/build_offline.py`.
- Atualizados versionamento, README, changelog e testes que verificavam a antiga tela.
- Incluído no ZIP completo o **workflow de GitHub Pages já corrigido em publicação anterior**; esse workflow não faz parte dos arquivos incrementais desta mudança.

## Testes locais efetivamente executados
- `node --check public/app.js`: aprovado.
- `node --check public/selection.js`: aprovado.
- `node tests/test_selection_logic_v23.js`: aprovado.
- `python -m pytest -q tests/test_import.py`: **6 aprovados**.
- `python tests/test_no_overview_v231.py`: aprovado; MOC inicial, ausência de Visão Geral, oito áreas de navegação, diagrama e impressão.
- `python tests/test_fullscreen_only_v221.py`: aprovado; botão Tela cheia, quatro formatos de diagrama, MOC e impressão.
- `python tests/test_productivity_v23.py`: aprovado; seleção por grupo/campo, seleção W38, presets, impressão, PDF, dicionário e diagrama.
- `python tests/test_hierarchy_v22.py`: **não concluído** dentro do limite do ambiente (rotina extensa de interface e PDF); não foi considerado aprovado.
- Publicação real no GitHub Pages: **não executada nesta entrega**. Será verificada quando os arquivos alterados forem enviados ao repositório.

## Limitações preservadas
A base padrão contém 196 nós demonstrativos; não constitui uma importação validada do MOC integral. Os XSD oficiais e o monitoramento remoto dependem do ambiente de publicação. Esta atualização não altera a documentação oficial, os schemas ou um banco Oracle.

## Instalação via GitHub Desktop
1. Baixe e extraia o ZIP **MODIFICADOS**; ele contém somente arquivos novos/alterados com seus caminhos originais.
2. No GitHub Desktop, abra **Repository → Show in Explorer**, na pasta local `dfe-data-explorer`.
3. Copie o conteúdo da pasta extraída **para dentro da raiz do repositório**, mesclando as pastas e substituindo somente os arquivos com mesmo nome.
4. Confira as alterações no GitHub Desktop e faça o commit: `V2.3.1 - remover Visão Geral`.
5. Clique em **Push origin**. O workflow de publicação já configurado deverá ser acionado por alterações na pasta `public/`.
6. Abra `https://maikonvenicius07.github.io/dfe-data-explorer/` e atualize com `Ctrl+F5`; confirme que o menu começa em **Leiaute do MOC**.

## Reversão
No GitHub Desktop, reverta o commit V2.3.1 caso haja regressão, faça push e confirme novamente a publicação. Não apague o histórico nem os dados.
