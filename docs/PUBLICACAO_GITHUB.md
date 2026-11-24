# Publicação e continuidade do projeto

## Caminho recomendado: GitHub Pages + GitHub Actions

**O que está preparado:** o workflow `.github/workflows/publicar_paginas.yml` publica a pasta `public/`; `.github/workflows/atualizar_moc.yml` agenda uma verificação diária e, somente se validada, copia o catálogo ao site estático. O aplicativo também roda localmente pelo HTML único.

**O que precisa ser feito pelo proprietário do GitHub:**

1. Criar um repositório preferencialmente público chamado `dfe-data-explorer`, sem dados sensíveis.
2. Enviar **o conteúdo da pasta raiz do ZIP completo** para a branch `main`, preservando a pasta `.github/` (arquivos ocultos incluídos).
3. No GitHub, acessar **Settings → Pages → Build and deployment → Source: GitHub Actions**.
4. Em **Actions**, executar `Publicar Explorador no GitHub Pages` caso ainda não tenha rodado. Conferir o endereço em **Settings → Pages** após publicação. O endereço depende do dono do repositório, portanto não foi inventado aqui.
5. Em **Actions**, testar manualmente `Verificar leiaute oficial MOC` e conferir o log da extração e a validação. Em caso de falha, a última base válida deve permanecer, e a falha precisa ser investigada.
6. Acompanhar o primeiro deploy e verificar se a UI carrega os dados certos. Sem uma base oficial sincronizada, ela mostrará apenas a seleção de 196 nós, com aviso visível.

### Recomendação de segurança

- Não publicar tokens, senhas, documentos fiscais com dados pessoais ou arquivos XML de contribuintes no repositório.
- `ADMIN_TOKEN` deve ser variável de ambiente do servidor privado, não texto do código.
- O GitHub Actions precisa de permissões para gravar em `data/` e `public/data/` para manter snapshots no repositório. Em repositórios com branch protegida, use uma política de aprovação/PR.
- Agendamentos do GitHub Actions podem atrasar ou falhar. Inspecione as execuções; não assuma que a ausência de alerta implica documentação atualizada.
- O histórico de snapshots cresce e exige política de retenção/arquivamento antes de escalar.

## Comparativo da publicação (sem custos contratados)

| Solução | Interface/relatório | Agendamento/atualização | Principal limitação |
|---|---|---|---|
| GitHub Pages | HTML/CSS/JS, filtros, PDF via navegador e JSON estático | Actions em workflow, atualizando arquivos versionados | Sem API dinâmica ou banco residente; repositório público no plano Free |
| Render Static Site | Mesma interface estática | Agenda externa ou serviço separado | API Python não está dentro do static site |
| Render Web Service | Interface e servidor Python com APIs de atualização | Serviço agendado separado, GitHub Actions ou cron | Plano Free pode hibernar com inatividade; não supor armazenamento local persistente |
| Vercel ou Netlify | HTML estático com boa entrega | Funções/tarefas conforme plano e limites | Monitor diário e persistência exigem configuração adicional |

**Caminho sugerido para começar:** GitHub Pages com GitHub Actions e catálogo versionado, por simplicidade e menor custo. Se for necessário endpoint de sincronização e estado de muitos usuários, avaliar Render ou serviço com banco persistente. Os preços/limites podem mudar; verificar diretamente com o fornecedor antes de contratar.

## Comandos opcionais (terminal com Git instalado)

```bash
git init
git add .
git commit -m "feat: consolidar explorador V2.3.0"
git branch -M main
git remote add origin https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git
git push -u origin main
git tag v2.3.0-beta.1
git push origin v2.3.0-beta.1
```

Substitua `SEU_USUARIO` e `SEU_REPOSITORIO` pelos seus dados. A URL acima é **um modelo**, não um repositório real.

## Em futuras entregas

1. Utilizar a última tag/commit do projeto como base; testar regressão antes e depois.
2. Manter o ZIP incremental com **somente** arquivos criados ou alterados; exclusões devem ser listadas no relatório, não presumidas.
3. Usar `python scripts/build_offline.py` depois de qualquer edição em CSS, JS ou HTML.
4. Preservar a base e snapshots de versões antigas. Nunca eliminar a história para resolver problema visual.
5. Antes do deploy, confirmar o aviso de cobertura parcial enquanto não houver validação do MOC integral + XSD.

## Fontes de referência

- https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages
- https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows
- https://render.com/docs/free
