# DF-e Data Explorer — V2.3.21-beta.1

Data: 27/11/2026. **Entrega parcial — infraestrutura de importação e carregamento; não representa a implementação integral dos leiautes solicitados.**

## 1. Escopo e resultado

Base: ZIP fornecido `dfe-data-explorer-main (3)(1).zip`, versão interna 2.3.20-beta.1. A página pública consultada exibia 2.3.20. Não houve publicação remota nesta sessão. O portal MOC do Paraná foi consultado pelas páginas Leiaute, não pelas páginas Visão Geral; trata-se de material de apoio que também requer conferência com manuais, NT e schemas oficiais originais. O aplicativo é independente.

A ausência dos demais catálogos é real, não apenas um problema de CSS/cache. O ZIP continha somente NF-e/NFC-e e DC-e piloto. A coleta integral foi tentada por Python para os 13 catálogos/variantes; todas as tentativas falharam antes de receber HTML (`Temporary failure in name resolution`, errno -3). A consulta textual das páginas via ferramenta de pesquisa não fornece um arquivo HTML integral para o importador local. Isso não comprova indisponibilidade do portal para outros usuários. Nenhum catálogo de teste foi instalado como catálogo fiscal. Não se alterou artificialmente o estado pendente.

## 2. Diagnóstico e correções

| Arquivo / componente | Causa na base | Alteração |
|---|---|---|
| public/documents.js | disponibilidade fixa e somente dois catálogos | registro de famílias e variantes, disponibilidade derivada de arquivos reais, validação de identidade e raiz, chaves próprias |
| public/app.js / switchDocument | carregamento limitado a NF-e/DC-e | carregamento sob demanda, cache por documento, proteção contra resposta assíncrona tardia, seleção e filtros separados, variante interna, importação JSON controlada |
| public/app.js / consultas técnicas | funções com pressupostos específicos da NF-e/DC-e | exibição de IDs de origem distintos das chaves internas, informações de seção e nível, XPath não confirmado sinalizado, sugestões Oracle genéricas identificadas como propostas |
| scripts/import_documents.py | importador exclusivo de DC-e | novo importador compartilhado para Leiaute com ID/Pai ou Nível; usa importador existente para DC-e; separação de CT-e/OS/GTVe e BP-e/TM/TA |
| scripts/build_document_registry.py | sem manifesto derivado dos catálogos | geração de manifesto e atualização da base embutida DC-e |
| scripts/build_offline.py | offline limitado ao catálogo piloto | incorpora catálogos efetivamente presentes |
| .github/workflows/workflows/importar_dce.yml | workflow aninhado, não executável como workflow GitHub | novo arquivo executável diretamente em .github/workflows, chama importador compartilhado |
| .github/workflows/importar_documentos.yml | ausência de coleta conjunta | execução manual por documento ou all; tentativa automática após alterações específicas; registro das falhas, preservação dos catálogos existentes e solicitação explícita de publicação |
| .github/workflows/publicar_paginas.yml | artefato public na raiz não preservava necessariamente /public/ | empacota raiz e public/ em _site mantendo o endereço solicitado |
| public/index.html / public/pdf-export.js | versão anterior | atualização de versão e assets, sem reformular o motor PDF |

Os arquivos aninhados antigos foram preservados como histórico inativo. A seleção progressiva ao expandir da NF-e continua como antes; nos novos documentos a expansão permanece independente da seleção, como já ocorria na DC-e. As consultas técnicas continuam contextuais, sem reintroduzir menus removidos.

## 3. Cobertura real disponível nesta entrega

