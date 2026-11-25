# DF-e Data Explorer — Conferência do ZIP e correção V2.3.6-beta.1

**Data:** 25/11/2026  
**Fonte examinada:** `dfe-data-explorer-main (1).zip`, versão identificada `2.3.5-beta.1`  
**Objetivo:** corrigir a validação de publicação no GitHub sem modificar as funcionalidades do aplicativo.

## Diagnóstico comprovado

O teste `tests/test_publication_v232.py` foi executado contra o ZIP enviado: **2 testes passaram e 1 falhou**. A causa é a ausência da linha `      - 'index.html'` nos filtros `on.push.paths` do arquivo `.github/workflows/publicar_paginas.yml`. A ação `actions/upload-pages-artifact@v4` já estava correta no ZIP recebido; portanto, não foi necessário alterar sua versão.

O ZIP enviado permanece na V2.3.5, ou seja, a V2.3.6 que tinha sido preparada anteriormente ainda não está presente nesse arquivo. O registro público de GitHub Actions em 25/11/2026 também indicava uma falha na validação, enquanto a publicação havia passado.

## Correção mínima

- `.github/workflows/publicar_paginas.yml` — adicionados `index.html` e `.nojekyll` aos caminhos de disparo, mantendo a configuração de publicação de `public/` e as ações existentes.
- `VERSION` — atualizado para `2.3.6-beta.1`.
- `README.md` — versão atualizada sem alterar as instruções.
- `CHANGELOG.md` — registrada a alteração.
- `RELATORIO_TECNICO_V2_3_6.md` — este relatório criado.
- `ARQUIVOS_SHA256.txt` — catálogo de checksums regenerado (sem autochecksum).

Nenhum arquivo foi excluído. Os ZIPs contêm os caminhos originais, com conteúdo binário idêntico entre os arquivos comuns do ZIP incremental e do completo.

## Verificações executadas

| Verificação | Resultado |
|---|---|
| `python -m pytest -q tests/test_publication_v232.py` antes da correção | **Falhou:** 2 passaram, 1 falhou |
| Testes de publicação e importação após a correção (`test_publication_v232.py` e `test_import.py`) | **9 aprovados** |
| `node tests/test_selection_logic_v23.js` | Aprovado |
| `node tests/test_integrated_selection_v235.js` | Aprovado |
| `node tests/test_diagram_progressive_v234.js` | Aprovado |
| Verificação de sintaxe dos 3 arquivos JavaScript principais (`node --check`) | Aprovada |
| `python scripts/build_offline.py` | Executado; gerou HTML independente |
| Suíte gráfica legada completa | **Pendente:** execução ultrapassou o limite do ambiente |
| Publicação na conta GitHub do usuário | **Não executada** nesta revisão |

## Funcionalidades preservadas

As oito janelas permanecem no HTML; não foi alterado `public/app.js`, `public/selection.js`, `public/diagram-state.js`, `public/index.html`, banco, XML, MOC, impressão ou exportações. A seleção integrada entre MOC, Árvore, Dicionário e Diagrama permanece como estava na V2.3.5.

## Como publicar usando GitHub Desktop

1. Baixe o ZIP incremental **V2.3.6** e extraia seu conteúdo.
2. No GitHub Desktop, acesse **Repository → Show in Explorer**.
3. Copie os arquivos e pastas extraídos para a raiz local `dfe-data-explorer`, substituindo os correspondentes; preserve os caminhos internos e não coloque uma segunda pasta dentro da raiz.
4. Confira que `.github/workflows/publicar_paginas.yml` e `VERSION` constam como modificados.
5. Escreva `V2.3.6 - Corrigir validação de publicação` no campo Summary e faça **Commit to main** e **Push origin**.
6. Em **Actions**, confira **Validar código e seleção** e **Publicar Explorador no GitHub Pages**. O resultado remoto depende do ambiente GitHub.
7. Em **Settings → Pages → Source**, prefira **GitHub Actions** para evitar mecanismos de publicação concorrentes.
8. Abra `https://maikonvenicius07.github.io/dfe-data-explorer/` e valide menu, seleção e impressão.

## Limitações e riscos

- A documentação fiscal permanece demonstrativa com 196 nós, sem cobertura integral do MOC/XSD.
- A existência de `publicar_paginas.yml` na raiz do ZIP não ativa um workflow; o arquivo efetivo do GitHub Actions fica em `.github/workflows/`.
- Esta análise não verifica o conteúdo de alterações que tenham sido publicadas depois do ZIP enviado; não substitua indiscriminadamente outros arquivos editados no GitHub.
- Não foi comprovado que a execução remota no GitHub Pages foi aprovada após esta correção.
