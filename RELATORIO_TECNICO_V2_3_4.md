# DF-e Data Explorer — Relatório técnico V2.3.4-beta.1

**Data:** 24/11/2026. **Base:** V2.3.3-beta.1. **Alteração incremental; não é revisão integral do MOC.**

## Diagnóstico

A versão anterior usava `diagramDepth` (1/2/3/5/15) em uma busca em largura que expandia automaticamente os filhos até o limite. O usuário não conseguia expandir independentemente `W34 → W36 → W37`. O SVG podia ser exportado, mas a impressão do diagrama dependia da seleção manual dos campos e da antiga central, não do estado de expansão.

## Correções implementadas

1. Novo módulo `public/diagram-state.js` que indexa relações pai-filho por chave interna; não confunde tags repetidas. Mantém estado independente de cada ramificação, sem alterar as marcações da Central de Impressão.
2. Diagrama inicial resumido; visão geral do documento e filtragem por grupo/subgrupo; botões `+ / −` nas caixas estruturais (árvore e modo compacto). Ao expandir um nó, somente os filhos diretos passam a aparecer, com descendentes fechados por padrão.
3. Expansão/recolhimento total e por elemento selecionado; pesquisa revela ancestrais sem obrigar a abertura de irmãos. Três formas de desenho preservadas: horizontal, vertical, compacto; DER Oracle é uma proposta separada.
4. Três ações separadas: **visualização atual** usa `diagramGraph.visible(...,false)`; **estrutura completa** usa `diagramGraph.visible('__ALL__','',true)`; **seleção manual** usa `buildPrintSelectionData()`. Uma não altera o estado da outra.
5. Imprimir a visualização atual não requer checkbox marcado. Prévia e impressão são alimentadas pela mesma função; conteúdos recolhidos não entram no documento atual.
6. Impressão A4/A3: em vez de reduzir um SVG enorme até ficar ilegível, o navegador gera páginas com cartões e recuos hierárquicos, fonte selecionável, cabeçalho de grupo repetido e numerador de página. Exportações SVG/PNG continuam usando o diagrama atual completo, inclusive partes fora do viewport.

## Testes realmente realizados

- `node --check` em `app.js` e no novo módulo: **aprovado**.
- `node tests/test_diagram_progressive_v234.js`: **aprovado**, validando abertura parcial, independência, recolhimento e expansão completa, sem limite artificial de profundidade.
- `python -m pytest -q tests/test_import.py tests/test_publication_v232.py`: **9/9 aprovados**.
- `node tests/test_selection_logic_v23.js`: **aprovado** (seleção da impressão anterior preservada).
- Navegador automatizado Chromium com HTML offline: **sem erros de JavaScript**. Grupo W inicialmente 1 nó; após abrir W01, W34, W36, total visível 11; abrir W37 expôs W38; prévia corrente passou de 11 para 14 nós. Alternância horizontal/vertical/compacto manteve o estado.
- A impressão atual foi habilitada com **zero elementos selecionados**; seleção manual continua independente. Modo completo enumerou os **196 nós disponíveis**, mesmo com filtro W.
- PDFs reais produzidos: `docs/DIAGRAMA_GRUPO_W_PARCIAL_V2_3_4.pdf` (**2 páginas A4**) e `docs/DIAGRAMA_CATALOGO_COMPLETO_V2_3_4.pdf` (**19 páginas A4**). Texto extraído do primeiro confirmou W02/W23/W31 recolhidos e W38/W39/W41 visíveis após expansão explícita. Primeira e segunda páginas renderizadas para inspeção visual; o documento não apresentou linhas cortadas nas páginas verificadas.

## Limitações e pendências

- **Cobertura:** somente 196 nós de demonstração. O leiaute integral oficial do MOC e os XSD correspondentes ainda não foram importados e validados; não é possível afirmar completude técnica.
- **Impressão:** o conjunto exato de nós visíveis e o seu parentesco são preservados; para caber em múltiplas páginas, a **geometria SVG da tela é reorganizada** em cartões hierárquicos, não reproduzida pixel a pixel. PDF vetorial da própria topologia geométrica com paginação por conectores continua como evolução futura.
- A quantidade de páginas finais e a distribuição de quebras podem variar conforme navegador e impressora.
- O teste de estresse com XSD real grande, monitoramento hospedado e múltiplos sistemas operacionais continua pendente.
- Publicação no GitHub Pages depende de `Commit` e `Push` no repositório do usuário; não foi executada nesta entrega.

## Arquivos novos e alterados

- **Novo:** `public/diagram-state.js`, `tests/test_diagram_progressive_v234.js`, dois PDFs de demonstração em `docs/`, `RELATORIO_TECNICO_V2_3_4.md`.
- **Alterados:** `public/app.js`, `public/index.html`, `public/styles.css`, `public/EXPLORADOR_OFFLINE_COMPLETO.html`, `scripts/build_offline.py`, `.github/workflows/validar.yml`, `README.md`, `CHANGELOG.md`, `VERSION`, `ARQUIVOS_SHA256.txt`.

## Publicar no GitHub

Descompacte o ZIP incremental sobre a raiz local `dfe-data-explorer`, mantendo a estrutura de pastas e substituindo os arquivos. No GitHub Desktop, crie o commit `V2.3.4 - Diagrama progressivo e impressão atual`, clique `Push origin`, acompanhe `Actions` e valide o site GitHub Pages. Não exclua dados nem altere o banco Oracle.
