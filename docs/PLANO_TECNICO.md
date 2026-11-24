# Planejamento técnico e riscos

## Decisões arquiteturais

**Navegador:** HTML, CSS e JavaScript sem frameworks, executável localmente. Renderização de árvore e tabelas usa catalogação em memória; para volumes maiores, aplicar paginação ou virtualização.

**Coleta:** Python (`urllib`, BeautifulSoup) captura exclusivamente a URL oficial; identifica tabelas de dez colunas, grupos, IDs, pais, tipos, ocorrências e textos. O teste de integridade utiliza quantidade mínima conservadora de linhas, presença de estruturas essenciais e rejeição de perdas súbitas.

**Histórico:** snapshots JSON com hash SHA-256 de conteúdo técnico, escrita atômica, arquivo atual e comparação de propriedades relevantes. JSON foi escolhido por portabilidade e controle em Git; o projeto não precisa de conexão Oracle para funcionar.

**XSD:** parser seguro baseado em `defusedxml`; os schemas vêm de um ZIP enviado pelo responsável. `include/import/redefine` são listados e `include` local é conferido sem carregar URLs externas. O leitor mantém contextos de declaração para diferenciar nomes repetidos. Falta implementar resolução semântica completa de `type/ref`, derivação de tipos e cruzamento definitivo com o MOC.

**Monitoramento:** GitHub Actions em frequência diária (sujeito a atrasos, indisponibilidade da fonte e restrições da conta). Fail-safe: `catalogo_atual.json` não é trocado se o parser ou a validação falha. Uma falha deve permanecer visível no status; avisos persistentes de falha e retentativas com backoff são evolução recomendada.

**Oracle:** SQL de demonstração para Oracle 19c+; tratar CNPJ, CPF, códigos, modelos, série e chaves como texto para preservar zeros à esquerda. Usar timestamps com fusos quando a origem define zona. Valores monetários com `NUMBER(p,s)`, sujeitos a validação dos limites XSD. Nenhum script é executado automaticamente.

## Riscos e mitigação

1. **Mudança no HTML oficial**: parser pode deixar de localizar tabelas. Mitigação: gate de integridade e retenção do último snapshot aprovado.
2. **MOC diferente do XSD publicado**: documentos podem descrever fases distintas. Mitigação: registrar versão de cada fonte e não sintetizar equivalência sem verificar.
3. **Persistência no Render free**: disco pode desaparecer/reiniciar. Mitigação: versionar snapshots via GitHub Actions; para serviço crítico usar armazenamento persistente.
4. **Dependência de cron externo**: agenda pode atrasar. Mitigação: registrar última tentativa, erro e data de última atualização.
5. **Regra de grupo vs. árvore XML**: um grupo editorial não é necessariamente nó XML. Mitigação: manter metadados editoriais separados da árvore derivada das referências pai.
6. **Cardinalidade condicional**: ocorrência local do XSD não equivale à obrigatoriedade global. Mitigação: diferenciar `choice`, pais opcionais e regras condicionais.
7. **PDF longo**: dez colunas e observações extensas podem gerar páginas adicionais. Mitigação: A4 paisagem, cabeçalho repetido, revisão visual final e opção de imprimir um grupo.
8. **Dados de segurança**: XML importado pode conter entidades maliciosas. Mitigação: sem DTD externas, limites de tamanho e leitura offline.

## Próximas fases

**Fase A:** sincronização real, auditoria manual de cobertura, tabela de divergências MOC-XSD e enriquecimento de XPath.
**Fase B:** modelos analíticos Oracle revisados, dicionário completo com tipo XSD por caminho e SQL de ETL com testes.
**Fase C:** comparação avançada por NT, e-mails de notificação validados, exportação PDF por grupo com QA visual sistemático.
**Fase D:** implantação persistente, testes de concorrência, observabilidade e revisão de segurança.
