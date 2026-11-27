# DF-e Data Explorer — V2.3.27-beta.1

## Objetivo e base
Alteração pontual solicitada: deixar todos os grupos e subgrupos recolhidos no Leiaute MOC. Base: ZIP completo V2.3.26, 283 arquivos. Esta versão prioriza o pedido de interface; o monitoramento de XSD anteriormente planejado permanece pendente.

## Diagnóstico e correção
- `public/app.js`, função `normalize`: a inicialização populava `mocOpen` com todos os grupos e `mocNodeOpen` com os nós que possuem filhos. Agora os dois conjuntos iniciam vazios para cada catálogo aberto pela primeira vez.
- `public/app.js`, controles de `renderMoc`: o botão de recolhimento fechava os subgrupos mas reabria os grupos editoriais. Agora fecha ambos sem alterar a seleção.
- `public/app.js`, eventos de pesquisa e filtro: uma pesquisa não vazia revela os grupos que correspondem à busca; escolher um grupo no filtro abre o respectivo grupo. Nenhuma dessas ações marca campos. Expandir manualmente uma linha mantém a seleção progressiva já aprovada. Expandir tudo continua sendo apenas visual. A abertura de um título editorial não marca campos.
- Preservado o estado de navegação ao retornar a um documento já visitado na mesma sessão. O comando Recolher tudo permite fechá-lo novamente. Recarregar a página inicia recolhido.
- `public/index.html`: botão renomeado para Recolher tudo; referências de assets e número de versão atualizados. `public/pdf-export.js`: somente identificação da versão; algoritmo de PDF intacto.
- `public/EXPLORADOR_OFFLINE_COMPLETO.html`: regenerado com os dados da base fornecida. Publicação reconstrói o HTML com os catálogos atuais do repositório.

## Testes efetivamente realizados
- 49/49 testes Python de importação, monitoramento, preparação e publicação aprovados.
- Quatro suítes JavaScript aprovadas. Sintaxe de app.js e pdf-export.js conferida por Node.
- `tests/test_collapsed_moc_v2327.py`: Chromium com respostas de rede injetadas e os 14 catálogos reais da base. Confirmados grupos iniciais recolhidos, ausência de subgrupos abertos, expansão do título de cada documento, seleção progressiva na NF-e, pesquisa, filtro, expansão global sem seleção, recolhimento global sem desmarcar, retorno à NF-e com seleção e filtro preservados. Testado JSON auxiliar inválido. Gerado PDF real de 22 registros do Grupo W, com todos os IDs, uma página A4 retrato, rotação zero e texto extraível. HTML offline testado com grupos inicialmente fechados. Sem erros JavaScript nos cenários executados.
- Os testes históricos de navegador que pressupõem o comportamento anterior do botão Recolher subgrupos não foram reexecutados nesta etapa. Não foram realizados testes físicos de impressão, acesso HTTPS real, publicação remota ou execução do agendamento diário.

## Arquivos novos ou modificados
- `public/app.js`, `public/index.html`, `public/pdf-export.js`, `public/EXPLORADOR_OFFLINE_COMPLETO.html`
- `VERSION`, `CHANGELOG.md`, `README.md`, `ARQUIVOS_SHA256.txt`
- `tests/test_collapsed_moc_v2327.py` (novo), `RELATORIO_TECNICO_V2_3_27.md` (novo)

Nenhum arquivo excluído. Catálogos e diretórios de dados preservados byte a byte. Workflows, estilos, hierarquia e regras de impressão não foram modificados. O monitoramento e a publicação automática da versão anterior permanecem intactos.

## Instalação
Preferir o ZIP incremental no diretório raiz do repositório, pois não contém os diretórios de dados, evitando sobrescrever o histórico atualizado no GitHub. Os HTMLs derivados do ZIP-base podem conter dados anteriores aos mais recentes do GitHub; o workflow de publicação regenera esses artefatos com os dados atuais do checkout. Para uso offline com os dados atuais, executar `python scripts/prepare_release.py`. Após publicação, Ctrl+F5 e conferir a V2.3.27. O ZIP completo é backup da base utilizada nesta implementação, não substituto dos dados remotos mais recentes.
