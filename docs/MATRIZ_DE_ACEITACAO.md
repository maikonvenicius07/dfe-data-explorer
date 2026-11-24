# Matriz de aceitação — Explorador NF-e/NFC-e

| Área | Critério verificável | Estado desta entrega |
|---|---|---|
| Fonte oficial | Identificar fonte e versão publicada | Confirmado por consulta ao portal: NT 2026.008 v1.01 (30/10/2026) |
| Coleta | Extrair dez colunas e grupos das tabelas HTML | Testado com HTML representativo; **não executado contra a página integral online** |
| Cobertura | Capturar todos os grupos e observações vigentes | **Pendente de sincronização real e auditoria de cobertura** |
| Árvore XML | Expandir/recolher, pesquisar e selecionar campos | Executado em navegador em desktop e mobile |
| Dicionário | Filtrar, listar e exportar CSV e JSON | Executado em navegador em desktop e mobile |
| Diagrama | Mostrar nós, zoom, escolha de grupo e exportação SVG/PNG | Diagrama e controles funcionais; exportação não auditada visualmente em todos os grupos |
| XSD | Importar ZIP seguro, identificar tipos, facets e referências locais | Testes unitários de ZIP de exemplo aprovados; pacote oficial pendente |
| MOC-XSD | Cruzamento de ocorrências por caminho XML, divergências | **Pendente; sem substituições de dados não comprovadas** |
| MOC oficial | Imprimir dez colunas, incluindo observações | Gerador disponível; PDF de seleção histórica conferido visualmente |
| PDF | A4 paisagem/retrato com capa, numeração, cabeçalhos | PDF A4 de seleção histórica gerado e inspecionado (17 páginas) |
| Excel | XLSX da seleção e XLSX oficial via backend | Arquivo demonstrativo gerado; backend codificado e testado como estrutura ZIP |
| Oracle | Proposta de entidades e SQL comentado para download | Disponível; não executado em Oracle real |
| Persistência | Snapshot, hash, diff e recusa de coleta incompleta | Testes de unidade aprovados; ambiente de produção pendente |
| Agendamento | Verificação diária sem navegador aberto | Workflow configurado; **não habilitado nem executado em conta externa** |
| Notificações | Aviso interno e envio SMTP opcional | Lógica disponível; SMTP não configurado nem testado |
| Auditoria | Testes de parser, proteção de dados e XSD malicioso | 6 testes de unidade aprovados |
| Segurança | Restringir atualização manual por token | Código revisado; testes de penetração não executados |
| Escalabilidade | Suportar todos os campos e muitos acessos simultâneos | **Sem medição de carga real** |

## Critério de aprovação para publicação institucional

Não declarar a base integral ou oficialmente conferida sem (1) coleta MOC válida e cobertura de grupos, (2) importação do pacote XSD relevante e conferência de divergências, (3) revisão humana das regras fiscais e (4) inspeção do PDF completo com observações extensas. Isso deve ocorrer **antes** de usar os resultados em processos de fiscalização, ETL produtivo ou decisões de estrutura Oracle.
