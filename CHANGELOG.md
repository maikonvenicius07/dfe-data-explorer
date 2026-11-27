## V2.3.24-beta.1 — inicialização e consistência da publicação

- Catálogo NF-e real embutido na página inicial, sem dependência de requisição para sair da demonstração.
- Recursos auxiliares inválidos não interrompem a coleta dos demais; Pages consulta caminhos estáticos.
- Verificação de versão e reconstrução de artefatos antes da publicação; testes de regressão de navegação e PDF.
- Sem alterações nos catálogos, hierarquia, seleção ou estilos aprovados.

## V2.3.23-beta.1 — paridade dos leiautes multidocumento

- Aplicados os mesmos comandos de expansão e seleção da NF-e a todos os documentos.
- Rótulos de grupos mais claros; atributos isolados reunidos à seção do pai quando comprovado.
- Reconhecimento de GS/SG e Raiz; recuperação conservadora de 34 vínculos na visualização, demais avisos explícitos.
- Coluna Pai ampliada nos relatórios sem ID oficial; preservado o PDF NF-e.
- Catálogos originais, chaves, importadores e workflows preservados; 19 PDFs reais de QA.

## V2.3.22-beta.1 — correção da instalação e publicação dos importadores

- Workflows executáveis diretamente em `.github/workflows/`; preservadas cópias históricas inertes.
- GitHub Pages preserva o endereço `/public/`; diagnóstico de coleta na tela de catálogo indisponível.
- Alternativa de importação Windows e instrução para criação correta do workflow.
- HTML offline inclui a base NF-e publicada; correção de título de catálogo.
- Coleta remota de novos manuais e validação XSD ainda pendentes; sem catálogos fictícios.

# V2.3.21-beta.1 — 2026-11-27 (entrega parcial)

- Carregador multidocumento baseado nos catálogos presentes, com variantes CT-e e BP-e e seleção isolada.
- Importador comum de tabelas Leiaute por Pai/ID ou Nível, com rastreabilidade, validação estrutural, diagnóstico e preservação de dados anteriores em falhas detectadas.
- Workflows na pasta correta, publicação preservando o endereço /public/ e reconstrução da versão offline.
- A tentativa de coleta real falhou por DNS; nenhum catálogo novo foi confirmado. NF-e/NFC-e e DC-e piloto preservados. Testes de novos documentos usam fixtures, não dados fiscais reais.

# V2.3.20-beta.1 — 2026-11-26

- Primeira etapa multidocumento: registro único dos dez itens do portal e dois catálogos navegáveis (NF-e/NFC-e e piloto DC-e).
- Separação de seleção, contexto, filtros e conjuntos salvos; oito documentos pendentes não exibem dados de NF-e.
- DC-e: 111 registros estruturais, importador HTML independente com validação e workflow manual; descrições, observações e XSD ainda pendentes.
- Consultas técnicas contextuais; motor e layout de impressão compartilhados. Caso de regressão NF-e W22 preservado em A4 retrato.

# V2.3.19-beta.1 — 2026-11-26

- Corrige quebra antecipada no fluxo HTML, elimina agrupamento artificial de linhas e limita folga de compatibilidade entre motores.
- Preserva fonte da tabela, redistribui largura no A4 retrato e abre o mesmo PDF vetorial para imprimir ou baixar.
- Validação de versão do HTML e gerador PDF, assets versionados e offline sincronizado.
- Caso real de 22 registros: uma página A4 retrato, 8,5 pt, sem redução da fonte.

# V2.3.18-beta.1 — ajuste de página e paginação

- Paginação com medição física de linhas e alternativas moderadas de densidade; sem agrupamento indivisível de ramificações.
- Prévia paginada, modo de ajuste em uma página, automático e tamanho real; validação cruzada com o PDF direto.
- Mantidos colunas, pesos, níveis, conectores, cores, seleção e catálogo.
- Aviso quando a seleção não cabe em uma página dentro dos limites de legibilidade.

# V2.3.17-beta.1 — blocos hierárquicos no MOC

- Faixas de grupo com nível explícito, trilhos de conexão reforçados, delimitação dos ramos e mais espaço na coluna Campo.
- Mapa vetorial opcional com pais de contexto destacados, sem alterar a seleção. Tabela continua sendo a única saída padrão.
- Identificação da versão no PDF e referências versionadas de CSS/JS para reduzir cache antigo.
- Paginação tenta manter pequenos ramos juntos; preserva cabeçalhos de continuação.
- Catálogos, seleção progressiva e menu simplificado preservados.

