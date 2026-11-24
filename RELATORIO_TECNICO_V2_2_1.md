# Relatório técnico — Explorador NF-e/NFC-e V2.2.1-beta.1

Data: 24/11/2026

## Solicitação
Remover da barra destacada do Diagrama XML os controles de recolher menu, centralizar, ajustar, zoom e opções PNG, mantendo **somente o botão Tela cheia**. O restante das áreas e funções deve ser preservado.

## Implementação
- Simplificada a barra da área de diagramas: visível apenas **Tela cheia**, alinhado à direita; removida a grande faixa branca vazia.
- As referências internas dos controles anteriores permanecem ocultas para impedir falhas no JavaScript legado e manter a seleção de resolução utilizada pela exportação PNG, disponível em outro local.
- Preservados a árvore, o catálogo de 196 nós da seleção histórica, os modos horizontal/vertical/compacto/Oracle, a impressão, a exportação e o monitoramento já existente. Não foram alteradas as fontes oficiais, a base nem a hierarquia dos campos.
- Versionamento atualizado para **v2.2.1-beta.1**.

## Arquivos alterados
- `public/index.html` — barra simplificada na página com servidor.
- `public/EXPLORADOR_OFFLINE_COMPLETO.html` — mesma mudança no HTML autossuficiente.
- `public/styles.css` — barra compacta, sem fundo e alinhada à direita.
- `VERSION`, `README.md`, `CHANGELOG.md` — identificação da versão/documentação.
- `tests/test_ui_print.py` — regressão anterior usa clique programático no controle oculto para manter verificação da escala.
- `tests/test_fullscreen_only_v221.py` — novo teste de regressão dos controles visíveis e da tela cheia.
- `RELATORIO_TECNICO_V2_2_1.md` — este relatório.
- `ARQUIVOS_SHA256.txt` — novo inventário de hashes.

## Testes realmente executados
1. **Playwright/Chromium**: ao abrir a seção Diagrama, exatamente um botão da barra está visível e seu texto é `Tela cheia`. Aprovado.
2. Os antigos controles não são visíveis ao usuário. Aprovado.
3. Botão `Tela cheia` ativa `document.fullscreenElement` para `diagramViewport`; a saída via API nativa funciona. Aprovado.
4. Os quatro modos de diagrama renderizam conteúdo SVG. Aprovado.
5. A tabela do MOC abre e a Central de Impressão prepara conteúdo. Aprovado.
6. Ausência de exceções de JavaScript durante o fluxo acima. Aprovado.
7. **Pytest** (`tests/test_import.py`): 6 testes aprovados.

## Limitações
- Não foi realizada validação de todos os navegadores ou em celulares físicos.
- Não foram reexecutados os sete PDFs demonstrativos da versão anterior porque o mecanismo de impressão não foi modificado.
- A cobertura da base continua parcial (196 nós); a importação integral do MOC e os XSD oficiais não fazem parte desta alteração.

## Uso
Abra `public/EXPLORADOR_OFFLINE_COMPLETO.html` no navegador ou utilize o HTML avulso anexado. Na área Diagrama XML aparece apenas **Tela cheia**; saia dela com **Esc**. Para hospedagem, publique os arquivos atualizados no mesmo caminho relativo.
