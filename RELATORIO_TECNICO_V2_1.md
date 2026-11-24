# Auditoria e evolução do DF-e Data Explorer — v2.1.0-beta.1

**Data:** 24/11/2026  
**Base de comparação:** v2.0.0-beta.1  
**Estado:** beta / homologação local; não certificado como cobertura integral do MOC.

## 1. Escopo e diagnóstico

Auditoria feita sobre `public/index.html`, `public/app.js`, `public/styles.css`, scripts Python e testes do ZIP da versão 2.0. A tela antiga forçava `diagram-area svg{width:100%;height:100%;min-width:740px;min-height:540px}` embora o JavaScript declarasse um `viewBox` com dimensões potencialmente muito maiores. A largura física forçada escalonava os textos de forma invisível: o botão indicava 100%, mas uma unidade do desenho não correspondia a um pixel CSS. Havia um teto de apenas 60 nós na árvore SVG e exportação PNG de tamanho fixo (1600x1100), sujeita à redução, perda de definição e corte de elementos. O renderizador original utilizava um layout por nível muito comprido.

A impressão anterior oferecia A4 retrato/paisagem e tabelas, sem formatos de diagrama para papel, sem seleção múltipla, controle de papel A3, impressão econômica, margens ou fonte. A página de resumo podia ficar muito vazia devido às quebras. A base da demonstração tem 196 nós e informações oficiais incompletas. Esse último ponto é **limitação de conteúdo**, não um bug visual. O sistema pré-existente já incluía coletor MOC, parser de XSD, snapshots, notificações condicionadas à instalação, filtros, dicionário e modelagem Oracle sugerida. Eles foram preservados.

## 2. Principais mudanças

| Área | Problema anterior | Alteração aplicada | Validação |
|---|---|---|---|
| Escala SVG | Layout reduzido para largura disponível, apesar de “100%” | SVG usa dimensões CSS naturais, sem scale automático; rolagem e ajuste opcional | Playwright confirmou largura CSS igual ao atributo SVG em 100% |
| Formatos | Somente árvore horizontal | Árvore horizontal, vertical, cartões compactos e DER Oracle proposto | Abertura dos quatro modos sem erros JS |
| Navegação | Falta de controles de foco e espaço | Seleção de grupo/raiz, profundidade, busca, centralizar, zoom, fullscreen, recolher menu e arraste | Testes automatizados da interface |
| Escala em grandes grupos | 60 nós, sem explicação | Limite de renderização de 350 nós, aviso explícito e filtro por raiz | Teste sobre seleção, não carga de 350 nós em dispositivo real |
| SVG/PNG | PNG fixo 1600x1100, exportações sensíveis ao zoom | Exportação SVG natural e PNG 2x ou 3x, verificando limites do canvas | Downloads capturados no Chromium |
| Impressão | Tela/tabelas com poucas opções | Central independente, oito modalidades, A4/A3, fonte, margens, orientação, grupos múltiplos e P&B | Sete PDFs demonstrativos gerados e inspecionados |
| Diagramas em papel | Enquadramento integral com letras pequenas | Paginação por pais e grupos, cartões de até doze linhas, identificação de continuidade; opção hierárquica recuada | PDF A3 e A4 inspecionados |
| Coluna # ausente | Texto “Não informado” quebrava verticalmente na tabela A4 | Exibição discreta “—” para campos administrativos ausentes; não substitui o dado oficial | Inspeção visual da tabela |
| Paginação | Páginas pouco utilizadas e capítulos separados desnecessariamente | Redução de quebras forçadas, títulos junto às próximas seções quando viável | Conferência das páginas renderizadas |

## 3. Conteúdo preservado

Mantidos: a tabela do leiaute com as **dez colunas** e o comportamento para valores ausentes, árvore, dicionário, pesquisa e filtros, visualizador XSD, entidade Oracle sugerida, SQL comentado, monitor oficial via Python, snapshots/histórico, diferenças de versão, notificações, importação de catálogo, exportação CSV/JSON/XLSX via backend e geração de HTML offline. Não foram feitas alterações no banco Oracle.

### Ressalva sobre “diagrama completo”

Uma só folha com todo o leiaute é ilegível; o modo de impressão por grupos pagina cada relação pai-filhos e repete seu contexto. A impressão **não** reconstrói automaticamente um fluxograma SVG horizontal gigantesco dividido em páginas interligadas; esta versão oferece a alternativa legível em cartões/hierarquia listada. Também não possui minimap implementado. Tais demandas continuam aprimoramentos possíveis.

## 4. Dados oficiais, importação e XSD

