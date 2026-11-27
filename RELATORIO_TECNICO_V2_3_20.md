# DF-e DATA EXPLORER — V2.3.20-beta.1
## Expansão multidocumento: arquitetura compartilhada e piloto DC-e

**Data:** 26/11/2026. **Base:** `dfe-data-explorer-main (2).zip`, commit f2d0fe4fc7d42662e5d42950a30d2e7259ae7449, VERSION 2.3.19-beta.1. O endereço público consultado exibia V2.3.19. Esta é uma entrega incremental das fases de arquitetura e piloto, não a implementação integral de todos os documentos.

## 1. Auditoria da base

A versão recebida usa HTML/CSS/JS sem dependências externas de runtime, um catálogo carregado em `public/app.js`, `selection.js` para seleção, `diagram-state.js` para relacionamentos e `pdf-export.js` para PDF. A atualização da NF-e tem um backend e uma rotina Python/GitHub próprios. Identificamos dependências do nome NF-e em títulos, exportação, armazenamento de seleções, modelagem Oracle e chamadas de atualização. O catálogo NF-e fornecido tem 1.173 registros; o seed offline NF-e legado tem 196. Os arquivos de dados da NF-e, histórico, notificações e snapshots foram mantidos byte a byte. Não reescrevemos o motor hierárquico ou a paginação.

## 2. Fontes e cobertura

- Portal de referência: https://moc.sped.fazenda.pr.gov.br/index.html (material de apoio; não substitui os manuais originais e NTs).
- Site publicado consultado: https://maikonvenicius07.github.io/dfe-data-explorer/public/.
- DC-e: https://moc.sped.fazenda.pr.gov.br/DCe/Leiaute.html, referência NT 2024.001 v.1.21, junho/2026. Modelo 99, manual versão 1.00. O catálogo piloto transcreve 111 linhas de dados estruturais consultadas (ordem, ID, tag, categoria, Pai, tipo, ocorrência, tamanho), incluindo raiz, 16 grupos editoriais e IDs duplicados. Os títulos de grupos são abreviados no piloto. Não equivale à importação integral: descrições e observações não importadas são `n/i`; não são inferidas. As regras e XPaths são baseados nos vínculos documentados, não certificados pelo XSD. A regra de controle RC não recebe XPath presumido. O ID oficial Z06 aparece duas vezes (xCampo e xTexto), sem renumerar; as chaves internas distinguem os registros. Signature permanece vinculada ao pai informado pelo manual, sem corrigir por hipótese.
- O ambiente de execução não conseguiu resolver o domínio do MOC para baixar o HTML bruto, apesar de a consulta web às tabelas estar disponível. Por isso, não foi possível executar o importador contra o HTML real nem importar o pacote XSD nesta entrega. O importador e seu workflow manual estão preparados, com validação em fixture sintética. Nenhuma informação ausente foi apresentada como oficial.

| Documento | Situação |
|---|---|
| NF-e/NFC-e | Catálogo existente e motor preservados; 1.173 registros publicados no ZIP fornecido |
| DC-e | Piloto estrutural, 111 registros; importação integral e XSD pendentes |
| CT-e/CT-e OS/GTVe | Entrada e manual identificados; catálogo pendente |
| NF-e ABI | Pendente |
| NFGAS | Pendente |
| NFAG | Pendente |
| NF3-e | Pendente |
| NFCom | Pendente |
| BP-e | Pendente |
| MDF-e | Pendente |

## 3. Implementação

- `documents.js`: registro de documentos, validação do documento raiz e namespace de conjuntos salvos. Os itens pendentes abrem uma tela informativa, com link do manual, e não habilitam a impressão de outro catálogo.
- `app.js`: troca de catálogo, estado independente em memória por documento (seleção, expansão, filtro MOC, modo, ficha selecionada, histórico/XSD associados); conjuntos salvos em armazenamento local separado; guarda contra resposta assíncrona tardia do backend NF-e; rejeição de JSON com raiz incompatível. Todos os nomes e exportações relevantes passam a usar o documento ativo. Seleção compartilhada dentro do documento e não entre documentos. O documento DC-e usa um catálogo próprio; nada foi copiado da NF-e como se fosse DC-e.
- O comportamento aprovado da NF-e (seta marca registro e filhos diretos) foi preservado; na DC-e a seta apenas expande, conforme a instrução mais recente de não confundir expansão e seleção. Marcar descendentes continua sendo explícito e reversível. O filtro "Exibir somente os selecionados" não muda a seleção. Ao imprimir todo o catálogo DC-e é solicitada confirmação.
- Um painel recolhível dá acesso a árvore, dicionário, diagrama e visualizador XSD, sem restaurar quatro itens duplicados no menu lateral. Os recursos de XSD e XLSX do servidor estão limitados ao documento originalmente suportado; a DC-e não reutiliza seu XSD/SQL. Há proposta Oracle conceitual própria DC_DOCUMENTO/DC_ITEM (não validada para produção).
- `pdf-export.js`: atualização da identificação de versão; o algoritmo de paginação é o mesmo. A impressão principal continua apenas com o MOC e a seleção ativa; o mapa opcional permanece. Catálogo e documento constam no cabeçalho. PDF não imprime registros de outros documentos.
- `import_dce.py`: coleta HTML ou arquivo local, identifica tabelas das dez colunas e valida estrutura, raiz, presença de grupos, quantidade mínima, pais e duplicidade. Registra snapshot anterior, atualiza catálogo DC-e e seed/offline, sem alterar dados NF-e. Validação da extração real e histórico/comparativo/notificação DC-e ainda não habilitados. `importar_dce.yml`: workflow manual, não agendado, para executar a coleta no GitHub.

