# RELATÓRIO TÉCNICO — Explorador NF-e/NFC-e V2.0.0-beta.1

**Emissão:** 24/11/2026  
**Natureza:** primeira versão da nova arquitetura; homologação técnica com dataset histórico parcial  
**Referência externa conferida:** MOC NF-e/NFC-e atualizado até NT 2026.008 v1.01, publicada em 30/10/2026  
**URL oficial:** https://moc.sped.fazenda.pr.gov.br/NFe_NFCe/Leiaute.html

## 1. Diagnóstico da solução anterior

O HTML A4 da versão anterior é um relatório interativo, baseado em uma seleção de 196 nós do MOC 7.0. Não contém a íntegra de grupos, linhas, observações e mudanças da edição atual do MOC. Sua modelagem Oracle é conceitual e não inclui pacote XSD integral. O novo projeto preserva o HTML e PDF antigos na pasta `legado` para evitar perda da entrega aprovada.

## 2. Arquitetura e armazenamento

A arquitetura possui quatro camadas: catálogo/visualização no navegador; parser MOC em Python; importador de XSD offline e seguro; monitor com snapshots JSON, histórico, diferenças e status. Um servidor Python opcional expõe arquivos estáticos e endpoints de consulta. O agendador diário é GitHub Actions, condicionado à publicação e habilitação das permissões. Não há instalação de banco de dados obrigatória nem integração Oracle ativa.

## 3. Implementado nesta versão

- Navegação por módulos: visão geral, MOC em dez colunas, árvore, dicionário, diagrama, visualizador XSD, Oracle, atualizações e impressão.
- Pesquisa e filtros por grupo/ID/nome e interpretação de pais/filhos e XPath quando determinável.
- Importador das dez colunas oficiais, incluindo campos `#`, `ID`, `Campo`, `Descrição`, `Ele`, `Pai`, `Tipo`, `Ocor.`, `Tam.` e `Observação`.
- Captura de referência de Nota Técnica quando localizada no HTML, identificadores e fonte de origem.
- Análise de XSD em ZIP: tipos, elementos, atributos, restrições, `sequence/choice/all`, includes/imports e arquivo de origem.
- Snapshot atômico, hash SHA-256, histórico, diff e proteção contra atualização incompleta.
- Diagrama SVG com escolha de grupo, profundidade, zoom, exportação SVG e PNG.
- DER conceitual e proposta Oracle, download de SQL sem execução no banco.
- Configurações de impressão A4 retrato/paisagem, capa, seleção por grupo, observações e dicionário.
- Exportação CSV/JSON, XLSX demonstrativo e backend para XLSX após sincronização oficial.
- Interface visual clara e adaptável a telas pequenas.

## 4. Testes realmente executados

**Unidade (Python): 6 de 6 aprovados.** Parser das dez colunas; diferenças incluído/alterado; bloqueio de redução inesperada; preservação do catálogo após erro; análise de ZIP XSD com dependência local; bloqueio de entidade externa maliciosa.

**Navegador (Chromium automatizado):** 9 módulos abriram sem erro de JavaScript. Pesquisa do leiaute, filtro UB, busca de XPath na árvore, filtro do dicionário e seleção de grupo para impressão foram testados nas larguras 1440 px e 390 px.

**PDF:** A4 paisagem de 17 páginas com seleção de 196 nós, cabeçalhos repetidos, capa e numeração. O arquivo foi gerado e as páginas inicial, intermediária e final foram inspecionadas visualmente.

**XLSX:** gerado arquivo de 196 registros com IDs/códigos em texto; a função do servidor para XLSX foi criada e sua estrutura ZIP/XML conferida, sem teste de download em um ambiente HTTP externo.

## 5. Pendências relevantes (não ocultar)

**Crítico para completude documental:** sincronizar a página oficial inteira, validar os grupos e linhas e importar o pacote XSD oficial correto. O backend não pôde baixar a fonte nesta sessão por restrição de rede, embora o portal tenha sido consultado para verificar a NT publicada. **Não é correto declarar esta base completa ou plenamente atualizada.**

**Alto:** resolução integral de tipos e referências XSD entre arquivos, equivalência XPath MOC-XSD, validação de cardinalidade condicional e análise de divergências MOC vs. XSD por versão.

**Alto:** agendador e notificação configurados no ambiente real, permanência de snapshots após deploy e teste real da fonte em GitHub Actions.

**Médio:** exportação XLSX em navegador desconectado do backend, comparativo de versões avançado por NT, PDF muito extenso com observações e análise de impacto Oracle por elemento.

**Médio:** testes de carga, autenticação e segurança de hospedagem, execução SQL em ambiente Oracle de homologação, caso autorizada.

## 6. Arquivos principais

- `public/index.html`, `public/styles.css`, `public/app.js`: interface e relatórios.
- `public/catalogo_selecao_anterior.json`: seleção histórica parcialmente documentada.
- `scripts/catalog_core.py`: parser MOC e controle de qualidade/diff.
- `scripts/xsd_catalog.py`, `scripts/import_xsd.py`: XSD ZIP e metadados.
- `scripts/monitor.py`: consulta diária/manual, snapshots e notificações opcionais.
- `scripts/serve.py`, `scripts/xlsx_export.py`: API e exportações XLSX.
- `.github/workflows/atualizar_moc.yml`: rotina agendada (depende de habilitação).
- `docs/RELATORIO_LEIAUTE_DEMONSTRATIVO_A4.pdf`: PDF de exemplo parcial.
- `docs/DICIONARIO_SELECAO_DEMONSTRATIVA.xlsx`: Excel de exemplo parcial.
- `legado/`: versão anterior do relatório aprovado.

## 7. Implantação

1. Extraia o ZIP completo em uma pasta; abra `public/index.html` para navegar offline.
2. Para obter dados oficiais dinâmicos, instale `requirements.txt`, execute `python scripts/monitor.py` em uma máquina com acesso ao site e confira as linhas extraídas contra o MOC.
3. Importe o ZIP dos XSD oficiais com `python scripts/import_xsd.py CAMINHO.zip`; confira nomes e versões dos arquivos.
4. Execute `python scripts/serve.py` ou publique com `render.yaml`.
5. Para monitoramento diário, habilite GitHub Actions e escrita dos snapshots no repositório. Configure `ADMIN_TOKEN` e, caso deseje email, variáveis SMTP como segredos.
6. Confira as alterações, revise as regras fiscais com especialista e gere PDF/XLSX definitivos somente após aprovar a cobertura.

**Integridade de produção:** nenhuma DDL Oracle foi executada; nenhum histórico fiscal foi alterado; nenhuma atualização externa/agenda foi habilitada automaticamente.
