## V2.3.6-beta.1 — GitHub Pages e validação (25/11/2026)

- Corrigidos os gatilhos de `index.html` e `.nojekyll` em `.github/workflows/publicar_paginas.yml`.
- Preservada a ação `actions/upload-pages-artifact@v4` e a publicação `actions/deploy-pages@v4`.
- Nenhuma alteração no código das oito janelas, no catálogo ou na seleção integrada.

# V2.3.5-beta.1 — seleção única e relatório integrado (25/11/2026)

- Integrados os checkboxes de seleção nos quatro módulos MOC, Árvore XML, Dicionário e Diagrama SVG.
- Distinguidas as ações: filtrar, expandir, marcar nó isolado e selecionar descendentes de forma explícita.
- Adicionado controle individual em cada cartão SVG, estado sincronizado e contagem de seleção.
- Ajustada a árvore de seleção para não repetir grupos quando o pai pertence a grupo editorial diferente.
- Central de Impressão: quatro seções independentes, todas ativas inicialmente, com prévia integral e remoção de campos.
- MOC e dicionário imprimem apenas registros marcados; árvore e diagrama exibem ancestrais exclusivamente como contexto.
- Incluído modo explícito para imprimir todos os registros do catálogo carregado, sem alterar a seleção manual.
- Ajustadas quebras de página, capa e sumário; PDF de teste B02/W38 A4 paisagem, seis páginas e texto pesquisável.
- Acrescentado teste de regressão Node e atualizada automação de validação do GitHub.
- Preservadas as oito janelas e a base demonstrativa de 196 nós. A importação integral do MOC e XSD permanece pendente.

# V2.3.4 — expansão progressiva e três modos distintos de impressão (2026-11-24)

- Corrigido o diagrama de profundidade fixa: expansão `+ / −` individual por ramificação, com estado preservado ao alternar formatos.
- Visão inicial resumida, expansão de ancestrais na pesquisa, expansão total apenas por ação explícita.
- Três modos de impressão independentes: visualização atual, catálogo completo e seleção manual; sem modificar os nós abertos ao imprimir.
- Prévia e impressão usam os mesmos registros; PDF usa cartões hierárquicos pagináveis, texto pesquisável, recuos e referência de grupo por página.
- Corrigido o bloqueio da impressão atual quando nenhum campo estava marcado manualmente.
- Nova lógica isolada em `diagram-state.js`, com teste Node e CI atualizado.
- Gerado PDF de exemplo do Grupo W e PDF do catálogo disponível (196 nós). Não representa cobertura oficial completa.
- Nenhuma tela anterior, dado, regra de impressão selecionada nem banco de dados foi removido.

# V2.3.3 — seleção manual independente de filtros (2026-11-24)

- Removida a seleção inicial automática de todos os 196 registros.
- Dicionário: filtro por subgrupo, checkbox por campo, checkbox coletivo e estado parcial, botões de seleção filtrada/toda a base e visualização apenas de selecionados.
- Seleção compartilhada entre dicionário, MOC, árvore, diagrama e Central de Impressão, sem eliminar marcações anteriores.
- Impressão: exclusividade do conjunto marcado, bloqueio se vazio, prévia com remoção de itens e seleção de colunas MOC.
- Elementos de contexto não contam como selecionados; chaves internas diferenciam ocorrências homônimas quando houver informação de caminho.
- Testes de fluxo com B02/W38, validação do PDF, regressões de navegação e testes estáticos.
- Preservadas as oito telas e o leiaute conhecido, sem migração de dados.

# Histórico de versões

## V2.3.2-beta.1 — 24/11/2026

- Ajustada entrada do GitHub Pages quando a publicação está configurada como `main / (root)`: novo `index.html` na raiz encaminha ao aplicativo em `public/`.
- Adicionado `.nojekyll` para evitar processamento Jekyll da entrada no modo branch.
- Incluído o arquivo raiz no gatilho do workflow de publicação via GitHub Actions, sem modificar a estrutura do aplicativo.
- Incluído teste de regressão para verificar que as **oito janelas restantes** aparecem no menu e possuem telas correspondentes nos dois HTMLs, com `Leiaute do MOC` como tela inicial e **sem Visão Geral**.
- Preservadas integralmente as telas existentes, o catálogo demonstrativo, as regras de impressão, diagramas e JavaScript do aplicativo.


## V2.3.1-beta.1 — 24/11/2026

- Removida a página **Visão Geral** e seu item de navegação.
- Tela inicial alterada para **Leiaute do MOC**.
- Removidas as chamadas do painel executivo que deixaram de ter interface.
- Atualizados testes e HTML offline independente.
- Preservados catálogo, diagrama, explorador, dicionário e Central de Impressão.
- No pacote completo, mantido o workflow de GitHub Pages já corrigido e aprovado no repositório, sem incluí-lo na atualização incremental.


## V2.3.0-beta.1 — 24/11/2026

**Base:** V2.2.1. Não houve reconstrução do sistema.

- Nova Visão Geral com indicadores calculados, distribuição por grupos, profundidade hierárquica e modo apresentação.
- Central de Impressão com árvore selecionável, suporte a níveis internos e elementos individuais; seleção parcial e múltiplos grupos.
- Salvar, carregar e excluir conjuntos de impressão em `localStorage` com validação de chaves existentes.
- Dicionário com ordenação, escolha de colunas e seleção de campos para impressão; CSV respeita filtros e colunas visíveis.
- Prévia/PDF limitados à seleção; nós pais não selecionados incluídos apenas como **contexto** e diferenciados visualmente.
- Link de impressão a partir da ficha do explorador; impressão por campos filtrados do dicionário.
- Publicação preparada para GitHub Pages; fallback para JSON versionado em site estático, scripts de geração HTML offline e cópia de snapshots.
- Adicionados testes automatizados de seleção e fluxo de impressão; registros técnicos e instruções de publicação.

**Permanecem pendentes:** importação integral do MOC e dos XSD oficiais, confirmação de deploy real, XLSX filtrado, histórico agendado em hospedagem. Nenhum banco de produção foi modificado.

## Versões anteriores

Consultar `RELATORIO_TECNICO_V2.md`, `RELATORIO_TECNICO_V2_1.md`, `RELATORIO_TECNICO_V2_2.md` e `RELATORIO_TECNICO_V2_2_1.md` incluídos para preservar o histórico.