## 4. Testes executados

- `node --check public/app.js`, `public/documents.js` e gerador PDF: sintaxe.
- 11 testes pytest aprovados: importação NF-e, fixture DC-e (incluindo preservação do ID duplicado e rejeição de conteúdo incompleto/raiz errada), publicação estática. Teste de contrato de navegação atualizado intencionalmente para a nova estrutura, sem remover validações do redirecionamento Pages.
- 3 suítes Node aprovadas: seleção, seleção integrada, diagrama progressivo.
- Teste Chromium `tests/test_multidocument_v2320.py`: carregamento da base NF-e 1.173 por HTML offline com seed real do ZIP; alternância de documentos, estado independente, filtro W, expansão sem seleção da DC-e, seleção de Z06/xCampo sem Z06/xTexto, dicionário contextual, documento pendente e bloqueio de impressão, modelo Oracle separado, seed offline original; quatro PDFs reais produzidos e examinados por texto e visualmente nos exemplos principais. O teste HTTP local foi impedido pela política de rede do navegador (`ERR_BLOCKED_BY_ADMINISTRATOR`), então foi executado com HTML embutido via Playwright; não equivale a teste de Pages ao vivo.
- PDF NF-e W22: mesmo conjunto de 22 registros da V2.3.19, A4 retrato, uma página, mesmos recuos e conectores. PDF DC-e emitente: 17 linhas do Grupo C, A4 paisagem, uma página. PDF DC-e total: W16, sem registros NF-e. Os exemplos estão em `docs/v2320/`.
- A base NF-e foi comparada byte a byte com o ZIP recebido. Nenhum arquivo anterior foi excluído. Testes históricos completos, telefone físico, driver Windows, rede real de coleta e publicação GitHub após atualização não executados. Os 111 registros são cobertura estrutural, não validação integral de conteúdo oficial.

## 5. Atualização no GitHub

1. Descompacte o pacote completo ou o incremental na raiz do repositório (preserve `.github/`, `public/`, `scripts/`, `tests/`, etc.). Não exclua dados/histórico. Faça commit e publique pelo fluxo atual.
2. Verifique no navegador a versão 2.3.20 e teste a NF-e antes de avançar. Abra a DC-e e confira o indicador de cobertura parcial.
3. Para tentar completar descrições e observações, execute no GitHub: Actions → Importar catálogo DC-e (piloto) → Run workflow. Alternativamente use `python scripts/import_dce.py` (internet) ou `python scripts/import_dce.py --html Leiaute_DCe.html`. Se o parser rejeitar a origem, não substitua o catálogo anterior; analise o erro. O workflow ainda não foi executado neste ambiente. Após uma coleta bem-sucedida, publique novamente caso o fluxo automático não dispare.
4. Próximas etapas: validar a importação efetiva da DC-e e respectivos XSD/NT, executar QA em Pages, testar mobile, implementar monitoramento e comparação por documento, depois adicionar os restantes de maneira incremental, começando pela família CT-e conforme a sequência sugerida. A NF3-e também pode ser priorizada por interesse fiscal.

## 6. Arquivos alterados/novos

- `.github/workflows/importar_dce.yml` — novo
- `.github/workflows/validar.yml` — modificado
- `ARQUIVOS_SHA256.txt` — modificado
- `CHANGELOG.md` — modificado
- `README.md` — modificado
- `RELATORIO_TECNICO_V2_3_20.md` — novo
- `VERSION` — modificado
- `docs/v2320/DC_E_EMITENTE_PILOTO.pdf` — novo
- `docs/v2320/DC_E_TOTAL_PILOTO.pdf` — novo
- `docs/v2320/NFE_SELECAO_INDIVIDUAL.pdf` — novo
- `docs/v2320/REGRESSAO_NFE_W22_A4_RETRATO.pdf` — novo
- `public/EXPLORADOR_OFFLINE_COMPLETO.html` — modificado
- `public/app.js` — modificado
- `public/data/dce/catalogo_atual.json` — novo
- `public/documents.js` — novo
- `public/index.html` — modificado
- `public/pdf-export.js` — modificado
- `public/styles.css` — modificado
- `scripts/build_offline.py` — modificado
- `scripts/import_dce.py` — novo
- `tests/test_import_dce.py` — novo
- `tests/test_multidocument_v2320.py` — novo
- `tests/test_publication_v232.py` — modificado
