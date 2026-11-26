# DF-e Data Explorer — V2.3.19-beta.1

## Diagnóstico
Base: V2.3.18 completa. `ficou pior(2).pdf` contém duas folhas A4 retrato, Microsoft Print to PDF, rodapé V2.3.17. O conteúdo termina perto de 21% da altura da primeira folha e 17% da segunda. O PDF anterior `erro na impresao(1).pdf` continha 29 registros, o novo contém 22. A identificação da versão é evidência de que a saída não corresponde ao gerador V2.3.18 entregue; não é possível confirmar se a causa foi cache, implantação incompleta, arquivo local antigo ou outra origem. A escala exata configurada no driver Windows não está disponível e não foi reproduzida.

O código da V2.3.18 ainda entregava ao `window.print()` páginas explicitamente divididas (`prepareBrowserPrint`, `.print-physical-page:not(:last-child)`), podendo sofrer uma segunda alteração de escala no navegador/driver. `planPrint` também juntava pai e primeiro filho antes de verificar o espaço; havia tentativas com orçamento até 72% da altura para conciliar motores. O fallback do PDF direto deslocava pequenos ramos/caudas em bloco. Esses mecanismos são riscos concretos de quebras antecipadas; não se atribui exclusivamente a eles a saída do driver Windows. A reprodução local da base V2.3.18 com 22 registros obteve uma folha A4 somente com redução da fonte a 8 pt. A nova versão obtém a mesma folha a 8,5 pt.

## Correção
- `public/app.js`: `planPrint` mantém a fonte original nos três perfis, mede linhas individualmente e não desloca ramificações; limita a folga adicional de compatibilização a 8% (antes até 28%). `configureMocPrintTable` redistribui pesos de colunas somente no A4 retrato: [6,8,30,21,4,7,5,6,6,25], total 118; anterior [6,8,37,19,4,7,5,6,6,20]. Melhora espaço de descrições e observações e diminui quebras de texto. A hierarquia, recuos calculados, cores, conectores, ordem e conteúdo não foram substituídos. `selectedReportPDF` é o único gerador usado pelos botões Abrir PDF para imprimir e Baixar PDF direto. `prepareBrowserPrint` monta tabela contínua para Ctrl+P (alternativa), sem impor páginas de um tamanho que o driver pode alterar.
- `public/pdf-export.js`: elimina regra de deslocamento de ramos/caudas em fallback; mantém proteção de linhas e repetição dos cabeçalhos. PDF vetorial em tamanho físico, fonte Helvetica/WinAnsi selecionável, rodapé V2.3.19.
- `public/styles.css`: neutraliza quebras e alturas de contêineres no caminho Ctrl+P, conserva `break-inside:avoid` para linhas, thead repetido e mapa opcional. Não aplica escala global. 
- `public/index.html`: novo rótulo do botão Abrir PDF para imprimir, instrução para tamanho real (100%) e alerta de versões misturadas no gerador. URLs dos assets com versão 2.3.19; HTML offline regenerado pelos módulos atuais. A versão do aplicativo e a do gerador PDF são verificadas antes de gerar o arquivo.

## Teste principal
Seleção transcrita visualmente do PDF (22 IDs): W01 W01a W02 W17 W23 W31 W34 W35 W36 W37 W42 W43 W44 W46 W47 W48 W49 W50 W57 W59e W59h W60. Mantidos todos os IDs, na ordem, com 10 colunas. Fonte geral 10 pt, tabela 8,5 pt, margens 12 mm. PDF direto A4 595,276 × 841,89 pt, sem rotação; texto extraível, fonte principal verificada fisicamente. Última linha de conteúdo alcança aproximadamente 91% da altura da folha (90% no Chromium), sem contar rodapé. A tabela deixa pequena margem inferior, em lugar das duas folhas quase vazias do PDF enviado.

| Cenário | Prévia | Ctrl+P Chromium | PDF direto |
|---|---:|---:|---:|
| 22 registros A4 retrato, ajuste em uma página | 1 | 1 | 1 |
| 22 registros A4 paisagem | 2 | 2 | 2 |
| 22 registros A3 retrato | 1 | 1 | 1 |
| 22 registros A3 paisagem | 1 | 1 | 1 |
| 22 registros A4 retrato, tamanho real | 2 | 2 | 2 |
| 22 registros A4 retrato, automático | 2 | 2 | 2 |
| 29 registros anteriores, A4 retrato | 2 | 2 | 2 |
| Grupo W completo, 88 registros, A4 paisagem | 5 | 5 | 5 |
| 12 registros IBS, A4 paisagem | 1 | 1 | 1 |
| 12 registros IBS + mapa opcional | 2 | 2 | 2 |

