# DF-e Data Explorer — V2.3.26-beta.1

Data: 27/11/2026. Base: `dfe-data-explorer-main (4)(1).zip`, V2.3.25-beta.1, 278 arquivos. Escopo escolhido: confirmar publicação, sem alterar as regras de monitoramento fiscal ou iniciar o monitoramento XSD.

## Diagnóstico

A auditoria anterior constatou que a coleta dos 14 catálogos já foi executada remotamente, mas não havia confirmação de que o pacote publicado correspondia ao conteúdo atualizado no repositório. A consulta pública desta sessão mostra a V2.3.25 no HTML. Isso não confirma todos os arquivos ou o histórico servido. O ZIP-base contém a linha de base anterior à primeira verificação do monitor. Não deve substituir os dados já atualizados no GitHub. A listagem pública de Actions consultada mostrou execuções históricas de validação com falhas, porém a listagem não basta para diagnosticar a causa; não foi possível confirmar os logs completos dessas falhas.

Fontes públicas consultadas: https://maikonvenicius07.github.io/dfe-data-explorer/public/ e https://github.com/maikonvenicius07/dfe-data-explorer/actions .

## Implementação

- `scripts/publication_receipt.py`: gera um comprovante no artefato de Pages com versão completa, commit de origem, data de preparação, data de verificação do monitor, 14 catálogos e hashes SHA-256 de 23 arquivos (HTML, CSS, JavaScript, offline, catálogos e monitoramento). Valida identidade, presença e contagem dos catálogos antes do deploy. A comparação posterior exige que o comprovante remoto seja igual ao local e verifica os bytes de cada arquivo, com query de verificação e tentativas para propagação. Em divergência persistente, a etapa falha explicitamente. O comprovante não é assinatura digital nem prova de completude do manual.
- `.github/workflows/publicar_paginas.yml`: prepara HTML, registro e offline diretamente a partir dos dados do checkout de main. Gera comprovante dentro de `_site/public/`, guarda cópia como artefato; após deploy, utiliza o mesmo commit para verificar o endereço retornado pelo Pages, incluindo `/public/`. As publicações são serializadas pelo grupo de concorrência existente.
- `.github/workflows/importar_documentos.yml`: mantém horário, coleta, proteções, histórico, e-mail opcional e solicitação explícita de publicação. No modo branch, sinaliza que a solicitação não possui comprovação do novo mecanismo; usar Settings > Pages > Source > GitHub Actions. O workflow de importação não aguarda o resultado do workflow de publicação; devem ser conferidos separadamente.
- `public/app.js` / `public/index.html`: Central de Atualizações consulta `publicacao.json`, compara a versão da página e o SHA-256 dos bytes do monitor recebido; mensagens distintas para ausência, divergência, cópia offline ou verificação não suportada. Isso comprova somente o monitor recebido na sessão; a conferência dos demais arquivos é feita pelo workflow.
- `public/pdf-export.js`: somente identificação de versão; regras de PDF intactas. CSS, seleção, hierarquia, diagrama e importadores mantidos. `public/EXPLORADOR_OFFLINE_COMPLETO.html` regenerado a partir da base enviada; publicação reconstrói com os dados atuais do repositório.
- `.github/workflows/validar.yml`: inclui os novos testes. `COPIAR_PARA_WORKFLOW_GITHUB.txt` sincronizado com o workflow real. `VERSION`, `README.md`, `CHANGELOG.md`, `LEIA_PRIMEIRO_V2326.md` e este relatório atualizados.

## Testes executados

- 49/49 testes Python (test_import.py, test_import_documents_v2321.py, test_import_dce.py, test_monitor_documents_v2325.py, test_release_v2324.py, test_deployment_v2322.py, test_publication_v232.py e test_publication_receipt_v2326.py). Novos testes: comparação de bytes reais dos 23 arquivos por transporte simulado, rejeição de commit antigo, monitor divergente, MDF-e divergente, identidade/contagem incorretas, ordem de etapas do workflow.
- Quatro suítes JS existentes aprovadas e sintaxe dos cinco JS verificada com Node. Cinco workflows principais carregados como YAML válido (isso não substitui execução real no GitHub).
- Chromium: `tests/test_browser_publication_v2326.py` — 14 linhas na Central, mensagens de monitoramento correspondente/divergente, versão antiga, falta do comprovante e recuperação; seleção ao expandir e geração real de PDF de 22 registros W, uma página A4 retrato, rotação zero, texto extraível e todos os IDs presentes; nenhum erro JavaScript nesses cenários. Navegação HTTPS do sandbox foi bloqueada; a versão aprovada do teste injeta respostas e usa ponte SHA-256 para Python quando WebCrypto não está disponível. Portanto não comprova navegação HTTPS real nem WebCrypto nativo. Não foi executada a suíte histórica completa de navegador ou a impressão física.
- Comprovante local gerado para os 14 catálogos, 23 arquivos; arquivo de teste retirado do diretório de publicação antes da entrega. Nenhuma prova falsa de deploy foi distribuída.
- Todos os arquivos `data/` e `public/data/` são byte a byte idênticos ao ZIP-base, total de 5.830 registros na base enviada. Nenhum arquivo anterior excluído.

## Instalação e limitações

Usar preferencialmente o ZIP incremental, no diretório raiz do repositório. Ele não contém os diretórios de dados. O HTML offline é derivado do ZIP-base e será reconstruído no workflow; para offline local, regenerar com `python scripts/prepare_release.py` sobre os dados atuais. O ZIP completo é apenas backup executável do estado fornecido, não deve substituir a base mais recente do GitHub. Não criar pasta `.github/workflows/workflows/`; as cópias históricas já presentes são inertes e foram preservadas. Selecionar Settings > Pages > Source > GitHub Actions. Executar `Publicar Explorador no GitHub Pages` e verificar a etapa `Confirmar versão e catálogos no endereço público`. Depois consultar Central de Atualizações no site.

O download de fontes e a execução remota do novo workflow não foram realizados neste ambiente (DNS indisponível para conexão direta; consulta pública feita por ferramenta de pesquisa). A execução por agendamento ainda não foi comprovada. A nova verificação pode falhar por propagação ou indisponibilidade externa, sem indicar que os dados fiscais foram perdidos. A importação de XSD e seu monitoramento automático continuam pendentes. Não alteramos o cron 07:17 de Rondônia, nem as regras de aprovação de mudanças na documentação.

## Arquivos novos/modificados

- `.github/workflows/importar_documentos.yml`
- `.github/workflows/publicar_paginas.yml`
- `.github/workflows/validar.yml`
- `ARQUIVOS_SHA256.txt`
- `CHANGELOG.md`
- `COPIAR_PARA_WORKFLOW_GITHUB.txt`
- `LEIA_PRIMEIRO_V2326.md` (novo)
- `README.md`
- `RELATORIO_TECNICO_V2_3_26.md` (novo)
- `VERSION`
- `public/EXPLORADOR_OFFLINE_COMPLETO.html`
- `public/app.js`
- `public/index.html`
- `public/pdf-export.js`
- `scripts/publication_receipt.py` (novo)
- `tests/test_browser_publication_v2326.py` (novo)
- `tests/test_publication_receipt_v2326.py` (novo)
