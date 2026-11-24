# RELATÓRIO TÉCNICO — DF-e Data Explorer V2.3.0-beta.1

**Data:** 24/11/2026  
**Versão de referência:** V2.2.1  
**Objetivo:** evolução incremental do explorador NF-e/NFC-e, sem reconstrução, priorizando apresentação e seleção personalizada de impressão.  
**Status:** versão beta funcional para estudos e homologação, **não** certificada como documentação oficial integral do MOC.

## 1. Diagnóstico e causas identificadas

| Área | Diagnóstico anterior | Gravidade | Ação |
|---|---|---|---|
| Visão Geral | Quatro estatísticas e mapa sem gráficos de distribuição; não adequada a apresentações | Alta | Indicadores calculados e modo apresentação |
| Impressão | Escopo por grupo, grupos múltiplos ou documento completo; inexistia seleção de subgrupos e campos individuais | Alta | Árvore de seleção integrada, com estados parciais |
| Dicionário | Colunas fixas, ordenação limitada e navegação para a ficha técnica sem seleção para impressão | Média | Configuração de colunas, ordenação e seleção dos campos filtrados |
| Fluxo interativo | Elemento selecionado na ficha não podia ser enviado diretamente à impressão | Média | Botão de seleção integrado à ficha |
| Implantação | Offline e servidor opcionais, mas não havia workflow independente de publicação Pages | Alta | GitHub Actions Pages, scripts de build e fallback estático |
| Dados | Catálogo demonstrativo anterior de 196 nós; campos ausentes e títulos derivados de prefixos de ID | **Crítica** | Mantido aviso de cobertura; **coleta e validação integral pendentes** |
| Monitoramento | Cron preparado, sem hospedagem configurada ou validação da coleta remota | Alta | Integrado ao build estático, **não ativado remotamente** |

## 2. Alterações realizadas

1. **Visão Geral:** seis indicadores adicionais, gráficos por grupo e profundidade calculados dos registros disponíveis, links de exploração e modo de apresentação em tela cheia. A legenda não sugere cobertura oficial total.
2. **Seleção hierárquica para impressão:** uma árvore em que os grupos são seções editoriais e os vínculos XML são derivados do campo pai catalogado. Seleção/desmarcação em cascata, estado parcial de ancestrais, pesquisa, expandir/recolher, selecionar tudo e limpar. Grupos diferentes podem participar da mesma seleção.
3. **Contexto sem impressão indevida:** no modo hierárquico o relatório inclui pais necessários para esclarecer a hierarquia, com marcação explícita **“pai: contexto, não selecionado”**. Os demais campos não entram. A contagem considera apenas os elementos marcados.
4. **Seleções reutilizáveis:** conjuntos nomeados no armazenamento local do navegador, com carga/remoção e eliminação de chaves que não pertençam ao catálogo importado.
5. **Dicionário:** ordenação por ID, nome, grupo ou descrição; escolha de colunas exibidas; caixas de seleção por registro; ação que transforma os campos filtrados em seleção de impressão. Exportação CSV respeita busca, ordenação e colunas visíveis.
6. **Publicação:** workflow de GitHub Pages, workflow de teste rápido, script de geração do HTML independente e script para copiar snapshots JSON validados para `public/data/`; fallback de leitura do JSON estático quando as APIs não existem.
7. **Preservação:** diagramas horizontal/vertical/compacto/DER, dez colunas do MOC, ficha técnica, histórico, XSD, Oracle e opção **somente Tela cheia** na barra do diagrama (V2.2.1) permanecem.

## 3. Evidências dos testes efetivamente executados

| Teste | Resultado | Evidência |
|---|---|---|
| Importador, validação e comparação de snapshots | **6/6 aprovados** | `python -m pytest -q tests/test_import.py` |
| Motor puro de seleção: pai/filho, subgrupos, parcial, duplicidade de IDs e contexto | **Aprovado** | `node tests/test_selection_logic_v23.js` |
| Interface no Chromium: indicadores, árvore, seleção W34 e seleção isolada W38, modelos salvos, dicionário e PDF | **Aprovado** | `python tests/test_productivity_v23.py` |
| Regressão visual da barra: apenas botão Tela cheia e entrada/saída | **Aprovado** | `python tests/test_fullscreen_only_v221.py` |
| Geração de documentos dos sete cenários legados | **Aprovado** | `python tests/test_ui_print.py`; sete arquivos PDF presentes em `docs/pdf_examples` |
| Layout mobile em 390 px | **Aprovado na inspeção pontual** | captura `docs/v23_mobile.png` e verificação `scrollWidth=390` |
| PDF W38 isolado, A4, texto selecionável, pais de contexto | **Aprovado** | `docs/v23_relatorio_selecao_W38.pdf`; uma página inspecionada em PNG |
| Suíte extensa `test_hierarchy_v22.py` | **Não concluída** | execução ultrapassou o limite local de 25 segundos; não declarar aprovação |
| Atualização oficial no site e publicação real GitHub Pages/Render | **Não executadas** | exigem fonte remota, conta e implantação ativa |
| Exportação XLSX filtrado por seleção | **Não implementada** | usar CSV para seleção exata; XLSX do backend não aplica filtros |