# V2.3.16-beta.1 — árvore gráfica contínua na impressão MOC

- A coluna Campo utiliza linhas de continuidade, bifurcações e encerramentos calculados pelos caminhos de pai e filhos do catálogo, preservando a profundidade original.
- Pais ausentes são indicados como contexto textual, sem linhas adicionais nem mudança da seleção.
- Destaques por nível, maior largura da coluna Campo e conectores vetoriais nos dois motores.
- Paginação do navegador a partir de clone da tabela, com cabeçalhos de continuação e caminho de contexto; PDF direto também identifica continuações.
- Mantida a impressão exclusiva do MOC e o menu simplificado. Catálogos inalterados.

# V2.3.15-beta.1 — hierarquia do MOC na impressão

- Prévia e impressão reutilizam a travessia hierárquica da tabela MOC e somente depois filtram os registros selecionados.
- PDF direto respeita profundidade, conectores, cor de grupo e negrito; larguras compartilhadas com HTML.
- Título editorial e cabeçalhos repetidos em páginas seguintes.
- Preservados seleção progressiva, menu simplificado e saída exclusiva MOC.

# V2.3.14-beta.1 — simplificação de controles

- Seleção concentrada no Leiaute do MOC; Central de impressão sem segunda árvore ou lista de revisão repetida.
- Retirada de campos diretamente na prévia; atualização automática; observações controladas pela coluna.
- Remoção de dois atalhos de impressão redundantes, link duplicado e referência fixa no menu.
- Catálogo recebido preservado, incluindo os 1.173 registros da extração HTML.

## V2.3.13-beta.1 — 26/11/2026

- Impressão e PDF exclusivamente do Leiaute do MOC com os registros marcados, sem capa, sumário, árvore, dicionário ou diagrama.
- Central simplificada; papel, orientação, colunas, observações e seleção preservados.

## V2.3.12-beta.1 — 26/11/2026

- A seta individual do Leiaute MOC seleciona o registro expandido e seus filhos diretos visíveis, progressivamente.
- Recolher mantém a seleção; filtros, expansão global e botões +/− filhos permanecem independentes.

## V2.3.11-beta.1 — 26/11/2026

- Removida a faixa de atalhos “Divisões XML neste grupo” do Leiaute MOC em todos os grupos.
- Mantidos títulos, contagens, tabelas, expansão individual, seleção e impressão.

## V2.3.10-beta.1 — 26/11/2026

- Navegação reduzida a quatro telas: MOC, Oracle, Atualizações e Central de impressão.
- Árvore, dicionário, diagrama e XSD retirados da navegação, preservados internamente para relatórios e processamento.
- Removido o atalho do MOC para a tela de diagrama. Seleção reversível e PDF horizontal preservados.

## V2.3.9-beta.1 — seleção reversível de filhos (25/11/2026)

- Botões de seleção de ramificações alternam entre marcar e desmarcar o mesmo conjunto (nó + descendentes).
- Estado parcial completa a seleção; estado completo permite limpar sem afetar outras ramificações.
- A ação e os rótulos são compartilhados entre MOC, árvore, ficha técnica, diagrama e Central de Impressão.
- Preservados seleção individual, filtros, expansão, catálogo e geração de PDF da V2.3.8.

## V2.3.8-beta.1 — diagrama horizontal e PDF direto (25/11/2026)

- Diagrama horizontal por padrão, com a Central de Impressão seguindo o formato da tela ou uma escolha explícita.
- Árvore horizontal paginada por caminhos, com caixas arredondadas e curvas pai-filho; sem seleção implícita de irmãos ou descendentes.
- PDF direto local, vetorial e pesquisável para os modos integrados e diagramas, com dimensões físicas A4/A3 e /Rotate 0; não depende do driver Windows.
- Mantida impressão nativa, com dimensões CSS explícitas e aviso de orientação; preservadas as oito telas, o catálogo e a seleção compartilhada.
- Teste de regressão reproduz os 13 campos do PDF do usuário e valida três configurações físicas do PDF, além da impressão nativa e do catálogo inteiro.

## V2.3.7-beta.1 — seleção e impressão integradas (25/11/2026)

- Unificados os atalhos Imprimir selecionados nas quatro telas, sempre abrindo o relatório integrado.
- Adicionado modo integrado de registros visíveis, independente da seleção manual e do catálogo completo.
- Diagrama de impressão SVG com conectores reais, três formatos, paginação e referências de continuidade.
- Revisados controles de seleção explícita e contagens na Central de Impressão; preservados dados, oito janelas e publicação.
- Novo teste de navegador e três PDFs de demonstração.

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