No caso de 29 registros, a primeira página chega a aproximadamente 76% da altura no PDF direto, 81% no Chromium; segunda página cerca de 81%. Para 88 registros, primeiras quatro páginas do PDF direto chegam a 86–91% da altura. Não se força redução de fonte para caber numa folha; a última página pode ter área livre quando a quantidade de registros é pequena. Formato A4 paisagem tem menos altura; no caso de 22 registros, continua exigindo duas páginas.

## Validações
- `tests/test_print_pagination_v2319.py`: 16 PDFs, cenários acima até Grupo W completo; conferência de todos os IDs na coluna ID, ordem, metadados de árvore na prévia, contagem, texto dentro dos limites físicos, rotação zero e versão correta. Teste interceptou URL da nova aba e confirmou igualdade byte a byte com PDF baixado. Não testou visualizador PDF nativo em Windows.
- `tests/test_print_fit_ui_v2318.py` (regressão): 4 PDFs; seleção pelo MOC, remoção na prévia, mapa opcional; aprovado.
- 9 testes Python de importação/publicação e 3 testes JavaScript de seleção e diagrama aprovados; sintaxe JS aprovada. Renderizadas todas as páginas dos 16 PDFs principais; inspeção em mosaico e visualização em resolução maior do caso principal A4 nos dois caminhos. Os exemplos de referência estão em `docs/exemplos_v2319/`.
- Limitações: publicação GitHub Pages e driver Windows/impressora física não testados; a prévia editável e o PDF usam a mesma divisão planejada, mas o Ctrl+P é fluxo nativo e poderá apresentar diferenças dependendo do navegador e do papel. A suíte histórica integral não foi executada. A base oficial importada de 1.173 registros e o catálogo embutido de 196 foram preservados; não se afirma validação integral XSD.

## Atualização
Use preferencialmente o ZIP completo, pois o último PDF ainda indicava V2.3.17. Se usar o incremental, aplique sobre V2.3.18 completa preservando os caminhos. Aguarde conclusão da publicação, use Ctrl+F5, confirme 2.3.19 no cabeçalho e rodapé. Selecione A4 retrato, fonte 10 pt, margem 12 mm, Ajustar relatório em uma página, mapa desmarcado. Clique Abrir PDF para imprimir; no leitor PDF use A4 retrato e escala 100%. Não selecione A3 no aplicativo e A4 na impressora. Se a nova aba for bloqueada, o PDF é baixado. Nenhuma alteração de seleção ou dados; nenhum arquivo anterior removido.

## Arquivos criados e modificados
- `ARQUIVOS_SHA256.txt` (modificado)
- `CHANGELOG.md` (modificado)
- `README.md` (modificado)
- `RELATORIO_TECNICO_V2_3_19.md` (novo)
- `VERSION` (modificado)
- `docs/FUNCIONALIDADES_APROVADAS.md` (modificado)
- `docs/exemplos_v2319/IBS12_A4_direto.pdf` (novo)
- `docs/exemplos_v2319/IBS12_mapa_direto.pdf` (novo)
- `docs/exemplos_v2319/W22_A3_paisagem_direto.pdf` (novo)
- `docs/exemplos_v2319/W22_A3_retrato_direto.pdf` (novo)
- `docs/exemplos_v2319/W22_A4_paisagem_direto.pdf` (novo)
- `docs/exemplos_v2319/W22_A4_retrato_browser.pdf` (novo)
- `docs/exemplos_v2319/W22_A4_retrato_direto.pdf` (novo)
- `docs/exemplos_v2319/W29_A4_retrato_direto.pdf` (novo)
- `docs/exemplos_v2319/W_completo_A4_direto.pdf` (novo)
- `public/EXPLORADOR_OFFLINE_COMPLETO.html` (modificado)
- `public/app.js` (modificado)
- `public/index.html` (modificado)
- `public/pdf-export.js` (modificado)
- `public/styles.css` (modificado)
- `tests/test_print_pagination_v2319.py` (novo)
