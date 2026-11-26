# Funcionalidades preservadas e regras aprovadas — V2.3.3

- O MOC é a tela inicial; **Visão Geral foi removida** por solicitação expressa.
- Desde V2.3.10, manter apenas quatro telas acessíveis (MOC, Oracle, atualizações, impressão). Os quatro módulos retirados do menu permanecem internos; seus mecanismos permanecem internos.
- DER proposto na Modelagem Oracle; desde V2.3.13, somente MOC na impressão.
- Desde V2.3.11, não exibir a faixa redundante de atalhos “Divisões XML neste grupo”; a navegação interna ocorre pela tabela hierárquica.
- MOC com dez colunas, três modalidades de apresentação e hierarquia por vínculo pai-filho.
- O catálogo de 196 nós é **parcial** e jamais deve ser declarado integralmente oficial.
- A seleção para impressão começa **vazia** e nunca deriva automaticamente dos filtros.
- Cada checkbox na tabela do dicionário representa **somente o campo correspondente**.
- O checkbox do cabeçalho seleciona/desmarca os itens exibidos pelos filtros atuais; estado parcial visível.
- Alterar filtros, grupos, subgrupos, busca, ordenação ou tela não apaga o conjunto selecionado.
- “Imprimir selecionados” usa exclusivamente o conjunto escolhido independentemente do filtro atual.
- Desde V2.3.14, seleção de campos no MOC; a Central não repete a árvore de seleção.
- Pais não escolhidos não aparecem como registros na impressão MOC.
- Nenhum documento é impresso se a seleção estiver vazia.
- Prévia apresenta a tabela uma única vez e permite retirar registros diretamente de suas linhas; o usuário escolhe colunas, papel e orientação.
- O processo de publicação deverá ser incremental via GitHub e ZIPs completo + modificado + relatório técnico.

- Desde V2.3.12, exceção no Leiaute MOC: expandir pela seta individual marca o nó e seus filhos diretos apresentados na tabela; recolher não desmarca. Expandir tudo, filtros e busca não marcam.

- Desde V2.3.13, somente a seção Leiaute do MOC com registros escolhidos, sem capa, sumário ou demais representações.

- Desde V2.3.15, prévia e PDF MOC preservam a mesma profundidade hierárquica da tabela de tela, sem adicionar pais não selecionados como linhas. Os títulos editoriais e cabeçalhos repetem-se na paginação.

- Desde V2.3.16, a impressão MOC mostra linhas de árvore contínuas e término dos ramos, com profundidade original, pais ausentes apenas como contexto textual, e cabeçalhos de continuação. Nenhuma seção além do MOC é incluída.

- V2.3.17: tabela MOC por faixas estruturais com conectores contínuos e encerramentos de ramos; mapa opcional desmarcado inicialmente, sem reintroduzir telas. Versão da aplicação identificada na saída PDF.
