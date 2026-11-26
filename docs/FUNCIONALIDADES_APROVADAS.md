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
- Na Central de Impressão, checkbox de grupo ou subgrupo é uma ação explícita e pode selecionar seus descendentes; somente abrir o nó não seleciona.
- Pais não escolhidos não aparecem como registros na impressão MOC.
- Nenhum documento é impresso se a seleção estiver vazia.
- Prévia lista os itens e permite retirá-los; o usuário escolhe as colunas do MOC, papel e orientação.
- O processo de publicação deverá ser incremental via GitHub e ZIPs completo + modificado + relatório técnico.

- Desde V2.3.12, exceção no Leiaute MOC: expandir pela seta individual marca o nó e seus filhos diretos apresentados na tabela; recolher não desmarca. Expandir tudo, filtros e busca não marcam.

- Desde V2.3.13, somente a seção Leiaute do MOC com registros escolhidos, sem capa, sumário ou demais representações.