Fonte principal: <https://moc.sped.fazenda.pr.gov.br/NFe_NFCe/Leiaute.html>. Durante a verificação pública, a página identificava atualização até **NT 2026.008 v1.01 de 30/10/2026**. A sessão local do projeto **não conseguiu se conectar diretamente ao domínio** (falha de resolução DNS). Portanto **não foram importados todos os grupos e campos do MOC** nem os arquivos XSD oficiais. A aplicação mantém aviso visível de seleção parcial e a rotina existente de sincronização segura com bloqueio de extrações incompletas. Não há certificação de correspondência integral entre MOC e XSD.

## 5. Testes executados

1. `node --check public/app.js`: aprovado.
2. `python -m unittest discover -s tests -p 'test_import.py' -v`: **6/6 testes aprovados** (parser de 10 colunas, diff, qualidade, bloqueio de extração incompleta, XSD e proteção contra entidades externas).
3. Playwright + Chromium: **8 áreas** da interface navegadas; quatro formatos de diagrama renderizados; zoom 100% verificado; grupo B testado com mais de nove nós; **sem erros JavaScript**.
4. Download real dos formatos SVG e PNG: ambos gerados com êxito na seleção de teste.
5. **7 PDFs demonstrativos** gerados: grupo pequeno A4, extenso A4, tributário A4, hierarquia A3, leiaute MOC A4 (196 registros disponíveis), Oracle A4 e técnico integrado A4.
6. Os PDFs foram lidos com PyMuPDF para validar páginas e texto selecionável, e imagens representativas foram abertas visualmente para conferir cabeçalhos, tabela, blocos, paginação e ausência de cortes aparentes.

| PDF de demonstração | Páginas após ajustes |
|---|---:|
| Grupo pequeno A4 | 3 |
| Grupo extenso A4 | 8 |
| Grupo tributário A4 | 4 |
| Diagrama grupo B A3 | 3 |
| Tabelas padrão MOC A4 | 15 |
| Modelagem Oracle A4 | 3 |
| Técnico integrado A4 | 6 |

As amostras são extraídas **somente dos 196 nós da base demonstrativa**. Uma inspeção real em impressora física e uma avaliação com catálogo oficial completo ainda são necessárias. Os resultados não são prova de melhoria de CPU ou de RAM: não foi executado benchmark comparativo de desempenho, nem teste de carga com milhares de registros oficiais.

## 6. Limitações ainda abertas

- **Crítico para certificação fiscal:** importar todo o leiaute oficial, suas observações, os XSD vigentes e validar a cobertura e as referências; o material demonstrativo não contém todas as 10 colunas preenchidas.
- **Alto:** validar a hierarquia contra schemas verdadeiros, incluindo choice, import/include, campos repetidos em XPaths distintos e obrigatoriedade condicional. O diagrama segue o pai declarado no catálogo atual.
- **Médio:** integrar um minimapa e paginação SVG vetorial horizontal com referências cruzadas por página. O SVG de tela pode ser extenso e exige rolagem.
- **Médio:** homologar com dados oficiais e realizar inspeção de impressão física A4/A3 colorido e P&B em impressoras diferentes.
- **Médio:** habilitar e validar o serviço agendado e as credenciais de notificação em hospedagem persistente; não está ativo automaticamente por ser aberto no navegador.
- **Baixo:** ampliar exportação PNG para PDFs vetoriais sob demanda, mantendo limites de segurança de canvas.

## 7. Execução

Abra `public/EXPLORADOR_OFFLINE_COMPLETO.html` para testes offline. Para executar backend e sincronização quando houver acesso à fonte, use:

```sh
python -m pip install -r requirements.txt
python scripts/serve.py
python scripts/monitor.py
python scripts/import_xsd.py CAMINHO_PACOTE_XSD.zip
```

O monitor exige rede e configuração de agendamento para executar periodicamente. Na plataforma gratuita, verifique disponibilidade, persistência, custos e capacidade de execução de rotinas agendadas.

## 8. Condições para aceitar a próxima versão como “completa”

A próxima etapa deve validar quantitativamente a quantidade de linhas, grupos, subgrupos e tags na documentação oficial, comparar versões e resolver referências XSD; produzir relatório de divergências e testes com grandes grupos reais; e comprovar impressão e exportação sem corte. Esta beta **não satisfaz ainda o requisito de cobertura integral**.

**Conclusão:** as falhas comprovadas de escala do diagrama e a estrutura anterior de impressão foram corrigidas e validadas localmente, mantendo os módulos existentes. A certificação do conteúdo fiscal depende da sincronização e validação oficiais ainda pendentes.
