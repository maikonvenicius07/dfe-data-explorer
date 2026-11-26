# DF-e Data Explorer — V2.3.10-beta.1

Data: 26/11/2026. Base: ZIP completo V2.3.9. Escopo: simplificação da navegação.

## Decisão e implementação

A imagem enviada aponta quatro áreas a retirar: Explorador Hierárquico, Dicionário de Dados, Diagrama XML e Visualizador XSD. Elas foram removidas do menu. Permanecem apenas Leiaute do MOC (tela inicial), Modelagem Oracle, Atualizações e histórico e Central de impressão.

A remoção é funcional na interface, não uma exclusão física dos módulos: as seções internas ficam ocultas, inertes e fora da árvore de acessibilidade; a navegação aceita somente as quatro telas restantes. O atalho e a legenda de localização no diagrama foram retirados do MOC. Esta decisão evita quebrar dependências do motor de impressão e permite preservar a evolução já aprovada. A opção de imprimir a visualização da antiga tela de diagrama foi retirada do seletor; a impressão dos registros visíveis no MOC continua disponível. Na Central de impressão, a árvore horizontal passa a ser a opção explícita padrão, sem depender da antiga tela de diagrama.

As quatro representações do relatório integrado (MOC, hierarquia, dicionário e diagrama) permanecem como conteúdo opcional da impressão, com as quatro habilitadas por padrão, conforme regra anterior. É possível imprimir apenas as seções desejadas. A seleção é feita no MOC ou na Central, sem alterar a semântica de seleção individual ou +/− filhos.

## Arquivos alterados

- `public/index.html`: menu, seções internas inertes, rótulos de impressão e formato horizontal.
- `public/app.js`: navegação restrita, remoção do atalho ao diagrama e textos ajustados.
- `public/styles.css`: regra explícita para ocultar módulos internos.
- `public/EXPLORADOR_OFFLINE_COMPLETO.html`: regenerado pelo script oficial.
- `VERSION`, `README.md`, `CHANGELOG.md`, `docs/FUNCIONALIDADES_APROVADAS.md`: identificação e regras atualizadas.
- `tests/test_publication_v232.py`: valida a nova navegação no HTML web e offline.
- `tests/test_simplified_navigation_v2310.py`: novo teste funcional com Chromium e PDF direto.
- `RELATORIO_TECNICO_V2_3_10.md`, `ARQUIVOS_SHA256.txt`: relatório e manifesto.

Nenhum arquivo removido. Catálogo, mecanismos de seleção, geração direta de PDF e monitoramento preservados. A cobertura permanece parcial (196 nós da seleção anterior), não se trata de importação integral do MOC.

## Testes efetivamente realizados

- 9 testes pytest de importação e publicação aprovados.
- 4 arquivos de testes Node aprovados: seleção, alternância de filhos, diagrama progressivo e seleção integrada.
- Sintaxe JavaScript da aplicação aprovada.
- Chromium: quatro menus visíveis e navegáveis, quatro módulos ocultos, ausência do atalho do MOC para diagrama, seleção em grupos distintos, marcação e desmarcação de filhos, seleção preservada na Central, correspondência exata dos dois registros selecionados nas quatro seções, possibilidade de imprimir somente duas seções e bloqueio quando a seleção fica vazia. Nenhum erro JS observado no cenário.
- PDF direto real: A4 paisagem, A4 retrato e A3 paisagem, com rotação zero, texto horizontal e seleção correta. Diagrama horizontal verificado na estrutura HTML que alimenta o PDF. Não foram feitas alterações no motor de renderização do PDF.

## Limitações

O ambiente Chromium bloqueou navegação `file://` por política administrativa; o teste funcional carregou o conteúdo HTML offline via Playwright, sem testar abertura do arquivo pelo navegador do usuário. Os testes antigos que exigem navegação nas telas removidas não foram executados nesta versão, por terem requisitos de interface superados. Seus arquivos foram mantidos como histórico. Não houve publicação remota nem teste em impressora física. A validação da importação oficial e da cobertura completa continua pendente.

## Publicação

Se o repositório já estiver na V2.3.9, aplique o ZIP incremental mantendo os caminhos. Caso contrário utilize o ZIP completo. Confirme a aprovação do GitHub Actions e a publicação antes de recarregar a aplicação (Ctrl+F5). Para uso local, abra `public/EXPLORADOR_OFFLINE_COMPLETO.html`.
