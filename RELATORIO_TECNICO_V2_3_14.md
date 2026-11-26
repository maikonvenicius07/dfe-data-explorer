# DF-e Data Explorer — V2.3.14-beta.1
## Auditoria e simplificação de controles

Base: ZIP enviado pelo usuário `dfe-data-explorer-main (1)(1).zip`, versão 2.3.13-beta.1, 142 arquivos. A base publicada incluída no ZIP contém 1.173 registros extraídos do HTML do MOC em 25/11/2026, NT 2026.008 v.1.01; o catálogo embutido offline mantém 196 registros demonstrativos. Não houve nova coleta, validação XSD nem mudança de dados.

## 1. Diagnóstico e decisões

| Redundância / problema | Ação |
|---|---|
| Imprimir relatório no cabeçalho, Preparar impressão no título e Imprimir selecionados na barra | Removidos os dois primeiros; mantido Imprimir selecionados e acesso à Central pelo menu |
| Árvore de seleção repetida na Central | Retirada da interface e removida sua lógica de renderização e eventos; seleção no MOC |
| Lista de revisão repete a tabela da prévia | Removida; botão × por linha na própria prévia permite retirar campos; botão não pertence ao documento impresso |
| Atualizar prévia, apesar de atualização automática | Retirado; alterações de configuração e seleção regeneram a prévia |
| Checkbox Observações e coluna Observação | Controle único na configuração de colunas |
| Selecionar filtrados e Selecionar documentação quando filtro abrange toda a base | Um único comando Selecionar tudo nessa situação; comando integral reaparece ao restringir filtro |
| Desmarcar filtrados e Limpar seleção quando filtro abrange toda a base | Mantido Limpar seleção; Desmarcar filtrados reaparece quando filtro restringe a base |
| Dois contadores do MOC | Um indicador de registros filtrados/total e selecionados |
| Link oficial repetido na área de atualizações | Mantido o link do cabeçalho |
| Referência fixa no menu lateral | Retirada; informações reais do catálogo continuam na área Atualizações e no relatório |
| Metadados de impressão ignoravam `technicalNote` e `extractedAt` | Impressão utiliza esses campos quando presentes, sem inventar versão |

Mantidos os comandos de marcar e desmarcar filtrados quando distintos, Expandir tudo e Recolher subgrupos (ações de visualização), +/− filhos e seleção individual. A seleção progressiva pela seta continua marcada apenas no nível aberto. Salvar/carregar/excluir seleções permanecem em área opcional recolhível. PDF direto, impressão do navegador e CSV são saídas distintas, não duplicidades. As dez colunas continuam disponíveis e selecionadas por padrão. As quatro áreas públicas permanecem; não se excluem módulos internos históricos ou formatos de arquivo necessários à compatibilidade.

## 2. Auditoria de arquivos e limites da limpeza

A comparação de SHA-256 da base identificou cópias idênticas entre `data/`, `public/data/` e o snapshot atual. São intencionais (persistência, publicação estática e histórico); foram preservadas. Arquivos vazios `.gitkeep`/`.nojekyll` cumprem funções distintas. O `publicar_paginas.yml` da raiz é idêntico ao workflow ativo; há também um `validar.yml` antigo em subpasta de workflows. Esses arquivos não são workflows ativos adicionais no GitHub Actions. Foram mantidos para evitar exclusões estruturais fora do escopo da interface e para que a atualização incremental não exija apagar arquivos. Relatórios e testes históricos preservados; controles ocultos de módulos legados não são acessíveis pelo menu. Não se reivindica auditoria de segurança, desempenho de produção, ou completude fiscal da base. A limpeza é focada nos controles repetidos da interface atual.

## 3. Testes executados

- Node: quatro arquivos JS de teste passaram (seleção, expansão, marcação em lote e integração).
- Python: nove testes de importação e publicação passaram.
- Chromium: regressão V2.3.12 de expansão progressiva passou.
- Chromium: nova regressão V2.3.14 passou com 196 nós e com os 1.173 nós do catálogo real fornecido. O catálogo amplo foi injetado exatamente a partir de `public/data/catalogo_atual.json` na versão standalone; armazenamento local simulado para testar presets, pois navegação direta por URL local foi bloqueada pelo ambiente. Não foi testada a implantação remota. A seleção, filtros, marca/desmarca, prévia, remoção, presets, escolha de colunas, PDF direto e PDF via navegador foram conferidos.
- PDFs A4 paisagem, A4 retrato e A3 paisagem gerados pelo código da aplicação nos dois catálogos, com texto extraído para verificar inclusão/exclusão e orientação. PDF A4 paisagem via navegador também gerado. Inspeção visual do exemplo da base ampla: tabela sem diagrama ou lista adicional.
- Sintaxe do app.js verificada. Testes antigos que dependem da árvore de impressão retirada ou das telas removidas anteriormente são históricos; não foram executados como critérios atuais.
- Não foi testada uma impressora física, GitHub Pages remoto ou sincronização externa nesta entrega.

## 4. Publicação

Atualizar o repositório com os arquivos do ZIP incremental (base: ZIP fornecido pelo usuário), preservando caminhos. Alternativamente usar ZIP completo. Não é necessário excluir arquivos do repositório. Após o deploy, recarregar com Ctrl+F5, verificar versão 2.3.14 e selecionar alguns registros de grupos distintos. Na Central, revisar a tabela, retirar um registro e gerar PDF. Confirmar que os dados oficiais publicados permanecem disponíveis.
