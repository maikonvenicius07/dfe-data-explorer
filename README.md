# DF-e Data Explorer — NF-e e NFC-e

**Versão do aplicativo:** V2.3.1-beta.1 · **Base embutida:** seleção demonstrativa anterior, 196 nós.

> Projeto independente de documentação técnica. Não é uma publicação oficial do Fisco. A fonte de referência é o [MOC NF-e/NFC-e](https://moc.sped.fazenda.pr.gov.br/NFe_NFCe/Leiaute.html). Nenhum resultado do catálogo parcial deve ser confundido com cobertura oficial completa.

## Abrir imediatamente

Abra `public/EXPLORADOR_OFFLINE_COMPLETO.html` no navegador. Não necessita instalar nada. Também é possível executar `python scripts/serve.py` e acessar `http://localhost:8000`, para usar o servidor opcional.

## Recursos preservados e ampliados

- A aplicação abre diretamente no Leiaute do MOC; a tela Visão Geral foi retirada por solicitação do usuário.
- Leiaute MOC nas dez colunas e modo hierárquico com subgrupos.
- Explorador, ficha do campo, dicionário de dados com filtros, ordenação e colunas selecionáveis.
- Diagramas horizontal, vertical, compacto e DER **proposto**, não oficial.
- Central de Impressão com árvore de caixas de seleção: grupo, subgrupo, subdivisão, elementos e atributos; seleção parcial, pesquisa e conjuntos salvos no navegador.
- Os pais não selecionados entram **apenas como contexto** no relatório hierárquico, com identificação visual. As contagens e exportação CSV consideram os campos efetivamente marcados.
- PDF A4/A3 pelo navegador, relatórios por grupo, comparativos e modelagem Oracle; catálogo XSD, monitoramento e histórico se houver dados verificados.

## Repositório permanente e publicação sem reconstruir o projeto

Consulte [docs/PUBLICACAO_GITHUB.md](docs/PUBLICACAO_GITHUB.md) para os passos de instalação, configuração do GitHub Pages, rotina agendada e recuperação de versões. Os workflows já estão incluídos, porém **nenhum repositório foi criado ou publicado automaticamente**.

**Fluxo incremental recomendado:** 1. baixar e preservar a última versão; 2. comparar os arquivos; 3. modificar apenas o necessário; 4. testar; 5. atualizar `VERSION`, `CHANGELOG.md` e relatório; 6. enviar commit; 7. publicar; 8. preservar tags de versões anteriores.

## Limitações importantes

1. O catálogo de 196 nós continua demonstrativo e não garante completude do MOC. Os XSD oficiais não foram importados/validados nesta entrega.
2. A rotina agendada está preparada, mas só será executada após a configuração do GitHub e ativação do Actions. A implantação no Render exige configurar `ADMIN_TOKEN` e armazenamento persistente.
3. A seleção salva utiliza `localStorage` do navegador; não é sincronizada entre computadores e pode ser apagada quando os dados locais do navegador forem limpos.
4. O XLSX gerado pelo backend utiliza o catálogo oficial completo armazenado no servidor; **não** aplica a seleção da impressão. Para exportar exatamente os campos marcados, utilize CSV da Central de Impressão.
5. Não foi feita publicação externa, nem teste de infraestrutura do GitHub Pages, Render ou de atualização real no site oficial nesta versão.

## Verificações

Execute `node tests/test_selection_logic_v23.js`, `python tests/test_productivity_v23.py`, `python tests/test_fullscreen_only_v221.py` e `python -m pytest -q tests/test_import.py`. Executados localmente com aprovação. A suíte gráfica completa das versões antigas possui um caso extenso não concluído no limite local; consulte o relatório.

Arquivos para manter sincronizados: `public/index.html`, `public/styles.css`, `public/selection.js`, `public/app.js` e `public/EXPLORADOR_OFFLINE_COMPLETO.html`. Ao alterar o código, execute `python scripts/build_offline.py`; ao importar MOC validado, execute `python scripts/build_static.py`.
