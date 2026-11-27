# DF-e Data Explorer — V2.3.24-beta.1

## Objetivo e diagnóstico
Base: ZIP `dfe-data-explorer-main (7).zip`, commit ed98eab, versão 2.3.23-beta.1. Comparação por caminho e conteúdo com o ZIP completo entregue anteriormente: idênticos. O usuário informou apenas “deu erro”; o erro exato não foi identificado. A consulta pública ao site retornou V2.3.21, enquanto o ZIP é V2.3.23. Essa observação pode refletir cache ou versão publicada anterior; não confirma o estado visto pelo usuário. O histórico público de Actions mostrou falhas em execuções anteriores (por exemplo, #30, commit 81c0063, exit code 1), mas os logs completos exigem login e não foram acessados. Não se atribui a falha específica a um teste sem seu log.

Problemas concretos encontrados:
1. `public/index.html`, `seedData`: base inicial de 196 nós, embora `public/data/catalogo_atual.json` contenha 1.173. Falha na requisição podia manter a demonstração.
2. `public/app.js`, `fetchServer`: JSON auxiliar malformado rejeitava Promise.all; a normalização do catálogo e a atualização dos demais recursos eram interrompidas. Em Pages, tentava caminhos absolutos `/api` sem backend. Normalização desnecessária podia redefinir a navegação quando o mesmo snapshot já estava carregado.
3. Publicação e verificação: não havia uma única etapa de preparação que conferisse versões dos assets, registro de catálogos e fallback inicial antes da montagem do pacote publicado.

## Alterações
- `public/app.js`: carregamento tolerante a falhas individuais, caminhos estáticos no Pages, validação do catálogo, evita normalização repetida do mesmo snapshot, captura falha de atualização.
- `public/index.html`: fallback NF-e igual ao catálogo já publicado no pacote; URLs de assets V2.3.24.
- `public/pdf-export.js`: apenas identificação da versão 2.3.24. Algoritmo e estilos de impressão inalterados.
- `public/EXPLORADOR_OFFLINE_COMPLETO.html`: reconstruído a partir dos mesmos módulos e catálogos.
- `scripts/prepare_release.py`: verifica versão, arquivos, catálogo inicial; gera registro de disponibilidade e HTML offline com os scripts existentes.
- `.github/workflows/publicar_paginas.yml`: executa a preparação antes de montar o site, mantém `/public/` e publicação manual.
- `.github/workflows/validar.yml`: executa preparação e testes de release, sintaxe do PDF e teste de seleção de ramificações.
- `tests/test_release_v2324.py`, `tests/test_browser_release_v2324.py`: verificações de empacotamento e de navegação com respostas de rede controladas.
- `docs/v2324/nfe-W22.pdf`: evidência real de regressão; `VERSION`, `README.md`, `CHANGELOG.md`, relatório e manifesto atualizados.

## Testes efetivamente executados
- 33 testes Python aprovados: importação, publicação, DC-e, multidocumento, implantação e release.
- 4 suítes JavaScript aprovadas e verificação de sintaxe dos módulos.
- Chromium: HTML/CSS/JS reais do pacote, respostas de fetch injetadas com JSON reais, inclusive um recurso auxiliar JSON propositalmente inválido. Carregamento inicial NF-e com 1.173 registros, navegação pelos 13 outros catálogos/variantes (ABI 269, BP-e 293, BP-e TA 246, BP-e TM 228, CT-e 978, CT-e OS 314, DC-e 111, GTVe 162, MDF-e 325, NF3-e 507, NFAG 350, NFCom 410, NFGAS 464), retorno à NF-e com filtro W e seleção preservados. Zero exceções JS não tratadas nesse cenário.
- PDF real dos 22 registros do Grupo W: uma página A4 retrato, sem rotação, texto extraível, todos os IDs e versão 2.3.24 presentes. Página renderizada e conferida visualmente.
- Comparação dos catálogos originais: nenhum JSON em public/data ou data modificado; nenhum arquivo excluído. A hierarquia e os 277 avisos de vínculos pendentes não foram alterados.

## Limitações
Não foi possível navegar via HTTP local no Chromium (ERR_BLOCKED_BY_ADMINISTRATOR). A integração foi testada com respostas injetadas, não com tráfego HTTP real. Não houve execução remota de Actions, publicação efetiva, nova auditoria fiscal de XSD, teste de impressão física ou reprodução do erro específico do usuário. A suíte histórica completa não foi executada. O erro reportado pode ter outra causa. Em caso de persistência, encaminhar a mensagem exata, captura da tela ou log do passo que falhou.

## Instalação
Extraia o ZIP incremental na raiz local do repositório, mantendo os caminhos completos, especialmente `.github/workflows/`. Não envie a pasta workflows para dentro de outra pasta workflows. Alternativamente, use o ZIP completo preservando a estrutura e os dados existentes. Faça commit dos arquivos. Se Pages estiver configurado para GitHub Actions, execute “Publicar Explorador no GitHub Pages” após a validação; se estiver configurado para publicar da branch main, aguarde o deploy da branch. Não é necessário alterar a modalidade de publicação ou importar os catálogos novamente. Confira a versão 2.3.24 no cabeçalho e no PDF após Ctrl+F5. Se uma execução falhar, abra Actions > execução > job > passo com erro e encaminhe a mensagem completa.