Em nenhum ponto foi inferida melhoria de velocidade sem medição comparativa em produção. Os testes visuais citados foram realizados por injeção de HTML no navegador de automação local, sem publicação pública da aplicação.

## 4. Integridade e cobertura oficial

A interface embutida permanece com **196 nós demonstrativos**, sem a importação integral do MOC atualizado, XSD oficial e correspondência definitiva MOC↔XSD. Não apresentar as contagens como totais fiscais oficiais. A fonte de referência do projeto é `https://moc.sped.fazenda.pr.gov.br/NFe_NFCe/Leiaute.html`, identificada no portal como atualizada até a NT 2026.008 v1.01, de 30/10/2026 (confirmação web em 24/11/2026). O portal nacional também publica pacotes XSD recentes que precisam ser importados separadamente.

A nova seleção reutiliza o relacionamento XML pai–filho conhecido no catálogo. Em IDs de pais duplicados, a associação ambígua não é inventada. A modelagem Oracle permanece **conceitual** e não executa alterações no banco de dados.

## 5. Implantação no GitHub e custos

O projeto está **pronto para ser enviado** a um repositório GitHub, com `public/index.html` e workflows de Pages. **Ainda não há publicação nem URL real**. Instruções completas: `docs/PUBLICACAO_GITHUB.md`.

Recomendação inicial: repositório público + GitHub Pages para interface e relatórios, e GitHub Actions para a consulta programada. GitHub Pages serve arquivos estáticos; não hospeda diretamente a API Python. Render Web Service é alternativa para API, porém o serviço gratuito pode hibernar após período de inatividade. Automações agendadas pelo GitHub podem atrasar ou falhar e exigem acompanhamento. Nenhum serviço pago foi contratado.

## 6. Arquivos e consistência do incremental

Arquivos essenciais criados/alterados: `public/index.html`, `public/app.js`, `public/styles.css`, `public/selection.js`, `public/EXPLORADOR_OFFLINE_COMPLETO.html`, `scripts/build_static.py`, `scripts/build_offline.py`, `.github/workflows/publicar_paginas.yml`, `.github/workflows/validar.yml`, `.github/workflows/atualizar_moc.yml`, `tests/test_productivity_v23.py`, `tests/test_selection_logic_v23.js`, `tests/test_ui_print.py`, `README.md`, `VERSION`, `CHANGELOG.md`, `ARQUIVOS_SHA256.txt` e documentação em `docs/`.

Os ZIPs são criados por comparação de SHA-256 com a V2.2.1: o incremental inclui apenas entradas realmente novas/alteradas, preservando os mesmos caminhos e **bytes idênticos** aos correspondentes do ZIP completo. **Nenhum arquivo da base antiga foi excluído**. Os PDFs e imagens legadas sem mudança funcional são preservados sem entrar no incremental.

## 7. Limitações e recomendações para a próxima versão

1. **Prioridade crítica:** extrair, auditar e cruzar a documentação completa do MOC e o pacote XSD oficial, com relatório de cobertura antes de substituir a base atual.
2. Validar implantação real GitHub Pages e monitor diário com revisão de snapshots e alertas de falhas.
3. Implementar XLSX que respeite a seleção, além de filtro técnico avançado, exportação dos diagramas selecionados e presets exportáveis entre dispositivos.
4. Ampliar os testes com um catálogo oficial grande (milhares de linhas) e exercitar o modelo em navegadores móveis reais.
5. Criar um roteiro de apresentação em tela cheia com resumos de grupos fiscais, após a importação integral.

**Conclusão:** correções de interface e impressão implementadas sobre a base anterior, preservando as funcionalidades conhecidas. A plataforma continua beta, com cobertura fiscal oficial parcial, e não deve ser considerada concluída até validar o catálogo integral e a publicação real.
