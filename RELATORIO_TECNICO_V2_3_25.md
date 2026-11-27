# DF-e Data Explorer — V2.3.25-beta.1

## Objetivo e base

Implementar monitoramento automático diário dos leiautes de todos os documentos fiscais já disponíveis, histórico individual, avisos e republicação explícita do GitHub Pages. Base: ZIP `dfe-data-explorer-main (3)(2).zip`, V2.3.24-beta.1. Os 14 catálogos existentes, com 5.830 registros, foram preservados byte a byte. Nenhum registro fiscal simulado foi incluído na produção. Não houve alteração da hierarquia, seleção ou leiaute de impressão aprovado.

## Implementação

- `scripts/monitor_documents.py`: consulta dez fontes HTML para os 14 catálogos e variantes, compartilhando a resposta das famílias CT-e e BP-e. Compara campos, ordem, grupos, referência do manual, NT e valores da fonte disponíveis. Mudanças meramente no HTML sem alteração técnica não substituem o catálogo. Registra data de tentativa, sucesso, erros, contagem e situação por documento. Salva snapshots anteriores/novos em `data/documents/<documento>/snapshots/`, preserva o histórico legado NF-e e gera `public/data/monitoramento.json`.
- Segurança: valida identidade, chaves, cobertura estrutural, tabelas, seções e vínculos; bloqueia exclusões/identidades removidas, perda de tabelas/seções e aumento de inconsistências. As exclusões são apresentadas como propostas pendentes, sem aprovação automática. Erros são isolados por documento, sem apagar comparações pendentes anteriores; erro de gravação ou preparação impede commit no workflow. A validação estrutural é conservadora, não equivale à validação fiscal integral ou XSD.
- `.github/workflows/importar_documentos.yml`: agendamento diário às 11:17 UTC (07:17 em Rondônia), execução manual all/individual e disparo por mudança dos scripts/workflow. Testa antes de coletar, prepara HTML online/offline, grava dados e solicita explicitamente o deploy do Pages após o commit. Se houver fontes com falha/revisão, publica os diagnósticos e encerra com status de atenção (falha). Exporta artefato `cobertura-documentos`. A publicação real depende da configuração e permissões do GitHub.
- `.github/workflows/atualizar_moc.yml` e `importar_dce.yml`: atalhos manuais para a mesma rotina; não duplicam agendamento. `publicar_paginas.yml` usa a versão atual da main e serializa publicações. `validar.yml` inclui os testes do monitor. `COPIAR_PARA_WORKFLOW_GITHUB.txt` contém cópia idêntica do workflow atualizado.
- `public/app.js` e `public/index.html`: central de monitoramento dos 14 catálogos, status individual, última tentativa e sucesso, NT, contador de avisos não lidos, comparações por data e documento, busca e CSV. O contador usa armazenamento local do navegador. Consulta ao relatório não altera a seleção nem dispara coleta remota. Avisos e comparações bloqueadas permanecem distinguíveis de atualizações aprovadas. O histórico legado permanece disponível.
- `scripts/build_offline.py`: incorpora relatório do monitor ao HTML offline. `public/EXPLORADOR_OFFLINE_COMPLETO.html` é reconstruído. `VERSION`, assets e rodapé PDF identificam V2.3.25.
- E-mail SMTP opcional: envia resumo de alterações aprovadas após commit e solicitação de publicação se os segredos SMTP forem configurados. Não envia sem credenciais; não certifica conclusão do deploy. Falhas de envio ficam no log. Nenhuma credencial foi incluída.

## Testes locais realizados

- 42 testes Python passaram: importação, comparação, coleta compartilhada, preservação dos 14 catálogos sem mudança, isolamento de falhas, atualização NF3-e simulada, histórico NF-e, inclusão, bloqueio de redução de registros/tabelas e piora hierárquica, persistência de pendência em falha posterior, consistência da publicação. Fixtures são separadas da produção.
- Quatro suítes JavaScript passaram: seleção, expansão, descendentes e contexto integrado. `node --check` do aplicativo passou.
- Chromium: central com 14 documentos, comparativo anterior/atual e falha isolada (respostas injetadas); navegação pelos 14 catálogos reais, seleção/filtro preservados e zero erros JS. PDF NF-e W22 gerado pelo aplicativo em A4 retrato, uma página e 22 registros; amostra em `docs/v2325/nfe-W22.pdf`, conferida visualmente. Não é teste de publicação HTTP remota.
- `scripts/prepare_release.py` concluído: registro e HTML offline sincronizados. Validação binária dos ZIPs e dos catálogos feita na entrega.

## Limitações e decisões

Não executei o novo workflow no GitHub do usuário nem realizei uma coleta integral real nesta sessão. Os testes de mudanças utilizaram respostas simuladas, além dos catálogos reais já presentes no ZIP. O monitor começa com estado **Aguardando primeira verificação**, não com sucesso fictício. A execução diária depende de Actions habilitadas, acesso às fontes, permissões para gravar main e configuração de Pages. Agendamentos podem atrasar ou ser suspensos. Uma requisição de deploy bem-sucedida não confirma a publicação. Recomendo Settings → Pages → GitHub Actions. O SMTP não foi testado com servidor/credenciais reais. O acompanhamento de arquivos XSD ou novas NT fora das páginas Leiaute permanece pendente; os importadores HTML existentes não certificam o conteúdo fiscal integral. Exclusões e mudanças potencialmente incompletas foram deliberadamente bloqueadas para proteger a base; precisam de revisão do manual/importador antes de atualização. O monitor pressupõe catálogo de referência já existente; o importador inicial anterior permanece disponível. O histórico novo cresce ao longo do tempo e deve ser acompanhado.

## Instalação e próximos passos

Siga `LEIA_PRIMEIRO_V2325.md`. Atualize os arquivos na raiz do repositório main. Abra Actions → Importar leiautes de todos os DF-e → Run workflow → all, se não houver execução em andamento; acompanhe o resultado e a publicação. Acesse a Central de atualizações no site e verifique última tentativa/sucesso por documento. Não é necessário importar os 14 catálogos novamente.

## Arquivos novos/alterados

- `.github/workflows/atualizar_moc.yml` — alterado
- `.github/workflows/importar_dce.yml` — alterado
- `.github/workflows/importar_documentos.yml` — alterado
- `.github/workflows/publicar_paginas.yml` — alterado
- `.github/workflows/validar.yml` — alterado
- `ARQUIVOS_SHA256.txt` — alterado
- `CHANGELOG.md` — alterado
- `COPIAR_PARA_WORKFLOW_GITHUB.txt` — alterado
- `LEIA_PRIMEIRO_V2325.md` — novo
- `README.md` — alterado
- `RELATORIO_TECNICO_V2_3_25.md` — novo
- `VERSION` — alterado
- `docs/PUBLICACAO_GITHUB.md` — alterado
- `docs/v2325/nfe-W22.pdf` — novo
- `public/EXPLORADOR_OFFLINE_COMPLETO.html` — alterado
- `public/app.js` — alterado
- `public/data/monitoramento.json` — novo
- `public/index.html` — alterado
- `public/pdf-export.js` — alterado
- `scripts/build_offline.py` — alterado
- `scripts/monitor_documents.py` — novo
- `tests/fixtures/dce_v2324.json` — novo
- `tests/test_browser_monitor_v2325.py` — novo
- `tests/test_import_dce.py` — alterado
- `tests/test_monitor_documents_v2325.py` — novo

Nenhum arquivo excluído. O manifesto SHA-256 foi regenerado para refletir a entrega.
