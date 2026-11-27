> **V2.3.29-beta.1 — recuperação conservadora de vínculos hierárquicos do MOC.** A projeção usa escopo de tabelas e Tipo=G de pgto, preserva as chaves e sinaliza pendências que precisam de XSD. Consulte o relatório técnico.

> **V2.3.28-beta.1 — monitor de publicações e pacotes XSD.** Verificação diária integrada ao workflow multidocumento. A leitura integral dos pacotes oficiais ainda depende de acesso às fontes e links de download; a central diferencia publicação localizada, pacote lido e falha. O MOC não é sobrescrito pelos XSD. Consulte `RELATORIO_TECNICO_V2_3_28.md`.

> **V2.3.27-beta.1 — navegação inicial recolhida.** Todos os grupos e subgrupos do Leiaute MOC começam fechados na primeira abertura de cada documento. Recolher tudo fecha a estrutura sem desmarcar a seleção. Pesquisa e filtro explícito revelam os grupos correspondentes.

> **V2.3.26-beta.1 — comprovante e verificação pública da publicação; monitoramento diário preservado.** Os 14 catálogos existentes são preservados. O workflow `Importar leiautes de todos os DF-e` verifica as dez fontes HTML diariamente às 07:17 de Rondônia (11:17 UTC), compara registros e referências técnicas, guarda snapshots, publica alterações aprovadas e registra falhas por documento. Consulte [LEIA_PRIMEIRO_V2325.md](LEIA_PRIMEIRO_V2325.md). A primeira execução real no GitHub ainda precisa ser confirmada; validação XSD continua separada.

> **V2.3.24-beta.1 — correção da inicialização e publicação.** A página inicial usa a base NF-e disponível no pacote, os demais catálogos continuam separados e são carregados sob demanda. Consulte `RELATORIO_TECNICO_V2_3_24.md`.

> **V2.3.23-beta.1 — padronização multidocumento.** Os 14 catálogos presentes no ZIP (5.830 registros) usam o leiaute compartilhado, seleção progressiva e impressão. Os dados originais foram preservados; vínculos não confirmados são sinalizados. Consulte `RELATORIO_TECNICO_V2_3_23.md`.

> **V2.3.22-beta.1:** leia [LEIA_PRIMEIRO_V2322.md](LEIA_PRIMEIRO_V2322.md) para instalar e executar os workflows no diretório correto. A disponibilização dos novos leiautes depende da coleta real e validação dos catálogos.

# DF-e Data Explorer — plataforma multidocumento

**Versão do aplicativo:** V2.3.29-beta.1 · **Base embutida:** catálogo NF-e/NFC-e com 1.173 registros; demais catálogos independentes.

