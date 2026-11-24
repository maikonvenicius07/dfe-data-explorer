# Pendências — DF-e Data Explorer V2.3.3

- **Cobertura fiscal incompleta:** o catálogo incluído tem 196 registros selecionados. Não é uma extração integral certificada do MOC vigente.
- **Validação XSD:** o pacote oficial ainda não foi conferido completamente; tipos e relações dependem dessa etapa.
- **Monitoramento:** a rotina preparada para GitHub Actions depende de configuração operacional, permissões e verificação do resultado em produção.
- **Exportação XLSX:** a exportação dinâmica do backend ainda não respeita necessariamente a seleção manual do navegador; para seleção exata, usar relatório/PDF e CSV selecionado.
- **Seleções salvas:** os perfis são armazenados no navegador local; não há sincronização entre aparelhos.
- **DER/Oracle:** propostas conceituais não são mapeamentos certificados dos campos e não devem ser executadas automaticamente.
- **Testes de regressão extensos:** parte da suíte gráfica legada não terminou dentro do limite do ambiente de teste; revisar após publicação.
- **Paginação:** o número de páginas varia por fonte/navegador; exemplos A4 foram verificados, não todas as combinações de relatórios longos.
