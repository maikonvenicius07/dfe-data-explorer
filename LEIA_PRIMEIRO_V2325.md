# Ativar o monitoramento automático — V2.3.25-beta.1

1. Atualize a branch `main` com o conteúdo do ZIP incremental, a partir da raiz do repositório. Preserve os caminhos, inclusive `.github/workflows/`. Não envie o ZIP fechado.
2. Em Settings → Actions → General, confirme que Actions estão habilitadas e que o workflow pode gravar os arquivos da branch main. Se houver proteção de branch que impeça o push automatizado, será necessária uma política de aprovação/PR.
3. Preferencialmente configure Settings → Pages → Source: GitHub Actions. O workflow publica `index.html` na raiz e o aplicativo em `/public/`. Para publicação por branch, o monitor tenta solicitar explicitamente a construção via API; se a permissão for negada, use GitHub Actions.
4. Abra Actions → **Importar leiautes de todos os DF-e** → Run workflow → `documento: all` → Run workflow. Uma mudança no script/workflow na main também pode disparar a primeira execução. Não há necessidade de repetir se uma execução já estiver em andamento.
5. Confira a execução, o artefato `cobertura-documentos`, o commit e o workflow `Publicar Explorador no GitHub Pages`. Uma execução vermelha pode indicar uma fonte com falha enquanto as demais foram atualizadas e publicadas. Veja os detalhes do log. Não confunda solicitação de publicação com publicação concluída.
6. Acesse o site e a tela **Atualizações e histórico**. Confira as datas da última tentativa e do último sucesso para cada catálogo. A versão entregue começa com `Aguardando primeira verificação` porque ainda não houve uma coleta real pelo novo monitor.

## Agendamento

Todos os dias às 11:17 UTC (07:17 de Rondônia). O GitHub pode atrasar ou suspender agendamentos; acompanhe a atividade. Não é necessário manter seu computador ligado. O antigo workflow exclusivo da NF-e é agora um atalho manual; não há dois agendamentos concorrentes.

## Segurança dos dados

Alterações de campos, metadados e inclusões que passam pelas verificações estruturais substituem o catálogo. Exclusões, perda de tabelas/seções ou aumento de vínculos hierárquicos não resolvidos exigem revisão manual. O comparativo fica visível sem substituir o catálogo existente. Uma falha de rede não apaga uma comparação pendente anterior. A extração HTML não certifica XSD nem cobertura integral. Não force a publicação de um catálogo rejeitado: confira a fonte e a integridade antes de ajustar o importador.

## Notificações

O contador da Central indica novas alterações publicadas e comparações pendentes não marcadas como lidas neste navegador. O histórico pode ser pesquisado e exportado para CSV. O botão de consulta lê o relatório publicado, não dispara uma coleta no servidor. O arquivo offline contém o último relatório incorporado e só muda ao baixar uma cópia nova.

Para e-mail opcional, configure em Settings → Secrets and variables → Actions → New repository secret: `SMTP_HOST`, `SMTP_PORT` (opcional, padrão 465), `SMTP_FROM`, `SMTP_TO`, `SMTP_USER`, `SMTP_PASSWORD`. O envio usa SMTP sobre TLS e ocorre após o commit e a solicitação de publicação, apenas se houver alterações aprovadas. Não inclui confirmação do deploy nem alerta de erro de fonte por e-mail. Sem credenciais, não envia mensagens. Não coloque senhas em arquivos.

## Execução local (opcional)

`pip install -r requirements.txt`

`python scripts/monitor_documents.py --document all`

Também aceita uma chave (`nfe`, `dce`, `cte`, `cteos`, `gtve`, `abi`, `nfgas`, `nfag`, `nf3e`, `nfcom`, `bpe`, `bpetm`, `bpeta`, `mdfe`). Use `--html-dir pasta` para HTML salvo, `nfe.html` para NF-e e as chaves/pastas previstas no importador para os outros manuais. O comando retorna 3 se houver fontes que requerem atenção. O importador anterior continua disponível para importação inicial; o monitor diário pressupõe um catálogo de referência existente. A publicação local depende de commit e push.
