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
