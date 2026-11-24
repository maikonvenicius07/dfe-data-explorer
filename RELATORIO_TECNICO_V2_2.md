# Auditoria técnica do DF-e Data Explorer — V2.2.0-beta.1

**Data:** 24 de novembro de 2026. **Escopo:** avaliação dos documentos de requisitos encaminhados em 24/11/2026, imagens do Grupo W e do Diagrama XML, HTML da V2.0 anexado e código-fonte da V2.1, preservada como base da correção. **Natureza:** ferramenta de documentação independente; não oficial.

## 1. Diagnóstico da causa raiz

### P1 — Hierarquia invisível no leiaute do MOC | ALTA | confirmado
O relatório original renderizava uma **tabela plana** por prefixo dos IDs (`W`, `UB` etc.). O catálogo já registra o `parent` de W01, W02, W34, W36, W37 e dos demais campos, mas não exibia os níveis internos nem permitia recolher um subgrupo. A nomenclatura da seção editorial confundia agrupamento de IDs com hierarquia XML.

**Correção:** uma função única calcula a árvore por `parent`/chaves. A tabela permanece com dez colunas, mas sua coluna Campo recebe recuos, indicadores de grupo e comandos para expandir/recolher qualquer pai. Foram introduzidos atalhos para os subgrupos, pesquisa com ancestrais e alternância de modos. Os prefixos dos IDs só servem para organizar a **seleção histórica**, e não para estabelecer relacionamentos nem supor grupos editoriais oficiais.

### P2 — Diagrama ilegível | ALTA | confirmado
O HTML V2.0 anexado tinha SVG comprimido para a largura disponível, com excesso de espaço vazio e fluxo vertical. A V2.1 havia iniciado a correção da escala, mas ainda separava o diagrama do MOC e usava cartões pequenos para estruturas com muitos campos.

**Correção:** o modo compacto da V2.2 foi reconstruído com dois painéis de cartões de **570 px**, título do pai, indicação dos filhos, descrição e cardinalidade legíveis. O usuário pode focar um subgrupo, mudar os quatro formatos ou rolar o desenho em escala 100%. SVG e PNG usam as dimensões naturais do conteúdo; não há promessa de imprimir a árvore extensa numa página única.

### P3 — Ausência de sincronização entre visões | ALTA | confirmado
Clicar na linha MOC apenas alterava a ficha técnica; não revelava esse elemento em um diagrama. O retorno do diagrama ao relatório também não estava implementado.

**Correção:** navegação bidirecional por chave do nó com preservação do grupo, expansão de ancestrais e localização da linha. MOC, árvore, diagrama, dicionário e impressão reutilizam os mesmos `nodes`, `byKey`, referências `parent` e filhos.

### P4 — Limitação da base | ALTA | sem resolução nesta versão
O HTML enviado e o catálogo original possuem **196 nós** selecionados. Destes, **42** pertencem ao grupo de referência W. Existem 38 registros `G`, 6 `CG`, 138 `E`, 11 `CE`, 2 `A` e 1 `ID`; são **21 seções por prefixo** no catálogo demonstrativo. Isso não mede a cobertura do MOC vigente.

A página oficial consultada em 24/11/2026 informa atualização até **NT 2026.008 v1.01, publicada em 30/10/2026**. A extração integral e reconciliação de todos os grupos e os schemas XSD oficiais não puderam ser concluídas por falta de acesso de rede no ambiente local do importador. O visualizador XSD permanece sem pacote oficial. Campos não importados exibem `n/i` em tabelas e PDFs, em vez de indicar falsamente que não existem no manual. Fonte: https://moc.sped.fazenda.pr.gov.br/NFe_NFCe/Leiaute.html

### P5 — Impressão do relatório hierárquico | MÉDIA | corrigido no catálogo parcial
O PDF anterior podia preservar tabelas com dez colunas, mas sem os recuos reais de subgrupos. A V2.2 usa a mesma árvore da tela para gerar linhas hierarquizadas, mantendo coluna Pai, tipo, cardinalidade e observação. Incluídos exemplos A4 e A3 com texto pesquisável. O sumário e os modelos Oracle permanecem como opções do sistema original.

### P6 — IDs repetidos e pais ambíguos | MÉDIA | tratamento defensivo
Documentos extensos podem conter IDs ou tags repetidos em contextos distintos. A V2.2 evita resolver automaticamente um pai por um ID que não seja único, e conserva a referência original; nesses casos a montagem da hierarquia exige confirmação do XSD. O catálogo demonstrativo fornecido não possui IDs duplicados, logo esse comportamento exige testes adicionais com esquemas oficiais.

## 2. Exemplo de aceitação da estrutura W

```text
W01 total
├── W02 ICMSTot
│   ├── W03 vBC
│   └── W04 vICMS  ...
├── W17 ISSQNtot
├── W23 retTrib
├── W31 ISTot
│   └── W33 vIS
├── W34 IBSCBSTot
│   ├── W35 vBCIBSCBS
│   └── W36 gIBS
│       ├── W37 gIBSUF
│       │   ├── W38 vDif
│       │   └── W39 vDevTrib
│       └── W42 gIBSMun
└── W60 vNFTot
```

