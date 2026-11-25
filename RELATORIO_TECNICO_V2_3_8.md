# DF-e Data Explorer — V2.3.8-beta.1

Data: 25/11/2026. Base: ZIP completo V2.3.7-beta.1. Escopo: correção da impressão do diagrama, orientação física do PDF e seleção integrada preservada.

## Diagnóstico

O PDF fornecido (`testeteste.pdf`) contém sete páginas, MediaBox de aproximadamente 595,32 × 841,92 pt (A4 retrato), /Rotate 0 e conteúdo visual girado. O produtor registrado é Microsoft: Print To PDF. O sumário do próprio PDF indicava A4 landscape. Logo, o problema não é apenas o metadado de rotação da página; a saída do driver foi efetivamente orientada de maneira incompatível com o leiaute. Não foi possível executar esse driver Windows neste ambiente. Nas páginas 5–7 o diagrama aparece em seis fragmentos compactos. O código anterior iniciava `diagramMode` em compact, e o seletor `printDiagramFormat` não determinava o formato do relatório integrado. O algoritmo anterior de impressão horizontal dividia a sequência de nós e podia separar a cadeia ancestral.

## Correção

- Árvore horizontal como padrão na aplicação; a Central de Impressão segue o formato da tela por padrão, com escolha explícita horizontal/vertical/compacto. Não se troca a estrutura selecionada por blocos compactos automaticamente.
- SVG horizontal com caixas, bordas, cores e curvas pai-filho inspiradas diretamente no diagrama aprovado da interface. Paginação por caminhos de ramificações, com referências de continuação identificadas. Pais de contexto não se tornam registros selecionados. Sem incluir irmãos ou descendentes não escolhidos.
- `Baixar PDF direto` gera um arquivo vetorial localmente, sem Microsoft Print to PDF. Dimensões físicas de A4/A3 calculadas em pontos e /Rotate 0. Textos e conectores permanecem vetoriais, e a tabela repete cabeçalhos em páginas adicionais. A impressão via navegador foi preservada, com @page em dimensões explícitas. Preferir o PDF direto para evitar rotação pelo driver.
- O PDF direto suporta os modos integrados (selecionados, visíveis, completo) e os modos de diagrama XML; os relatórios legados continuam utilizando a impressão nativa. O PDF direto tem composição própria, com a mesma seleção e SVG da prévia, mas a paginação e apresentação tipográfica das tabelas podem diferir. Utiliza fontes PDF padrão Helvetica/WinAnsi; português e caracteres ocidentais são suportados, outros caracteres Unicode podem ser substituídos por '?'. Não depende de bibliotecas remotas. Não altera dados fiscais.
- HTML offline regenerado; oito telas, base demonstrativa de 196 nós, filtros, seleção compartilhada, arquivos XSD e publicação mantidos.

## Evidências

Teste reproduziu a seleção de 13 registros mostrada nas tabelas do PDF: W01, W02, W03, W04, W04a, W15, W16, W16a, W17, W23, W31, W34 e W60. ROOT e A01 aparecem apenas como contexto. W05 e W38 não são incluídos. As quatro seções usam os mesmos registros selecionados.

| Teste | Resultado |
|---|---|
| PDF direto real, A4 paisagem | 6 páginas, diagrama em 2 páginas, /Rotate 0, texto horizontal pesquisável |
| PDF direto real, A4 retrato | 7 páginas, /Rotate 0, texto horizontal pesquisável |
| PDF direto real, A3 paisagem | 5 páginas, diagrama inteiro em 1 página, /Rotate 0, texto horizontal pesquisável |
| Impressão Chromium A4 paisagem | Dimensões e orientação corretas |
| Seleção completa do catálogo | PDF direto gerado e verificado |
| Registros selecionados e curvas pai-filho | Aprovado |
| Mudança do formato na Central de Impressão | Aprovado |
| Testes JS seleção, expansão e integração | 3 arquivos aprovados |
| Testes Python importação/publicação | 9 aprovados |
| Sintaxe JS | 4 arquivos aprovados |

As amostras reais estão em `docs/exemplos_v238/`. Foi conferida visualmente a árvore horizontal em A4/A3 paisagem e a tabela de MOC. O teste automático verifica posição de cada linha de texto no PDF direto, ausência de rotação, conteúdo e limites da página. O layout A4 distribui os 13 registros em duas páginas de diagrama; A3 permite a árvore completa em uma página. A escolha da orientação e formato de papel permanece do usuário. O driver Windows, a impressora física e a implantação remota não foram testados. A impressão nativa ainda depende das configurações do navegador e driver.

## Publicação

Extraia o ZIP incremental sobre a raiz do repositório local, mantendo os caminhos (incluindo o novo `public/pdf-export.js`). Commit e Push origin; confira GitHub Actions e atualize a página com Ctrl+F5. Se a base não for V2.3.7, use o ZIP completo. Na Central de Impressão selecione Paisagem, Mesmo formato do Diagrama XML (ou Árvore horizontal) e Baixar PDF direto. O catálogo continua parcial; esta atualização não importa novos campos do MOC.

## Arquivos alterados e novos

- `.github/workflows/validar.yml` — modificado
- `ARQUIVOS_SHA256.txt` — modificado
- `CHANGELOG.md` — modificado
- `README.md` — modificado
- `RELATORIO_TECNICO_V2_3_8.md` — novo
- `VERSION` — modificado
- `docs/exemplos_v238/EXEMPLO_W_V238_A3_landscape.pdf` — novo
- `docs/exemplos_v238/EXEMPLO_W_V238_A4_landscape.pdf` — novo
- `docs/exemplos_v238/EXEMPLO_W_V238_A4_portrait.pdf` — novo
- `docs/exemplos_v238/EXEMPLO_W_V238_NAVEGADOR.pdf` — novo
- `public/EXPLORADOR_OFFLINE_COMPLETO.html` — modificado
- `public/app.js` — modificado
- `public/index.html` — modificado
- `public/pdf-export.js` — novo
- `scripts/build_offline.py` — modificado
- `tests/test_print_orientation_v238.py` — novo

Nenhum arquivo excluído.

Regressão de navegador V2.3.7 executada novamente após a correção: aprovada (quatro telas, três formatos, modos atual/completo e seleção).