> Projeto independente de documentação técnica. Não é uma publicação oficial do Fisco. A fonte de referência é o [MOC NF-e/NFC-e](https://moc.sped.fazenda.pr.gov.br/NFe_NFCe/Leiaute.html). Nenhum resultado do catálogo parcial deve ser confundido com cobertura oficial completa.

## Abrir imediatamente

Abra o endereço principal `https://maikonvenicius07.github.io/dfe-data-explorer/` no navegador. Em GitHub Pages configurado pela branch `main` e `/ (root)`, o arquivo `index.html` da raiz encaminha automaticamente para `public/`, onde está o explorador de documentos. Também é possível abrir `public/EXPLORADOR_OFFLINE_COMPLETO.html` no navegador. Não necessita instalar nada. Também é possível executar `python scripts/serve.py` e acessar `http://localhost:8000`, para usar o servidor opcional.

## V2.3.21 — importação multidocumento (entrega parcial)

A arquitetura agora busca catálogos próprios de cada documento e variante. A coleta real nesta sessão falhou por DNS no ambiente de execução. Nenhum novo catálogo fiscal foi disponibilizado; NF-e/NFC-e e DC-e piloto permanecem intactos.

1. Atualize o repositório `main` com o conteúdo do ZIP completo na raiz, inclusive `.github/workflows/` e `public/`.
2. Abra **Actions → Importar leiautes de todos os DF-e → Run workflow**, com `documento=all`. Também é possível escolher uma chave específica (`mdfe`, `nf3e`, `cte`, `cteos`, `gtve`, `abi`, `nfgas`, `nfag`, `nfcom`, `bpe`, `bpetm`, `bpeta`, `dce`). O workflow tenta executar a coleta também após alteração do importador na branch main.
3. Confira o log e o artefato `cobertura-documentos`. Um status de erro NÃO significa importação concluída. As fontes precisam estar acessíveis ao runner; a primeira importação real deve ser auditada. O workflow preserva catálogos anteriores em falhas detectadas.
4. Confira o commit dos catálogos, o status da publicação e a URL `public/`. Se necessário, solicite manualmente **Publicar Explorador no GitHub Pages** (para configuração por Actions) ou a republicação da branch main (para configuração por branch).
5. Alternativa local: `pip install -r requirements.txt` e `python scripts/import_documents.py` em uma máquina com rede. Com páginas Leiaute salvas em HTML: `python scripts/import_documents.py --html-dir pasta`. Nomeie os arquivos por chave (`mdfe.html`, `nf3e.html` etc.) ou pela pasta original do manual (`MDFe.html`, `NF3e.html`, `CTe.html`, `BPe.html`, `DCe.html` etc.).

O importador genérico ainda não foi validado contra os HTML integrais reais nem os XSD. Os testes dos novos documentos utilizaram exclusivamente fixtures, que não são distribuídas como catálogos fiscais. Consulte `RELATORIO_TECNICO_V2_3_21.md`.

## V2.3.20 — primeira etapa da expansão

A NF-e/NFC-e continua sendo o documento inicial, com o catálogo publicado original intacto (1.173 registros). A DC-e (modelo 99) possui um catálogo estrutural piloto de 111 registros em 16 grupos, baseado nas tabelas do [MOC on-line da DC-e](https://moc.sped.fazenda.pr.gov.br/DCe/Leiaute.html), referência NT 2024.001 v.1.21. Descrições e observações ainda não foram importadas; `n/i` sinaliza essa limitação. O XSD ainda não foi validado. Os demais oito itens de navegação mostram a situação pendente e o link do respectivo manual, sem reutilizar os dados de outro documento.

Seleções, ramificações abertas, filtro principal e conjuntos salvos são separados por documento. A expansão individual da NF-e preserva a seleção progressiva aprovada; na DC-e, expansão e seleção são independentes, conforme a nova especificação. Consultas técnicas (árvore, dicionário, diagrama e XSD) estão acessíveis em um painel recolhível do leiaute ativo. A Central de Impressão utiliza o mesmo motor da V2.3.19, apenas com a identificação do documento ativo.

### Completar o catálogo DC-e

1. No GitHub, publique os arquivos da versão e abra **Actions → Importar catálogo DC-e (piloto) → Run workflow**. A rotina precisa de acesso à internet e permissão de escrita. Se a coleta falhar, o catálogo anterior permanece disponível.
2. Alternativamente, execute `pip install -r requirements.txt` e `python scripts/import_dce.py` em um ambiente com internet. Para um HTML previamente salvo do manual, execute `python scripts/import_dce.py --html Leiaute_DCe.html`.
3. Após o sucesso, publique as alterações em `public/` conforme a configuração atual do Pages. Se utilizar workflow de publicação e ele não for disparado pelo commit automatizado, execute **Publicar Explorador no GitHub Pages** manualmente.
4. Confirme a cobertura e a versão exibidas na interface. O importador do HTML não valida automaticamente o pacote XSD nem os manuais originais. A verificação automática agendada permanece exclusiva da NF-e nesta fase.

## Recursos preservados e ampliados

- A aplicação abre diretamente no Leiaute do MOC; a tela Visão Geral foi retirada por solicitação do usuário.
- Leiaute MOC nas dez colunas e modo hierárquico com subgrupos.
- Navegação simplificada: MOC, Modelagem Oracle, Atualizações e histórico e Central de impressão. Os módulos de árvore, dicionário, diagrama e XSD permanecem internos para preservar a infraestrutura de relatórios; não são páginas acessíveis pelo menu.
- A impressão agora contém exclusivamente as tabelas do MOC com os registros selecionados. DER **proposto**, não oficial, continua na Modelagem Oracle.
- Seleção exclusivamente no Leiaute do MOC; a Central de Impressão oferece prévia com retirada individual de registros, configurações, conjuntos salvos opcionais e geração do documento.
- Nenhum pai ou filho não selecionado é incluído como linha do relatório. A impressão preserva a profundidade e a ordem hierárquica do MOC, com recuos na coluna Campo e destaques nos grupos/subgrupos. Os títulos editoriais e cabeçalhos repetem-se nas páginas seguintes.
- PDF A4/A3 direto ou pelo navegador, exclusivamente com as linhas selecionadas do MOC; exportação CSV da seleção, modelagem Oracle separada, monitoramento e histórico.

## Repositório permanente e publicação sem reconstruir o projeto

Consulte [docs/PUBLICACAO_GITHUB.md](docs/PUBLICACAO_GITHUB.md) para os passos de instalação, configuração do GitHub Pages, rotina agendada e recuperação de versões. O repositório está em https://github.com/maikonvenicius07/dfe-data-explorer. O projeto inclui workflow de GitHub Actions e entrada compatível com publicação pela branch `/ (root)`. Confirme a configuração em Settings → Pages e teste o endereço público após cada push.

**Fluxo incremental recomendado:** 1. baixar e preservar a última versão; 2. comparar os arquivos; 3. modificar apenas o necessário; 4. testar; 5. atualizar `VERSION`, `CHANGELOG.md` e relatório; 6. enviar commit; 7. publicar; 8. preservar tags de versões anteriores.

## Limitações importantes

1. O catálogo embutido de 196 nós continua demonstrativo. O ZIP recebido contém adicionalmente 1.173 registros da extração HTML do MOC, de 25/11/2026; não equivale à validação do XSD. Os XSD oficiais não foram importados/validados nesta entrega.
2. A rotina agendada está preparada, mas só será executada após a configuração do GitHub e ativação do Actions. A implantação no Render exige configurar `ADMIN_TOKEN` e armazenamento persistente.
3. A seleção salva utiliza `localStorage` do navegador; não é sincronizada entre computadores e pode ser apagada quando os dados locais do navegador forem limpos.
4. O XLSX gerado pelo backend utiliza o catálogo oficial completo armazenado no servidor; **não** aplica a seleção da impressão. Para exportar exatamente os campos marcados, utilize CSV da Central de Impressão.
5. O endereço público foi verificado antes desta correção e estava exibindo o README. A publicação desta atualização e seu funcionamento externo dependem de commit/push no GitHub. Não houve teste em Render nem validação completa da base oficial.

## Verificações

Execute `node tests/test_selection_logic_v23.js`, `python -m pytest -q tests/test_import.py tests/test_publication_v232.py` e `python tests/test_simplified_controls_v2314.py`. O último requer Playwright, Chromium e PyMuPDF. Os testes de interface anteriores que abrem as quatro telas retiradas são históricos e não representam os requisitos de navegação atuais.

Arquivos para manter sincronizados: `public/index.html`, `public/styles.css`, `public/selection.js`, `public/app.js` e `public/EXPLORADOR_OFFLINE_COMPLETO.html`. Ao alterar o código, execute `python scripts/build_offline.py`; ao importar MOC validado, execute `python scripts/build_static.py`.


## Seleção manual para impressão — V2.3.3

No **Dicionário de Dados**, filtre por grupo, subgrupo, texto ou tipo. Filtros **não marcam registros**. Use a caixa da coluna `Imprimir` para marcar campos individualmente; o checkbox do cabeçalho opera apenas sobre os filtrados, apresentando estado parcial. Os botões permitem marcar/desmarcar filtrados ou toda a documentação. `Somente selecionados` facilita a conferência.

O botão **Imprimir selecionados** leva à Central de Impressão e mantém as marcações de outros grupos. Nessa área, configure A4/A3, orientação e colunas; verifique a lista de campos na prévia e retire os indesejados antes de gerar PDF. Sem seleção, a impressão fica bloqueada. As árvores e o diagrama compartilham o estado de marcação, mas selecionar/navegar até um grupo não marca seus campos automaticamente.

**Atenção:** a base embutida ainda cobre 196 nós do catálogo demonstrativo, não o MOC completo.

## Diagrama com expansão progressiva — V2.3.4

Na aba **Diagrama XML**, use `+` para expandir apenas os filhos diretos de cada nó, e `−` para recolher somente aquela ramificação. Os controles da barra permitem abrir/recolher tudo ou apenas o elemento selecionado. Alterar o formato horizontal/vertical/compacto preserva as ramificações já abertas. O documento inicia com a raiz e seus grupos superiores; o filtro `Grupo W` começa apenas com W01. Pesquisar um campo expande seus ancestrais.

Impressão: **visualização atual** (exatamente os nós expandidos/visíveis na árvore, inclusive os fora da área de rolagem), **estrutura completa do catálogo** (todos os 196 nós disponíveis, sem alterar as expansões) e **seleção manual** (somente os campos explicitamente marcados, com pais de contexto). Para manter a legibilidade em A4/A3, o PDF refluí os mesmos nós em **cartões hierárquicos pagináveis**: a distribuição geométrica na tela SVG não é reproduzida pixel a pixel. O conteúdo e os relacionamentos de pai-filho são preservados.

Testes: `node tests/test_diagram_progressive_v234.js` e `python -m pytest -q tests/test_import.py`. Arquivos sincronizados: `public/diagram-state.js`, `public/app.js`, `public/index.html`, `public/styles.css`, `public/EXPLORADOR_OFFLINE_COMPLETO.html`. Execute `python scripts/build_offline.py` após modificações.

**Limite:** os arquivos oficiais XSD ainda não foram importados; a seleção de 196 nós não é o leiaute integral.


## V2.3.5 — uma seleção nas quatro visualizações

- Leiaute do MOC, Explorador Hierárquico, Dicionário de Dados e Diagrama XML compartilham o **mesmo conjunto de identificadores internos**. Em todas essas áreas, marcar um campo é independente de filtrar, expandir e navegar.
- Nas caixas do diagrama (horizontal, vertical e compacto) há controles de marcação; pais e subgrupos são marcados **individualmente**, e o comando **Marcar filhos / Selecionar descendentes** é explícito e separado.
- A **Central de Impressão** inicia no modo **Imprimir selecionados — quatro visualizações**. Quatro caixas de opção ligadas por padrão permitem incluir/excluir MOC, árvore, dicionário e diagrama, sem mudar a seleção. A opção **Documentação disponível completa** é explícita e limita-se ao catálogo carregado (196 nós na base demonstrativa).
- Nas seções MOC e Dicionário, somente registros selecionados são linhas de dados. Árvore e Diagrama incluem os ancestrais indispensáveis, identificados como *PAI / CONTEXTO* e não contabilizados como seleção.
- A pré-visualização usa o mesmo documento que a impressão e permite retirar campos. A impressão é bloqueada sem elementos ou se nenhuma seção estiver marcada.
- O relatório pode ser impresso em A4/A3, retrato/paisagem; existe um exemplo de teste em `docs/EXEMPLO_INTEGRADO_B02_W38_V2_3_5.pdf`, com seis páginas A4 paisagem e texto pesquisável.
- Para validar: `node tests/test_integrated_selection_v235.js`, `python tests/test_cross_view_v233.py`, `python tests/test_custom_print_v233.py` e `python scripts/build_offline.py`. Para publicar, faça commit/push dos arquivos modificados e confira as Actions.

**Limite importante:** a publicação ainda utiliza a base demonstrativa de 196 nós; o projeto não inclui a importação e validação integral do MOC e dos XSD oficiais nesta atualização.

## Seleção e impressão integrada (V2.3.7)

- Marque campos em qualquer uma das quatro telas. Filtros, expansão e seleção são operações independentes.
- **Imprimir selecionados** abre a Central com as quatro seções e o conjunto acumulado. Desabilite as seções que não deseja.
- **Imprimir visíveis (4 visões)** captura os registros da visão atual, incluindo a rolagem, sem marcar outros campos nem alterar a seleção acumulada.
- **Documentação disponível completa** exige escolha explícita e cobre apenas o catálogo carregado.
- Diagrama vetorial com conectores pai-filho e formatos horizontal, vertical e compacto; contextos e referências de continuação não contam como novos campos.
- PDFs demonstrativos em `docs/exemplos_v237/`.
- Teste de navegador opcional: `pip install playwright pymupdf`, `playwright install chromium` e `python tests/test_integrated_print_v237.py` (ou configure `CHROMIUM_PATH`).

## Impressão horizontal e PDF direto (V2.3.8)

O diagrama XML inicia em árvore horizontal. Na Central de Impressão, mantenha **Mesmo formato do Diagrama XML** ou escolha explicitamente a árvore horizontal. Use **Baixar PDF direto** para gerar as quatro seções ou o diagrama sem passar pelo driver Microsoft Print to PDF. A4 paisagem é o padrão; A3 paisagem permite mais nós por página. A seleção e o contexto são preservados. A impressão nativa continua disponível. Os modos legados usam a impressão do navegador. Exemplos reais em `docs/exemplos_v238/`.

## Seleção reversível de ramificações (V2.3.9)

O botão `+ filhos` marca o nó e todos os descendentes; quando a ramificação está completa, muda para `− filhos` e desmarca o mesmo conjunto. Em seleção parcial, completa a ramificação. A caixa individual continua independente e as demais seleções são preservadas. A mesma ação vale na árvore, ficha técnica, diagrama e Central de Impressão.

## V2.3.11 — navegação simplificada

Selecione os campos no MOC ou na Central de impressão. Os botões + filhos e − filhos continuam disponíveis. A Central permite incluir as quatro representações no PDF, sem manter quatro telas separadas. O formato horizontal é o padrão; o botão Baixar PDF direto mantém a orientação escolhida.

## V2.3.12 — seleção progressiva ao expandir no MOC

A seta individual de um grupo XML ou subgrupo marca o próprio registro e os filhos diretos apresentados na tabela. Expanda os níveis seguintes para selecionar seus campos. Recolher mantém a seleção; use as caixas individuais ou − filhos para desmarcar. Filtros, busca, cabeçalhos editoriais e Expandir tudo continuam sendo ações de visualização.

## V2.3.13 — impressão exclusiva do MOC

A Central gera apenas a seção Leiaute do MOC, sem capa, sumário ou outras representações. Selecione registros explicitamente; a impressão vazia é bloqueada. Para imprimir tudo, use Selecionar toda documentação.

## V2.3.14 — interface enxuta

Selecione no MOC, clique em Imprimir selecionados e confira a própria tabela na Central. O botão × de cada linha da prévia retira o registro da seleção, sem entrar no PDF. As opções de papel, fonte, margens, cor e colunas atualizam a prévia automaticamente. Observação é controlada na seleção de colunas. Ações de seleção integral redundantes ficam ocultas quando o filtro abrange toda a base. Testes antigos que dependem dos controles removidos são históricos.

### V2.3.16 — impressão em árvore
A coluna Campo apresenta trilhas verticais contínuas e bifurcações reais da seleção. Pais ausentes são identificados como contexto, sem criar novos registros. A impressão nativa e o PDF direto preservam o mesmo modelo. A4 paisagem é o padrão; para maior legibilidade, prefira A3. O botão **Baixar PDF direto** evita conversões pelo driver de impressão. Exemplos reais em `docs/exemplos_v2316/`.

### V2.3.17 — blocos hierárquicos e versão verificável
A impressão mantém a tabela única de dez colunas, com faixas estruturais, níveis explícitos, trilhos reforçados e linhas de fechamento dos ramos. O mapa hierárquico é opcional e inicia desmarcado; ele usa a mesma seleção e distingue os pais de contexto. O PDF mostra V2.3.17 no cabeçalho/rodapé. Confira essa identificação depois da publicação. Assets possuem `?v=2.3.17`; o HTML offline é reconstruído a partir dos mesmos módulos. Exemplos em `docs/exemplos_v2317/`.

### V2.3.18 — ajuste de página e paginação
Central de Impressão: **Ajustar relatório em uma página** (padrão), **Paginação automática** (tenta compactar sem diminuir a fonte) e **Tamanho real**. A prévia mostra páginas físicas, tamanho efetivo da fonte e aviso se uma folha não comportar os registros. O PDF direto e o navegador consomem o mesmo plano. A3 é indicado para seleções extensas. O visual hierárquico e a base de dados permanecem inalterados. Exemplos em `docs/exemplos_v2318/`.

### V2.3.19 — impressão em fluxo e documento físico

O botão Abrir PDF para imprimir utiliza os mesmos bytes do botão Baixar PDF direto. Abra o arquivo no leitor PDF e use o papel escolhido e tamanho real (100%). O Ctrl+P do navegador é apenas alternativa em fluxo contínuo. O modo de uma página preserva a fonte da tabela e ajusta o espaçamento, sem redução automática. O A4 retrato recebe uma distribuição de colunas mais eficiente para descrições e observações. Verifique V2.3.19 no rodapé.
