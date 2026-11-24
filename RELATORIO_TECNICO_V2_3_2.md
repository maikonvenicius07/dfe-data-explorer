# Relatório técnico — DF-e Data Explorer V2.3.2-beta.1

**Data:** 24/11/2026  
**Origem:** ZIP enviado pelo usuário `dfe-data-explorer-main.zip`, já na V2.3.1-beta.1.  
**Tipo:** atualização incremental de publicação, sem reconstrução da interface.

## 1. Solicitação e diagnóstico

O pedido é **remover somente “Visão Geral”**, mantendo as outras janelas. A análise dos arquivos confirma que a V2.3.1 já preservava exatamente as seguintes oito áreas: Leiaute do MOC, Explorador Hierárquico, Dicionário de Dados, Diagrama XML, Visualizador XSD, Modelagem Oracle, Atualizações e Histórico, Central de Impressão. O Leiaute do MOC já era a tela inicial.

A investigação do endereço público `https://maikonvenicius07.github.io/dfe-data-explorer/` constatou que o conteúdo exibido era o README do repositório em vez da interface do aplicativo. A evidência é consistente com a configuração de GitHub Pages mostrada pelo usuário: **Deploy from a branch**, `main` e **/ (root)**, enquanto o aplicativo está localizado em `public/index.html`.

Portanto, **não havia motivo para remover, recriar ou modificar as oito telas existentes**. A correção necessária é assegurar que o endereço principal abra a aplicação, tanto com publicação pela branch quanto via workflow de GitHub Actions.

## 2. Correções aplicadas

1. **Novo `index.html` na raiz:** encaminha automaticamente para `./public/` no modo Pages `main / (root)`; contém link manual acessível caso o redirecionamento não ocorra.
2. **Novo `.nojekyll` na raiz:** evita processamento Jekyll dos arquivos publicados via branch.
3. **`.github/workflows/publicar_paginas.yml`:** mantém publicação de `public/` no GitHub Actions e também é acionado quando o novo arquivo raiz muda.
4. **`.github/workflows/validar.yml`:** executa novo teste de regressão para prevenir a remoção indevida de menus e telas.
5. **`tests/test_publication_v232.py`:** verifica as oito janelas nos HTMLs do site e offline, confirma MOC inicial, ausência da Visão Geral, redirecionamento na raiz e artefato de publicação.
6. **Documentação, CHANGELOG, VERSION e hash de integridade:** alinhados à V2.3.2.

**Nenhuma alteração** em `public/index.html`, `public/app.js`, `public/styles.css`, `public/selection.js`, `public/EXPLORADOR_OFFLINE_COMPLETO.html` ou `public/catalogo_selecao_anterior.json`. As funções do aplicativo e todos os 196 nós demonstrativos permanecem inalterados.

## 3. Arquivos criados ou modificados

| Arquivo | Situação | Finalidade |
|---|---|---|
| `index.html` | Novo | Entrada do GitHub Pages para publicação da raiz |
| `.nojekyll` | Novo | Impedir tratamento Jekyll na publicação da branch |
| `tests/test_publication_v232.py` | Novo | Regressão do menu e da entrada do site |
| `.github/workflows/publicar_paginas.yml` | Alterado | Gatilho adicional para a entrada da raiz |
| `.github/workflows/validar.yml` | Alterado | Executar o novo teste de regressão |
| `VERSION` | Alterado | V2.3.2-beta.1 |
| `CHANGELOG.md` | Alterado | Histórico da correção |
| `README.md` | Alterado | Instruções do endereço público e comportamento esperado |
| `docs/PUBLICACAO_GITHUB.md` | Alterado | Documentação de Pages branch e GitHub Actions |
| `ARQUIVOS_SHA256.txt` | Alterado | Manifesto dos arquivos atuais |
| `RELATORIO_TECNICO_V2_3_2.md` | Novo | Este relatório |

**Arquivos excluídos:** nenhum.

## 4. Testes executados

- `python -m pytest -q tests/test_publication_v232.py tests/test_import.py`: **9 testes aprovados**.
- `node --check public/app.js`: **aprovado**.
- `node --check public/selection.js`: **aprovado**.
- `node tests/test_selection_logic_v23.js`: **aprovado**.
- `python tests/test_no_overview_v231.py`: **aprovado**; oito janelas presentes, MOC como tela inicial, 196 nós exibidos, impressão e diagramas acessíveis.
- `python tests/test_fullscreen_only_v221.py`: **aprovado**; botão Tela cheia preservado, quatro formatos, MOC e impressão intactos.
- Inspeção dos ZIPs e SHA-256: **todos os arquivos incrementais coincidem com os correspondentes do ZIP completo**.

**Limitação:** a tentativa de abrir um endereço HTTP local no Chromium automatizado foi bloqueada pelo ambiente (`ERR_BLOCKED_BY_ADMINISTRATOR`). A rota de entrada foi verificada estaticamente e com inspeção da estrutura HTML; o redirecionamento não foi certificado em um navegador real no GitHub Pages. A publicação remota não foi efetuada nesta execução.

## 5. Como atualizar o GitHub Desktop

1. Extrair `EXPLORADOR_NFE_NFCE_V2_3_2_MODIFICADOS.zip`.
2. No GitHub Desktop, clicar **Repository → Show in Explorer**.
3. Copiar **o conteúdo** do ZIP incremental para a raiz da pasta local `dfe-data-explorer`, preservando `.github/workflows`, `docs` e `tests` e confirmando a substituição dos arquivos existentes. **Não copiar a pasta externa que o extrator eventualmente criar**.
4. Confirmar que `index.html` está na raiz, ao lado do `README.md`, e que `public/index.html` continua no subdiretório `public`.
5. Fazer commit `V2.3.2 - Preservar oito telas e corrigir abertura do site` e clicar **Push origin**.
6. Verificar Actions e abrir `https://maikonvenicius07.github.io/dfe-data-explorer/`. Se aparecer versão anterior, atualizar com `Ctrl+F5`.
7. Recomenda-se **Settings → Pages → Source → GitHub Actions**, para evitar concorrência entre a publicação da branch e o workflow. Se o usuário preferir manter `Deploy from a branch`, `main / (root)`, o novo arquivo raiz encaminha a `public/`.

## 6. Verificações posteriores à publicação

O site deve abrir no **Leiaute do MOC**. O menu lateral deve apresentar exatamente oito janelas e nenhuma opção “Visão Geral”. Testar navegação por todas as abas, hierarquia do Grupo W, Diagrama XML, dicionário e Central de Impressão. Se a raiz não carregar a interface, verificar diretamente `/dfe-data-explorer/public/` e conferir o método selecionado em Settings → Pages.

## 7. Limitações mantidas

O catálogo embutido possui **196 nós demonstrativos**. A importação integral do MOC, validação oficial XSD e o monitoramento efetivo de atualizações não são objeto desta correção. Nenhum dado de contribuinte, banco Oracle ou regra fiscal foi modificado.
