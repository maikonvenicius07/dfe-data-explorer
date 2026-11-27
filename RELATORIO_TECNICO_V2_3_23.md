# DF-e DATA EXPLORER — V2.3.23-beta.1

## Objetivo e base

Padronizar os leiautes dos documentos efetivamente importados, a partir do ZIP `dfe-data-explorer-main (5).zip` (V2.3.22-beta.1, commit 7f9089b48598da27fe05af74e9a84de7bbaea0e2). Não reconstruir o aplicativo. A importação anterior foi bem-sucedida: o ZIP contém 14 catálogos/variantes, 5.830 registros ao todo. As fontes são os catálogos e metadados do próprio ZIP, não uma nova consulta ao portal. A auditoria examinou o registro de documentos, normalização, seleção, árvore, diagramas, impressão, importador, dados e estrutura de publicação. Não foi uma certificação integral de cada regra fiscal.

## Diagnóstico e correções

| Área | Causa | Correção |
|---|---|---|
| Seleção progressiva | `renderMoc` condicionava a marcação dos filhos à NF-e | Mesma ação em todos: expandir marca nó e filhos diretos apresentados; recolher mantém; filtros e expansão global não marcam. Seleção exclusiva também respeitada quando o filtro de selecionados está ativo. |
| Configuração inicial | `installDocument` tratava documentos novos de forma distinta e podia herdar modo de tabela | Mesmo modo hierárquico inicial e estado de expansão do motor NF-e; estados de seleção e navegação salvos separadamente. |
| Grupos | Rótulos repetiam títulos completos e atributos versao/Id viravam seções isoladas | `groupLabel` abrevia títulos com base na seção/descrição original; `harmonizeDocumentRows` reagrupa atributos no grupo do pai quando a seção e vínculo coincidem. IDs oficiais não inventados. |
| Hierarquia | GS/SG e Raiz não eram reconhecidos pela lista de categorias estruturais | Correção da projeção de apresentação: 24 vínculos NFCom e 10 CT-e recuperados quando a seção, nível numérico, categoria do pai e eventual pai explícito são compatíveis. Outros vínculos ficam como pendentes; não se deduzem pais a partir de nomes ou posição sem nível. |
| Diagnóstico | Vínculos faltantes pareciam campos independentes comuns | Aviso no campo e na impressão; informações originais mantidas. |
| Formatação | Pai contém nomes XML mais longos em manuais por nível | Coluna Pai mais larga quando IDs não foram publicados; mantém dez colunas e estilo hierárquico. Ajuste de quebra de ID/Pai na tela. |
| Identificadores | CSV da seleção podia exibir hashes internos | Exporta o ID e o Pai de apresentação, sem transformar hashes em IDs oficiais. |
| Diagrama | Raiz única podia ocultar seções independentes em catálogos importados | Inclui raízes distintas no modo documento completo para catálogos com sourceSection; NF-e preservada. |
| Oracle | DER genérico de outros documentos podia exibir legenda de DC-e | Legenda conceitual específica ou genérica, sem copiar relacionamentos de outro documento. |
| Versão | Arquivos JS, CSS, PDF e offline precisavam estar coerentes | V2.3.23 nas referências, rodapé, nome PDF e arquivo offline regenerado. |

Os catálogos JSON, as chaves internas e os workflows permanecem byte a byte idênticos à entrada. As correções hierárquicas são uma projeção em memória: `original`, `sourceValues` e metadados permanecem preservados. O importador não foi reexecutado nem alterado. Não se afirma que todos os vínculos ou o XSD foram certificados. A antiga contagem de 311 avisos é do importador original; foram recuperados 34 na apresentação em NFCom e CT-e, restam 277 avisos a revisar, conforme a base. NF3-e tem 114 sem nível numérico; NFCom tem 116 ainda não resolvidos. Não forçar hierarquia nessas linhas.

## Catálogos preservados e testados

| Documento | Registros | Teste de seleção e PDF A4 paisagem |
|---|---:|---|
| NF-e/NFC-e | 1173 | Aprovado: 2 registros escolhidos, 1 página |
| DC-e | 111 | Aprovado: 2 registros escolhidos, 1 página |
| CT-e | 978 | Aprovado: 3 registros escolhidos, 1 página |
| CT-e OS | 314 | Aprovado: 3 registros escolhidos, 1 página |
| GTVe | 162 | Aprovado: 3 registros escolhidos, 1 página |
| NF-e ABI | 269 | Aprovado: 3 registros escolhidos, 1 página |
| NFGAS | 464 | Aprovado: 4 registros escolhidos, 1 página |
| NFAG | 350 | Aprovado: 5 registros escolhidos, 1 página |
| NF3-e | 507 | Aprovado: 4 registros escolhidos, 1 página |
| NFCom | 410 | Aprovado: 4 registros escolhidos, 1 página |
| BP-e | 293 | Aprovado: 3 registros escolhidos, 1 página |
| BP-e TM | 228 | Aprovado: 3 registros escolhidos, 1 página |
| BP-e TA | 246 | Aprovado: 18 registros escolhidos, 1 página |
| MDF-e | 325 | Aprovado: 3 registros escolhidos, 1 página |

## Testes executados

- 31 testes Python aprovados (importadores, publicação e consistência de arquivos); quatro suítes JavaScript aprovadas; verificação de sintaxe.
- Chromium com os catálogos reais embutidos: 14 documentos/variantes, expansão, marcação, recolhimento, expansão global sem novas marcações, alternância e seleção isolada. PDF direto A4 paisagem de cada um; conferência de versão e orientação, contagem e unicidade das linhas na prévia, captura visual da primeira página.
- Regressão NF-e Grupo W: 22 registros, uma página A4 retrato.
- Ramificações maiores: NF3-e total (20 registros, 2 páginas); NFCom gFidelidade (5 registros, 1 página); MDF-e ide (25 registros, 3 páginas); CT-e emit (20 registros, 2 páginas).
- Total: 19 PDFs reais incluídos em `docs/v2323/`, com logs. A navegação remota por URL de teste foi bloqueada pelo ambiente. Teste do carregador estático com assets reais e respostas fetch injetadas (sem acesso remoto), conforme log.
- Não foi executada a suíte histórica completa (alguns testes antigos esperam que documentos hoje existentes estejam pendentes), nem foi validado o GitHub Pages remoto, XSD, backend, impressora física ou todos os formatos de papel para cada documento. Exportação XLSX via servidor e atualização pelo backend continuam exclusivas da NF-e; CSV e PDF locais são compartilhados.

## Instalação

Utilize o ZIP completo ou sobreponha o incremental na RAIZ do repositório, preservando os caminhos. Não aninhar `public/` ou `.github/workflows/`. Não é necessário reimportar os manuais para aplicar a padronização. Confira V2.3.23 no cabeçalho e no PDF; Ctrl+F5 após a publicação.

## Arquivos de código modificados

`public/app.js`, `public/styles.css`, `public/diagram-state.js`, `public/pdf-export.js`, `public/index.html`, `public/EXPLORADOR_OFFLINE_COMPLETO.html`, `VERSION`, `README.md`, `CHANGELOG.md`, `ARQUIVOS_SHA256.txt`; adicionados três testes e exemplos/logs de QA. Nenhum arquivo removido.
