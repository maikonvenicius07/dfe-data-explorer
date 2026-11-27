# DF-e Data Explorer — V2.3.22-beta.1

## Diagnóstico e alcance
Base: ZIP `dfe-data-explorer-main (4).zip`, versão 2.3.21-beta.1. A consulta pública exibiu 2.3.20. O pacote recebido tem `importar_documentos.yml` e `importar_dce.yml` na pasta `.github/workflows/workflows/`. GitHub Actions não executa workflows nessa subpasta. O workflow de publicação anterior também colocava os arquivos de `public` na raiz do site, incompatível com a URL utilizada pelo usuário quando a publicação é via Actions. Não foi possível consultar as configurações privadas do repositório ou os logs de Actions; a causa operacional específica da publicação antiga não está confirmada.

## Alterações
- `.github/workflows/importar_documentos.yml` e `importar_dce.yml`: restaurados no diretório reconhecido pelo GitHub; coleta automática ao mudar os arquivos de importação e manual; relatório de falhas, commit de resultados e solicitação de publicação; proteção contra concorrência com a atualização NF-e.
- `.github/workflows/publicar_paginas.yml`: pacote contém `index.html`, `.nojekyll` e `public/` na raiz, permitindo tanto a entrada principal quanto `/public/`.
- `.github/workflows/validar.yml`: inclui testes de importação multidocumento, geração de offline e instalação.
- `scripts/import_documents.py`: corrige título do documento que poderia ser sobrescrito pelo último grupo; identificação da versão no agente de coleta. Mantidas as validações e preservação do catálogo anterior em falhas.
- `scripts/build_offline.py`: incorpora catálogo NF-e publicado, não apenas os 196 registros demonstrativos. Mantém os catálogos de outros documentos quando existirem.
- `public/app.js`, `public/index.html`: versão atualizada; link para Actions e última falha registrada na tela de catálogo indisponível.
- `public/pdf-export.js`: identificação 2.3.22, sem alteração de leiaute ou paginação.
- `IMPORTAR_LEIAUTES_WINDOWS.cmd`: alternativa local de coleta via Python 3, com ambiente virtual e opção de HTML salvo. O script não foi executado no Windows.
- `COPIAR_PARA_WORKFLOW_GITHUB.txt`, `LEIA_PRIMEIRO_V2322.md`: instruções para evitar a repetição de `workflows/workflows`. O texto de workflow é idêntico ao arquivo YAML oficial.
- `tests/test_deployment_v2322.py`: três verificações de empacotamento e base offline. Dois testes anteriores adaptados à versão do projeto.
- `.gitignore`, `VERSION`, `README.md`, `CHANGELOG.md`, HTML offline e documentação atualizados.

As cópias históricas aninhadas foram mantidas, sem efeito sobre a execução; nenhum arquivo anterior removido. Os arquivos ativos são os que estão diretamente em `.github/workflows/`.

## Cobertura e fontes
Portal: https://moc.sped.fazenda.pr.gov.br/index.html. A página `MDFe/Leiaute.html` foi consultada pela ferramenta de pesquisa e apresenta leiaute geral e quatro modais, mas a tentativa de baixar o HTML bruto falhou no ambiente de execução. O relatório anterior de importação registra falha DNS para as 13 chaves. O download alternativo do MDF-e também falhou. Não houve nova coleta bem-sucedida de HTML integral nem validação XSD. A falha no ambiente local não demonstra indisponibilidade do portal para GitHub ou Windows.

| Documento | Registros reais disponíveis | Estado |
|---|---:|---|
| NF-e/NFC-e | 1173 | Catálogo existente preservado; XSD pendente |
| DC-e | 111 | Piloto parcial preservado |
| CT-e, CT-e OS, GTVe | 0 | Coleta necessária |
| NF-e ABI | 0 | Coleta necessária |
| NFGAS | 0 | Coleta necessária |
| NFAG | 0 | Coleta necessária |
| NF3-e | 0 | Coleta necessária |
| NFCom | 0 | Coleta necessária |
| BP-e, BP-e TM, BP-e TA | 0 | Coleta necessária |
| MDF-e | 0 | Coleta necessária |

Nenhum dado simulado foi incluído nos catálogos publicados. Nenhum documento ausente foi declarado completo. O carregador mantém a indisponibilidade explícita até encontrar dados válidos.

## Testes executados
- 28 testes Python de importação, DC-e e publicação aprovados; 3 testes novos de instalação e offline aprovados.
- 4 suítes JavaScript aprovadas: seleção, seleção integrada, diagrama progressivo, alternância de descendentes.
- Sintaxe JavaScript verificada; cinco YAML na pasta de workflows ativa analisados localmente. Não equivale a execução pelo GitHub.
- Chromium: NF-e, NF-e-W22, DC-e e DC-e-emitente geraram PDFs pesquisáveis; W22 permanece em uma página A4 retrato. Testes de navegação, seleção e modo offline aprovados.
- Chromium: 12 variantes adicionais passaram em navegação e PDF com fixtures explicitamente sintéticas, em diretório temporário. Não representa validação fiscal.
- Não executados: workflow remoto, coleta integral, teste Windows, publicação real e conferência XSD. A solução é parcial e não garante importação remota bem-sucedida.

## Atualização do GitHub
Leia `LEIA_PRIMEIRO_V2322.md`. Envie os arquivos a partir da raiz. Confirme manualmente a existência de `.github/workflows/importar_documentos.yml` (sem subpasta duplicada). Abra Actions, escolha **Importar leiautes de todos os DF-e**, execute `all` em `main` e confira o resultado. Se a coleta falhar, o log e o arquivo `public/data/importacao_documentos.json` devem indicar o erro. Só considere concluído quando os JSON específicos existirem, a cobertura for conferida e a publicação exibir os dados. Alternativamente execute `IMPORTAR_LEIAUTES_WINDOWS.cmd` no ZIP extraído, com acesso à internet ou com os HTML oficiais salvos. Não envie `.venv` ao GitHub.
