# Relatório técnico — DF-e Data Explorer V2.3.3-beta.1

**Data:** 24/11/2026  
**Base:** ZIP completo V2.3.2 do projeto, preservando estrutura do GitHub.  
**Objetivo:** tornar a seleção de impressão independente dos filtros, acumulativa, verificável e coerente entre as telas.

## 1. Diagnóstico comprovado

| Gravidade | Problema da versão anterior | Evidência no código | Solução |
|---|---|---|---|
| Alta | Todos os 196 registros iniciavam selecionados | `HierarchicalSelection.reset()` populava o conjunto por padrão | Seleção inicia vazia, exceto quando perfil salvo for carregado explicitamente |
| Alta | Botão “Imprimir campos filtrados” apagava marcações anteriores | Handler usava `all(false)` e marcava os campos do filtro | Botão renomeado “Imprimir selecionados”; não altera o conjunto |
| Alta | Escopos “todos”/“grupo” podiam contornar a seleção | `buildPrintSelectionData()` usava dados de filtros conforme `printScope` | Todo relatório usa apenas `printSelection.selected`, independentemente de escopo |
| Alta | Checkbox da tabela marcava descendentes ao selecionar um campo | `changeNode()` cascata | Uso de `changeKeys()` para seleção individual; cascata mantida apenas na ação explícita na árvore de impressão |
| Média | Faltavam filtro de subgrupo, seleção coletiva dos filtrados e estado parcial | Ausência de controles específicos | Implementados controles e master checkbox com `indeterminate` |
| Média | Prévia não oferecia retirada de campos | Exibia apenas uma seção do documento | Lista detalhada de itens selecionados com botão Retirar; inclui grupos e colunas |
| Média | Identidade de campos homônimos poderia colidir ao importar outro catálogo | Chave padrão baseada apenas no ID | Para IDs duplicados, gerar chave com caminho XML informado ou fallback pai/tag; vínculos ambíguos não são assumidos |

## 2. Alterações e preservações

- **`public/selection.js`:** início vazio e novo método de alteração individual por chave.
- **`public/app.js`:** filtros desacoplados de seleção; coluna Imprimir com checkbox geral; seleção compartilhada nas telas MOC, árvore, diagrama e Central; impressão somente do conjunto; coluna configurável e remoção na prévia.
- **`public/index.html` e `public/styles.css`:** controles compactos, contadores, filtro de subgrupo, opções de impressão e estilos da pré-visualização.
- **`public/EXPLORADOR_OFFLINE_COMPLETO.html`:** reconstruído a partir dos mesmos arquivos; pronto para abrir localmente.
- **`tests/`:** testes atualizados e ampliados para a nova regra.
- **`VERSION`, `README.md`, `CHANGELOG.md`, `docs/`:** versão, orientação, evidências e pendências.

**Preservados:** MOC como tela inicial; ausência da Visão Geral; oito telas, quatro formatos de diagrama, exportações anteriores, fluxo de atualização oficial, propostas Oracle e nenhuma alteração no banco de dados.

## 3. Semântica da seleção

- Alterar grupo, subgrupo, pesquisa, ordenação ou modo “Somente selecionados”: **apenas filtra**.
- Marcar um campo no Dicionário/MOC/árvore/diagrama: seleciona **aquele campo**, não todos os filhos.
- Marcar grupo/subgrupo na árvore de impressão: ação deliberada para incluir os descendentes.
- “Selecionar filtrados” e checkbox mestre: somente linhas visíveis sob os filtros ativos. “Desmarcar filtrados” preserva campos selecionados fora do filtro.
- “Selecionar toda documentação”: ação explícita, sem depender do filtro. “Limpar seleção”: remove todos.
- O botão de impressão só funciona quando pelo menos um registro está marcado.
- Na impressão hierárquica, pais não selecionados podem ser exibidos exclusivamente como **contexto** (identificação e vínculo), sem serem contados como campos selecionados. No modo ordem MOC, somente linhas marcadas.
- A prévia mostra grupos e campos marcados, configurações de papel/orientação/colunas e permite excluir campos antes da impressão.

## 4. Testes realizados e evidências

| Teste | Resultado |
|---|---|
| Seleção começa com 0/196 e botão desativado | Aprovado em navegador automatizado |
| Filtrar Grupo B sem marcar | Aprovado |
| Selecionar B02, mudar ao Grupo W, filtrar W37 e selecionar W38 | Aprovado, seleção acumulada 2/196 |
| Checkbox do cabeçalho em seleção parcial | Aprovado (`indeterminate`) |
| Somente selecionados, marcar/desmarcar filtrados | Aprovado |
| Seleção de todos e limpeza | Aprovado |
| Impressão exclusivamente B02 e W38, sem W03 | Aprovado, PDF real com texto selecionável |
| Pais W01/W34/W36/W37 apenas como contexto | Aprovado para a seleção verificada |
| Colunas configuráveis, remoção de B02 na prévia e atualização do relatório | Aprovado |
| MOC → Dicionário → Árvore → Diagrama → Dicionário | Aprovado |
| Testes Python de importação/publicação | 9 aprovados |
| Teste funcional de ausência da Visão Geral | Aprovado |
| Regressão de seleção em Node.js | Aprovado |
| Suíte gráfica legada completa | Não concluída no limite local; requer execução posterior |

**Evidência no pacote:** `docs/V2_3_3_CAMPOS_B02_W38.pdf`. A impressão A4 paisagem gerou duas páginas, conforme a escolha de grupos e a hierarquia de contexto; o conteúdo é pesquisável. O número de páginas depende das configurações e do navegador.

## 5. Limitações e riscos

1. **Cobertura oficial não validada integralmente:** a base de 196 nós é demonstrativa. Não apresentar como MOC completo.
2. XSD oficial e monitoramento persistente continuam sujeitos à configuração/validação separada.
3. Se o usuário incluir a modelagem Oracle na impressão, esta seção continuará marcada como proposta independente, não como correspondência física oficial dos campos XML.
4. A exportação XLSX dinâmica do backend ainda não tem garantia de refletir a seleção da sessão; para ela, priorizar o CSV dos selecionados e o relatório PDF.
5. Alguns relatórios longos dependem de paginação do navegador; conferir a pré-visualização do PDF antes da distribuição institucional.
6. IDs ambíguos sem XPath ou parentagem única deverão ser revisados na importação, não resolvidos por suposição.

## 6. Publicação incremental no GitHub

1. Baixe o ZIP **modificados** e extraia-o.
2. Copie os arquivos extraídos para a raiz do repositório local `dfe-data-explorer`, preservando os caminhos e substituindo os arquivos correspondentes.
3. No GitHub Desktop, revise as diferenças; use a mensagem `V2.3.3 - Seleção manual e impressão de campos escolhidos`.
4. Faça **Commit to main** e **Push origin**.
5. Confira o workflow de validação e o GitHub Pages em Actions.
6. Acesse `https://maikonvenicius07.github.io/dfe-data-explorer/`, pressione Ctrl+F5 e verifique a seleção iniciando vazia no Dicionário.

**Não é necessário limpar ou reconstruir o repositório, nem alterar o banco Oracle.**
