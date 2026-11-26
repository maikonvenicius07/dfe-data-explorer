# DF-e Data Explorer — V2.3.16-beta.1
## Reformulação da árvore gráfica no relatório MOC

Base: DFE_DATA_EXPLORER_V2_3_15_COMPLETO.zip. Alteração pontual na impressão, sem reconstrução da aplicação.

### 1. Diagnóstico do documento recebido
- `testetstenfs(1).pdf`: duas páginas A4 retrato, sem rotação, produzido por Microsoft Print to PDF. A página 2 contém apenas três registros. O relatório mostra recuos, mas os conectores se resumem a pequenos cotovelos isolados, sem continuidade pelos irmãos ou descendentes.
- A extração pelo Poppler e PyMuPDF retornou zero texto; não há fontes registradas nem imagens detectadas, mas há 3.309 e 401 operações de desenho nas páginas 1 e 2. Isso é compatível com texto convertido em contornos pelo pipeline de impressão, e não permite atribuir com certeza a causa a uma etapa específica. O PDF direto do aplicativo evita o driver Windows e conserva texto pesquisável.
- O código anterior calculava a profundidade da árvore, mas cada linha tinha apenas um conector local, tanto no CSS como no PDF direto. A largura da coluna Campo era insuficiente para recuos mais expressivos.

### 2. Implementação
- `mocPrintBranches()` deriva as ramificações de `mocHierarchyEntries()` e dos caminhos originais dos registros, após a seleção. Calcula irmãos posteriores, guias dos ancestrais, último irmão, haste para os filhos e caminho de contexto. O desenho não depende de mera proximidade entre linhas.
- A mesma tabela HTML fornece os metadados (`data-depth`, `data-rails`, `data-tail`, `data-child`, `data-path`) para a prévia, impressão nativa e PDF direto. Não há cálculo independente da hierarquia no PDF. As linhas são vetoriais: bordas CSS e comandos de linha no PDF direto.
- Coluna Campo ampliada, recuo proporcional à profundidade e à largura física disponível, destaque estrutural em negrito e cores suaves por nível, conectores contrastantes inclusive em preto e branco. ID e Pai preservados. As dez colunas são mantidas por padrão; configurações anteriores de colunas continuam disponíveis.
- Pais intermediários ausentes da seleção são indicados como contexto textual na própria célula Campo, quando necessários. Não são novas linhas nem alteram a contagem ou a seleção. Irmãos não selecionados não são acrescentados. A profundidade não é recalculada a partir da seleção.
- A impressão nativa usa um clone da mesma tabela e mede a área útil da página. Procura manter o pai com o primeiro descendente e redistribuir pequenas continuações quando possível. Nas páginas seguintes repete título, colunas e caminho hierárquico. O PDF direto utiliza os mesmos dados e critérios semelhantes. Não se força toda a árvore em uma página.
- Se uma linha excepcionalmente alta não couber no papel, o navegador retorna à paginação nativa; nesse caso os cabeçalhos comuns permanecem, mas a indicação explícita de caminho por página pode não estar disponível. As duas saídas não são pixel a pixel idênticas, pois têm motores diferentes.

### 3. Evidências e testes
- `tests/test_branch_print_v2316.py`: seleção real em Chromium, igualdade de metadados da prévia e do documento, profundidade de W37/W42, continuidade de W38/W43, fim dos ramos W41/W46 e retorno W47/W48/W49 a W36. W43 isolado mantém nível 4 e identifica os pais ausentes como contexto. W37/W42 isolados são irmãos. Nenhum registro adicional foi introduzido.
- Reconstruídos visualmente os 41 IDs do PDF recebido. Relatórios A4 retrato e paisagem nos dois motores resultaram em três páginas com fonte legível, título e caminho de continuação; não se tentou repetir a compressão do driver Windows. O caso anterior de três linhas isoladas foi reduzido no exemplo de retrato do navegador: a última página contém 12 registros (conferir exemplos). A paginação varia de acordo com tamanho de papel, fonte, conteúdo e navegador.
- Novo teste gerou 11 PDFs; regressão `test_print_hierarchy_v2315.py` gerou mais 13 PDFs, incluindo catálogos de 1.173 e 196 registros, grupos diferentes, A4/A3, preto e branco, orientação e grupo W completo em seis páginas nos dois motores. Conferidos texto extraível, limites físicos da página, títulos, recuos, ausência de campos não selecionados, as dez colunas e correspondência prévia/documento. Inspeção visual por imagens dos exemplos e das páginas de continuação.
- Executados quatro testes JS históricos de seleção/diagrama; nove testes Python de importação/publicação; testes de regressão V2.3.12 (expansão e seleção progressiva) e V2.3.14 (simplificação e impressão em ambos os catálogos). Todos passaram localmente. Sintaxe JS verificada; HTML offline reconstruído dos mesmos arquivos.
- A impressão nativa foi testada em Chromium, não em Microsoft Print to PDF ou impressora física. O PDF enviado pelo usuário não foi modificado. Recomenda-se Baixar PDF direto para evitar perda de texto no driver. O XSD permanece pendente de validação integral; nenhuma atualização externa do MOC ou publicação remota foi executada nesta versão.

### 4. Arquivos e preservação
- Alterados: `public/app.js`, `public/styles.css`, `public/pdf-export.js`, `public/index.html`, `public/EXPLORADOR_OFFLINE_COMPLETO.html`, `VERSION`, `README.md`, `CHANGELOG.md`, `docs/FUNCIONALIDADES_APROVADAS.md`, `ARQUIVOS_SHA256.txt`.
- Novos: teste `tests/test_branch_print_v2316.py`, este relatório e 14 exemplos PDF em `docs/exemplos_v2316/`.
- Catálogos, dados históricos, filtros, seleção progressiva, botões +/− filhos, menu simplificado e modelagem Oracle preservados. Não foram reintroduzidas telas ou outras seções de impressão retiradas em versões anteriores. Nenhum arquivo excluído.
- Atualização incremental sobre V2.3.15: extraia os arquivos na raiz, mantendo caminhos; publique no GitHub e recarregue com Ctrl+F5. Confirme V2.3.16 no cabeçalho. Teste W36, W37, W42 e filhos, e Baixar PDF direto em A4 paisagem. Exemplos em docs/exemplos_v2316.
