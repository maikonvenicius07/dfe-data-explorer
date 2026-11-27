# V2.3.22 — Ativar a coleta real

O ZIP enviado continha `.github/workflows/workflows/importar_documentos.yml`. O GitHub não executa workflows nessa subpasta. Não é necessário apagar os arquivos históricos da subpasta. Os arquivos válidos estão diretamente em `.github/workflows/`.

## Opção A — GitHub, sem instalar Python

1. Atualize os arquivos do ZIP a partir da RAIZ do repositório. Não arraste a pasta `workflows` para dentro de `.github/workflows`.
2. Na página https://github.com/maikonvenicius07/dfe-data-explorer/new/main/.github/workflows crie `importar_documentos.yml` se ele ainda não existir. Cole integralmente o conteúdo de `COPIAR_PARA_WORKFLOW_GITHUB.txt` (não cole o nome do arquivo). Se já existir, abra e confira o conteúdo.
3. Confira que o endereço do arquivo termina em `/blob/main/.github/workflows/importar_documentos.yml`, sem `workflows/workflows`.
4. Em Actions, abra **Importar leiautes de todos os DF-e**, selecione Run workflow, main, documento `all` e confirme. A atualização também pode disparar a coleta automaticamente.
5. Abra a execução e veja o passo **Coletar manuais e gerar catálogos**. O relatório `cobertura-documentos` está nos Artifacts. Um resultado vermelho deve ser investigado; os dados anteriores são preservados. Consulte `public/data/importacao_documentos.json` para erros individuais e contagens.
6. Verifique que `public/data/mdfe/catalogo_atual.json` e os demais arquivos realmente foram criados (não apenas a entrada do menu). Se os arquivos não surgirem, consulte o erro de coleta. Se `git push` falhar, verifique permissões do repositório em Settings > Actions > General > Workflow permissions e eventuais regras de proteção de branch. O workflow declara `contents: write`.
7. Em caso de falha na publicação, confira Settings > Pages. Em modo GitHub Actions, execute **Publicar Explorador no GitHub Pages**. Em modo Deploy from a branch, use main / (root) e confira a execução pages-build-deployment. O pacote agora suporta o endereço `/public/`.
8. Confira https://maikonvenicius07.github.io/dfe-data-explorer/public/ (Ctrl+F5). A versão da tela deve ser 2.3.22. A versão não prova importação: abra MDF-e, NF3-e etc. e confira as contagens e os dados reais.

## Opção B — Windows, sem GitHub Actions

Extraia o ZIP completo. Execute `IMPORTAR_LEIAUTES_WINDOWS.cmd`. Requer Python 3 e acesso à internet para instalar as dependências e baixar as páginas oficiais. O script cria um ambiente virtual local; não exige token nem acesso ao GitHub. Pressione Enter para importar `all` e Enter para baixar as fontes. Confira o relatório JSON e abra `public/EXPLORADOR_OFFLINE_COMPLETO.html`. Envie a pasta `public` atualizada a partir da raiz do repositório.

Se a rede impedir o Python de baixar a fonte, abra as páginas Leiaute dos respectivos manuais em seu navegador, salve com Ctrl+S como HTML e informe a pasta ao script. Nomes de arquivo aceitos: `DCe.html`, `CTe.html` (três variantes), `NFe_ABI.html`, `NFGAS.html`, `NFAG.html`, `NF3e.html`, `NFCom.html`, `BPe.html` (três variantes), `MDFe.html`. Também aceita nomes das chaves individuais (ex. `mdfe.html`). Use a página Leiaute, não Visão Geral.

A coleta bruta não foi executada com sucesso no ambiente de criação da versão: rede indisponível. Os catálogos NF-e e DC-e permanecem preservados e os demais não são declarados completos. A importação precisa ser validada com os manuais e XSD. Não envie `.venv` ao GitHub.