| Documento | Fonte Leiaute (caminho relativo a https://moc.sped.fazenda.pr.gov.br/) | Registros encontrados nesta coleta | Registros no catálogo entregue | Hierarquia / XSD | PDF real | Situação |
|---|---|---:|---:|---|---|---|
| NF-e/NFC-e | NFe_NFCe/Leiaute.html | não recoletado | 1173 | preexistente; XSD pendente | sim | catálogo preservado |
| DC-e | DCe/Leiaute.html | não mensurado | 111 | piloto; XSD pendente | sim | parcial, coleta falhou |
| CT-e | CTe/Leiaute.html | não mensurado | 0 | não validada | não | coleta falhou |
| CT-e OS | CTe/Leiaute.html | não mensurado | 0 | não validada | não | coleta falhou |
| GTVe | CTe/Leiaute.html | não mensurado | 0 | não validada | não | coleta falhou |
| NF-e ABI | NFe_ABI/Leiaute.html | não mensurado | 0 | não validada | não | coleta falhou |
| NFGAS | NFGAS/Leiaute.html | não mensurado | 0 | não validada | não | coleta falhou |
| NFAG | NFAG/Leiaute.html | não mensurado | 0 | não validada | não | coleta falhou |
| NF3-e | NF3e/Leiaute.html | não mensurado | 0 | não validada | não | coleta falhou |
| NFCom | NFCom/Leiaute.html | não mensurado | 0 | não validada | não | coleta falhou |
| BP-e | BPe/Leiaute.html | não mensurado | 0 | não validada | não | coleta falhou |
| BP-e TM | BPe/Leiaute.html | não mensurado | 0 | não validada | não | coleta falhou |
| BP-e TA | BPe/Leiaute.html | não mensurado | 0 | não validada | não | coleta falhou |
| MDF-e | MDFe/Leiaute.html | não mensurado | 0 | não validada | não | coleta falhou |

A DC-e piloto existente tem 16 grupos e referência NT 2024.001 v.1.21. A NF-e/NFC-e conserva os metadados e a revisão do catálogo entregue pelo usuário, bem como a base demonstrativa embutida de 196 nós como fallback. A versão/data de cada nova fonte não foi certificada nesta coleta. A contagem de linhas encontradas não pode ser inferida da existência do manual. A cobertura e os vínculos reais dos novos documentos não foram certificados.

## 4. Importador e integridade

Mapeia cabeçalhos conforme a fonte, preserva valores originais, identificação de tabelas/seções e ordem, inclui Domínio/Expressão Regular na observação quando presentes, distingue IDs oficiais e identificadores internos. Níveis e pais declarados são tratados separadamente; divergências e tabelas não reconhecidas são registradas. Há checagens específicas de seções principais e modais, que não equivalem à validação XSD nem à certificação integral da fonte. A primeira extração real ainda poderá revelar variações de estrutura não previstas, e deve ser auditada. Redução de registros/tabelas ou aumento de vínculos não resolvidos em relação ao catálogo anterior exige revisão. Erros preservam o catálogo existente. Dados de teste nunca são incorporados ao manifesto de produção.

## 5. Testes efetivamente executados

- 28 testes pytest aprovados: importação existente, importador novo com fixtures HTML sintéticas, publicação, isolamento/identidade e estruturas de tabela. Comando: `python -m pytest -q tests/test_import_documents_v2321.py tests/test_import_dce.py tests/test_import.py tests/test_publication_v232.py`.
- Quatro suítes JS aprovadas: `test_diagram_progressive_v234.js`, `test_selection_logic_v23.js`, `test_integrated_selection_v235.js`, `test_branch_toggle_v239.js`. Sintaxe de app.js e documents.js verificada.
- Teste Chromium com catálogos existentes NF-e e DC-e: seleção separada, alternância, geração de quatro PDFs. Caso NF-e W22: uma página A4 retrato, preservando seleção e impressão. Exemplos reais existentes em `docs/v2321/`. Conferência visual do W22 e grupo emitente DC-e realizada.
- Teste Chromium com 12 variantes novas usando exclusivamente catálogos sintéticos gerados temporariamente, respostas fetch simuladas e assets reais: navegação e geração de PDF exercitadas. Isso valida a integração técnica, não a estrutura fiscal real. Não houve navegação HTTP efetiva no ambiente de testes: política do navegador impediu acesso ao servidor local; os assets foram injetados em memória.
- Coleta de fontes reais: 13 falhas DNS. Log `docs/v2321/coleta_real.log`; JSON `public/data/importacao_documentos.json`.
- Não realizados: validação de cobertura dos novos manuais reais, XSD, PDFs dos novos catálogos reais, testes móveis completos, execução do GitHub Actions, publicação remota ou confirmação HTTP 404 dos JSON. O monitoramento automático periódico continua restrito à NF-e; a nova coleta é manual ou por alteração do importador.

## 6. Atualizar e executar a coleta

1. Atualizar o repositório main com os arquivos na raiz, sem criar subpasta extra, inclusive `.github/workflows/`.
2. Em Actions, abrir **Importar leiautes de todos os DF-e**, clicar em **Run workflow**, escolher `main` e `documento=all`. A opção também aceita chaves individuais (`mdfe`, `nf3e`, `dce` etc.). O runner precisa ter acesso à fonte e permissões de commit/publicação. Não é garantido que a rede do runner ou a extração funcionem sem ajustes; verificar logs.
3. Conferir artefato `cobertura-documentos`, catálogos em `public/data/<documento>/catalogo_atual.json`, manifesto no index e pendências. Validar as tabelas importadas e XSD antes de declarar cobertura integral.
4. Conferir publicação na configuração atual do Pages. Commits pelo GITHUB_TOKEN não necessariamente disparam outra publicação; o workflow tenta solicitar a publicação explicitamente e pode exigir execução manual. Acessar https://maikonvenicius07.github.io/dfe-data-explorer/public/ após publicação concluída.
5. Alternativa: executar `python scripts/import_documents.py` em ambiente com rede, ou salvar cada página Leiaute como HTML e executar `python scripts/import_documents.py --html-dir pasta`. Exemplos de nomes: `DCe.html`, `CTe.html`, `NF3e.html`, `MDFe.html`, `BPe.html`, `NFe_ABI.html`, `NFAG.html`, `NFGAS.html`, `NFCom.html`.

## 7. Conclusão

O bloqueio arquitetural foi tratado; o bloqueio de obtenção dos dados reais não foi superado. O objetivo final solicitado — todos os documentos com conteúdo próprio completo e validado — **ainda não foi atingido**. A versão não deve ser apresentada como implementação integral nem aprovada para uso fiscal dos novos documentos. Não houve exclusão dos catálogos/históricos anteriores. A lista exata dos arquivos incrementais consta abaixo.

### Arquivos novos ou modificados

- `.github/workflows/importar_dce.yml` — novo
- `.github/workflows/importar_documentos.yml` — novo
- `.github/workflows/publicar_paginas.yml` — modificado
- `.github/workflows/validar.yml` — modificado
- `ARQUIVOS_SHA256.txt` — modificado
- `CHANGELOG.md` — modificado
- `README.md` — modificado
- `RELATORIO_TECNICO_V2_3_21.md` — novo
- `VERSION` — modificado
- `docs/v2321/DC-e-emitente.pdf` — novo
- `docs/v2321/DC-e.pdf` — novo
- `docs/v2321/NF-e-W22.pdf` — novo
- `docs/v2321/NF-e.pdf` — novo
- `docs/v2321/coleta_real.log` — novo
- `public/EXPLORADOR_OFFLINE_COMPLETO.html` — modificado
- `public/app.js` — modificado
- `public/data/importacao_documentos.json` — novo
- `public/documents.js` — modificado
- `public/index.html` — modificado
- `public/pdf-export.js` — modificado
- `scripts/build_document_registry.py` — novo
- `scripts/build_offline.py` — modificado
- `scripts/import_documents.py` — novo
- `tests/test_all_document_navigation_v2321.py` — novo
- `tests/test_import_documents_v2321.py` — novo
- `tests/test_multidocument_regression_v2321.py` — novo
- `tests/test_publication_v232.py` — modificado

Arquivos excluídos: nenhum.