Essa estrutura representa **apenas as relações presentes na seleção de 196 nós**; não afirma que as subdivisões W estejam completas no MOC atual.

## 3. Alterações no código

| Arquivo | Modificação |
|---|---|
| `public/app.js` | Árvore por Pai, modos MOC, expansão e pesquisa, integração de navegação, diagrama compacto redesenhado, impressão hierárquica, segurança para pais ambíguos. |
| `public/index.html` | Seletor de modo, legenda, quadro de divisões, contexto do nó no diagrama e seletor da tabela impressa. |
| `public/styles.css` | Identidade visual por profundidade e categoria, ampliação de blocos, otimização de impressão A4/A3. |
| `public/EXPLORADOR_OFFLINE_COMPLETO.html` | HTML atualizado com JS/CSS embarcados para abertura direta. |
| `tests/test_hierarchy_v22.py` | Testes específicos de integridade W, expansão, pesquisa, 10 colunas, ida/volta e dois PDFs. |
| `VERSION`, `README.md`, `CHANGELOG.md`, este relatório | Versionamento, instruções e auditoria. |
| `docs/v22_verificacao/` | Duas amostras PDF e capturas verificáveis, incluindo celular. |
| `docs/pdf_examples/` | Sete exemplos do teste de impressão anterior atualizados para o programa V2.2. |

Nenhuma alteração foi feita em banco Oracle ou na base histórica de 196 nós. Os importadores, serviços de monitoramento e APIs foram preservados.

## 4. Testes realmente executados

- **6/6** testes unitários do importador/versionamento/XSD fictício: aprovados (`python -m unittest ...`). Não equivalem a uma importação real de schemas oficiais.
- **Teste funcional específico V2.2:** aprovado para 42 registros W, 7 grupos estruturais com filhos, níveis W01 → W34 → W36 → W37 → W38, recolhimento seletivo de W02, pesquisa por W38 recuperando todos os ancestrais e navegação MOC ⇄ Diagrama.
- **Dez colunas** verificadas em tela e no PDF. **42 linhas** mantidas na impressão do Grupo W.
- **Quatro formatos gráficos** e **sete PDFs demonstrativos** passaram no teste de fumaça anterior, recalculados sobre V2.2.
- **Zoom 100%**: dimensões naturais do SVG conferidas no navegador, sem compactação silenciosa.
- **Impressão A4 paisagem**: PDF do Grupo W com 4 páginas; **A3 paisagem**: diagrama compacto W com 3 páginas; texto selecionável confirmado por extração e primeira página renderizada para inspeção visual.
- **Celular (viewport de 390 px):** sem erros de script; `documentElement.scrollWidth` igual à largura da tela. A tabela usa rolagem própria.

Não executados: comparação campo a campo com **todo** o MOC oficial, importação de XSD oficial de produção, teste de monitoramento agendado em hospedagem e auditoria de todas as páginas do manual integral. Não declarar homologação oficial.

## 5. Critérios de aceitação e pendências

1. **Concluído no catálogo parcial:** subgrupos com indicação de pai, vínculo entre relatório e diagrama, pesquisa hierárquica, impressão de grupos específicos e layouts gráficos mais legíveis.
2. **Pendente:** coletar/validar toda a página oficial de dez colunas com ordens originais, descrições e observações; converter cada seção para catálogo versionado e provar cobertura mediante reconciliação de contagens e IDs.
3. **Pendente:** importar pacotes XSD oficiais, resolver `choice` e `sequence`, testar referências duplicadas e validar cardinalidades e tipos por XPath.
4. **Pendente:** ativar agendamento em serviço persistente, notificações e comparação de versões com evidência real de atualização.
5. **Pendente:** provar impressão profissional do leiaute integral com grupos extensos e observações longas, inclusive em A4/A3, após a importação.
6. **Recomendação:** nunca identificar como "completo/oficial" o relatório que contém apenas a seleção anterior. Manter a última versão válida em caso de falhas de coleta.

## 6. Publicação e utilização

Abra `public/EXPLORADOR_OFFLINE_COMPLETO.html` diretamente no navegador. Para funcionamento com backend, execute `python -m pip install -r requirements.txt` e `python scripts/serve.py`. O arquivo HTML isolado não monitora atualizações com o navegador fechado. A sincronização depende de serviço e acesso ao MOC. A versão do código é **v2.2.0-beta.1**. Prefira o ZIP completo quando substituir os arquivos V2.0 enviados, para evitar misturar gerações do aplicativo.

**Conclusão:** a hierarquia e a legibilidade foram corrigidas para os dados comprovadamente disponíveis. **Não** foi concluída a cobertura integral do MOC/XSD; esse é um trabalho de coleta e validação oficial distinto da correção da interface.
