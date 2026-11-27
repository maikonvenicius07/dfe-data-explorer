# V2.3.26 — atualização segura no GitHub

**Use preferencialmente o ZIP incremental.** O ZIP completo é uma cópia do último arquivo enviado pelo usuário, anterior à execução de monitoramento que foi observada no GitHub. Não substitua os dados mais recentes do repositório por essa cópia.

1. Extraia o ZIP incremental e sobreponha os arquivos no diretório raiz do projeto, mantendo `.github/workflows/` diretamente na raiz. Não crie outra subpasta `workflows`.
2. Não remova nem substitua os arquivos em `data/` ou `public/data/` do repositório atual. O incremental não contém esses diretórios. O HTML offline incluído é um artefato derivado do ZIP-base; o fluxo Pages o reconstrói com os dados atuais. Para uso offline direto do repositório, execute `python scripts/prepare_release.py` após aplicar os arquivos e antes do commit.
3. Em Settings > Pages > Source selecione GitHub Actions. Modo branch ainda pode publicar, mas não tem o novo comprovante verificável. Não altere as permissões além das previstas pelos workflows.
4. Em Actions > Publicar Explorador no GitHub Pages, execute o workflow na branch main (ou aguarde o disparo por push). Confira as etapas de build, deploy e **Confirmar versão e catálogos no endereço público**. Essa última etapa precisa passar: somente um deploy verde anterior não é confirmação do novo artefato.
5. Abra `/public/`, pressione Ctrl+F5, consulte Atualizações e histórico. Confira V2.3.26 e o commit exibido. O arquivo `/public/publicacao.json` é criado no artefato de Pages, não no repositório.
6. A rotina `Importar leiautes de todos os DF-e` mantém o agendamento de 07:17 (Rondônia) e solicita publicação após o registro da rodada. A execução do importador e a confirmação da publicação são dois workflows distintos.

Se o comprovante não estiver disponível, confira se Pages está em modo GitHub Actions. Uma divergência pode resultar de cache, propagação ou pacote inconsistente. Se a verificação falhar, leia o passo que identifica o arquivo; não é necessário importar tudo novamente.

O comprovante não é assinatura digital nem garantia de integridade fiscal dos manuais. Compara os bytes efetivamente preparados com os bytes recebidos do site. Não verifica se houve alterações futuras nos XSD.
