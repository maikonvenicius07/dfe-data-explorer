# DF-e Data Explorer — V2.3.15-beta.1
## Correção da hierarquia na impressão do Leiaute MOC

Base: `DFE_DATA_EXPLORER_V2_3_14_COMPLETO.zip` (144 arquivos). As imagens do usuário mostram a prévia plana (primeira imagem) e a tabela hierárquica de tela (segunda imagem); esta última foi adotada como referência visual, independentemente da inversão das imagens na descrição do pedido.

### Diagnóstico
- `integratedMoc()` chamava `mocTable()` (tabela plana) sobre registros selecionados, ignorando a profundidade calculada por `mocHierarchyEntries()` e os estilos de `mocHierarchyTable()`.
- `pdf-export.js` extraía exclusivamente o texto das células, sem metadados de profundidade ou classificação. Alterar só o CSS não corrigiria o PDF direto.
- A prévia e o PDF do navegador necessitavam de larguras explícitas para evitar compressão das colunas ID, Campo e Pai e distribuição inadequada do espaço.

### Implementação
- Reutilizada a travessia hierárquica por grupo editorial, baseada no vínculo Pai, com a estrutura inteira antes do filtro de seleção. Reutilizadas classificação e renderização de `mocHierarchyTable()`. A profundidade não é recalculada com base apenas nos registros escolhidos.
- Cada linha possui metadados de profundidade e classificação utilizados também pelo PDF direto. Recuo em pontos físicos com passo ajustado à largura disponível e profundidade máxima; conectores discretos na coluna Campo, verde-claro para subgrupos, azul-claro para raízes estruturais, negrito nos grupos e tratamento de atributos. P&B preserva diferenciação por recuo/negrito e tons de cinza.
- Não se acrescentam linhas de ancestrais ausentes: mantém-se o ID do pai na coluna Pai (quando habilitada). Assim, os registros W38 e W47 preservam níveis distintos mesmo sem W36/W37 na seleção. Esta decisão preserva a regra anterior de imprimir somente registros selecionados.
- Cabeçalho do grupo editorial e colunas no `thead` repetido pelo navegador; PDF direto repete ambos com indicação de continuação. Larguras comuns via pesos de coluna e `colgroup`. Fonte do corpo da tabela consistente entre os dois motores. Botão de retirada da prévia fica fora do documento impresso.
- Mantidos dez campos do MOC habilitados inicialmente, configuração de colunas, impressão A4/A3 retrato/paisagem, exportação, presets, seleção individual/progressiva e +/− filhos, menu com quatro áreas, dados e histórico. Não foram reativadas as áreas removidas a pedido do usuário nem as seções adicionais de impressão.

### Testes e evidências
- Novo teste `tests/test_print_hierarchy_v2315.py` executado em Chromium, usando o HTML offline e a injeção do catálogo estático exato de 1.173 registros fornecido na versão anterior. A base embutida de 196 registros foi usada para regressão offline.
- Conferência programática da igualdade entre tela expandida, prévia e documento: chave, classificação, profundidade e ordem das linhas escolhidas. Seleções W36/W37/W38/W39/W41 e W36/W42/W43/W44/W46, 12 registros IBS, campos simples, grupos diferentes, níveis ausentes, remoção na prévia, alteração de colunas e grupo W integral.
- Gerados 13 PDFs reais (direto e navegador), incluindo A4 paisagem, A3 paisagem, A4 retrato e preto e branco. Texto extraído e coordenadas horizontais conferidas para demonstrar recuo progressivo, presença dos escolhidos e ausência de irmãos não selecionados. Orientação e limites da página conferidos. Grupo W completo em seis páginas em cada motor, cabeçalho de grupo e de colunas em todas as páginas. Inspeção visual dos exemplos IBS e da paginação; exemplos em `docs/exemplos_v2315/`.
- Quatro testes JS de seleção/diagrama passaram, nove testes Python de importação/publicação passaram. Regressão V2.3.14 de seleção, presets, prévia, PDF em ambos os catálogos executada. Sintaxe dos JS alterados validada.
- Os formatos de impressão compartilham estrutura e largura relativa das colunas, mas não são pixel a pixel iguais: motores de navegador e PDF direto paginam textos independentemente. Para grupos muito profundos ou papel estreito, o recuo físico é reduzido proporcionalmente sem alterar a profundidade registrada. Impressora física, publicação remota, consulta externa ao MOC e validação fiscal integral do XSD não realizadas. Testes históricos de telas e controles removidos não foram critérios de regressão atual.

### Arquivos e publicação
Alterados: `public/app.js`, `public/styles.css`, `public/pdf-export.js`, `public/index.html`, `public/EXPLORADOR_OFFLINE_COMPLETO.html`, `VERSION`, `README.md`, `CHANGELOG.md`, `docs/FUNCIONALIDADES_APROVADAS.md`, manifesto SHA-256. Novos: teste, relatório e oito PDFs de evidência. Nenhum arquivo excluído; catálogos preservados byte a byte. Atualizar via ZIP incremental sobre V2.3.14 ou ZIP completo e publicar no GitHub. Após a publicação, Ctrl+F5, selecionar o ramo W36 e conferir prévia e PDF direto. Usar A4 paisagem para as dez colunas; A3 pode melhorar a leitura de descrições extensas.
