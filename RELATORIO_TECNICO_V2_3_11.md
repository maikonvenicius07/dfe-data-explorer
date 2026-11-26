# DF-e Data Explorer — V2.3.11-beta.1

Data: 26/11/2026. Base: ZIP completo V2.3.10. Escopo: remoção da faixa de atalhos indicada na imagem.

## Alteração

Removida integralmente a faixa “Divisões XML neste grupo”, incluindo os botões de atalhos e o espaço ocupado por ela, de todos os grupos do Leiaute do MOC e dos três modos (oficial, hierárquico, Oracle). A tabela fica imediatamente abaixo do título do grupo. Os títulos e contagens no cabeçalho do grupo foram mantidos. A faixa não é meramente escondida: sua geração, evento de clique e estilos exclusivos foram removidos.

## Preservação

Nenhuma alteração na base MOC/XSD, nos IDs, nas dez colunas, na hierarquia, nos filtros, na expansão/recolhimento, no estado compartilhado, na marcação individual ou +/− filhos, nos quatro itens do menu, na Central de Impressão ou no motor de PDF. O HTML offline foi regenerado com o mesmo código da versão web. Nenhum arquivo removido.

## Arquivos novos ou modificados

- `public/app.js`: remove geração e evento da faixa.
- `public/styles.css`: remove estilos exclusivos da faixa.
- `public/index.html`: número da versão.
- `public/EXPLORADOR_OFFLINE_COMPLETO.html`: regeneração oficial.
- `VERSION`, `README.md`, `CHANGELOG.md`, `docs/FUNCIONALIDADES_APROVADAS.md`: identificação e registro da decisão.
- `tests/test_simplified_navigation_v2310.py`: regressão da ausência da faixa e da presença da tabela em todos os grupos, nos três modos.
- `RELATORIO_TECNICO_V2_3_11.md`: relatório novo.
- `ARQUIVOS_SHA256.txt`: manifesto atualizado.

## Testes executados

- Sintaxe de `public/app.js`: aprovada.
- Pytest de importação e publicação: 9 aprovados.
- Quatro arquivos de testes Node: aprovados (seleção, alternância de filhos, diagrama progressivo, seleção integrada).
- Chromium/Playwright: ausência da faixa e dos atalhos em todos os grupos nos três modos do MOC; tabelas mantidas imediatamente sob o título; navegação de quatro telas, seleção individual e reversível de filhos, preservação de seleções de grupos distintos, quatro seções da impressão e bloqueio de impressão vazia: aprovados.
- PDF direto real: A4 paisagem, A4 retrato e A3 paisagem. Conferência de dimensões, rotação zero, texto horizontal e seleção exata: aprovada.

## Limitações e publicação

Os testes foram feitos localmente com o catálogo embutido de 196 nós da versão-base, sem substituir nem importar informações. A imagem do usuário indica um catálogo carregado diferente; o código da faixa é comum a todos os catálogos e modos, mas a base carregada no ambiente do usuário não foi testada. Não houve publicação remota nem teste em impressora física. A validação de PDF nesta versão foi estrutural e textual, não uma nova auditoria visual.

Se o GitHub estiver na V2.3.10, aplique o ZIP incremental mantendo os caminhos. Caso contrário, use o ZIP completo. Não apague a base de dados externa ou os dados locais do navegador. Após publicação, use Ctrl+F5. Para uso offline, abra `public/EXPLORADOR_OFFLINE_COMPLETO.html` atualizado.
