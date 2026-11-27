# DF-e Data Explorer — V2.3.28-beta.1

## Escopo
Base: V2.3.27 (285 arquivos). Monitor independente das publicações e dos pacotes XSD, integrado ao agendamento existente (11:17 UTC / 07:17 Rondônia). Não altera a hierarquia, a seleção, os catálogos MOC ou a geração de PDF. A atualização dos leiautes continua a cargo do monitor anterior.

## Fontes e cobertura
São dez famílias para 14 catálogos/variantes. A fonte primária de cada família é o portal oficial SVRS, seção Documentos. Endereços configurados em `scripts/monitor_xsd.py`:

| Família | Fonte primária | Catálogos relacionados |
|---|---|---|
| NF-e | https://dfe-portal.svrs.rs.gov.br/NFe/Documentos | nfe (NF-e/NFC-e) |
| DC-e | https://dfe-portal.svrs.rs.gov.br/DCE/Documentos | dce |
| CT-e | https://dfe-portal.svrs.rs.gov.br/CTe/Documentos | cte, cteos, gtve |
| NF-e ABI | https://dfe-portal.svrs.rs.gov.br/Nfabi/Documentos | abi |
| NFGAS | https://dfe-portal.svrs.rs.gov.br/Nfgas/Documentos | nfgas |
| NFAG | https://dfe-portal.svrs.rs.gov.br/Nfag/Documentos | nfag |
| NF3-e | https://dfe-portal.svrs.rs.gov.br/Nf3e/Documentos | nf3e |
| NFCom | https://dfe-portal.svrs.rs.gov.br/Nfcom/Documentos | nfcom |
| BP-e | https://dfe-portal.svrs.rs.gov.br/Bpe/Documentos | bpe, bpetm, bpeta |
| MDF-e | https://dfe-portal.svrs.rs.gov.br/Mdfe/Documentos | mdfe |

Índices nacionais complementares: Portal NF-e (NF-e, ABI, NFGAS, NFAG, NF3-e e NFCom, códigos de conteúdo específicos no script) e Portal CT-e (lista conjunta CT-e/BP-e/MDF-e, com filtro por família). Fontes consultadas por pesquisa web em 27/11/2026. A tentativa de baixar diretamente a página NF3-e da SVRS via curl falhou por DNS (erro 6). A primeira coleta real do HTML e ZIPs no GitHub Actions ainda não foi validada. Não foram incluídos pacotes fictícios ou resultados simulados na base entregue. A associação por família não certifica que todas as variantes estão presentes em cada ZIP.

## Implementação
- `scripts/monitor_xsd.py`: identifica publicações técnicas pelos títulos, reconhece links HTTPS diretos de ZIP ou de arquivo do portal nacional, sem executar JavaScript do portal ou contornar CAPTCHA. Limite de 4 downloads por família por rodada (dois primeiros links reconhecidos e dois outros por data da última leitura). Não é uma auditoria de todos os arquivos históricos a cada dia, nem uma garantia de que a ordem da página corresponde à vigência em produção. Títulos sem link acessível são registrados como evidência de publicação, não como pacote validado. Fontes auxiliares que falham ficam sinalizadas.
- Analisa os arquivos `.xsd` em ZIP, com limites de tamanho (16 MiB download, 64 MiB XSD descompactado, 400 arquivos e 100 mil nós), bloqueio de DTD, entidades externas, rede XML e caminhos inseguros. Calcula hash da estrutura, preserva pacote original de cada snapshot estrutural e manifesto comprimido em `data/xsd_monitor/<familia>/`. A comparação é por arquivo e caminho da declaração, não por XPath expandido de uma instância. Inclui elementos, atributos, tipos, cardinalidades, facets, namespaces e ordem; não compila todos os schemas nem resolve completamente includes/imports. Arquivos e mudanças de nome podem aparecer como inclusão/exclusão. Não é validação de conformidade fiscal.
- Primeiro sucesso estabelece a referência, sem notificar publicações antigas como novas. Novas publicações são registradas; alteração no mesmo URL gera diferença, novo URL com conjunto idêntico de nomes de arquivo pode gerar comparação candidata explicitamente não confirmada como sucessora. Ausência de arquivos ou redução superior a 20% das declarações no mesmo URL bloqueia a substituição da referência. Erros de coleta preservam dados anteriores. Não apaga snapshots. A Central mostra até 100 diferenças por evento; a comparação integral permanece em JSON no repositório. Os arquivos ZIP e snapshots permanecem no repositório, não no site estático. Crescimento do histórico precisa ser acompanhado.
- `public/data/xsd_monitoramento.json`: estado inicial dos dez grupos; nenhuma data de coleta inventada. `public/app.js` e `public/index.html`: painel de monitoramento, situação, fonte, histórico, detalhes comparativos, contador de eventos. Não há envio de e-mail XSD nesta etapa. A leitura offline é um snapshot, não monitoramento ativo.
- `.github/workflows/importar_documentos.yml`: na execução geral `all` e no agendamento diário, roda XSD após MOC e antes do commit/publicação. Uma falha ou cobertura parcial XSD gera aviso, não bloqueia publicação MOC. O estado XSD entra no artefato de cobertura. A execução específica de um documento continua só MOC; a coleta XSD específica pode ser executada via `python scripts/monitor_xsd.py --family nf3e` (ou outra chave). O workflow continua solicitando publicação explicitamente.
- `scripts/build_offline.py`: incorpora o estado XSD no HTML offline. `scripts/publication_receipt.py`: inclui o JSON de XSD na conferência pós-publicação (24 arquivos, antes 23). `COPIAR_PARA_WORKFLOW_GITHUB.txt`: sincronizado com o workflow real. `.github/workflows/validar.yml`: executa testes XSD.
- `public/pdf-export.js`: somente identificação da versão. `VERSION`, README, CHANGELOG e referências de assets atualizadas.

## Testes realizados
- 63 testes Python aprovados (49 anteriores + 14 novos casos parametrizados): importação, monitor MOC, publicação, proteção do estado XSD, fontes autorizadas, detecção de cardinalidade/tamanho/novos campos, exclusão, mudança cosmética de prefixo e comentário, arquivos inseguros, nova publicação, comparação candidata, redução suspeita, indisponibilidade e preservação dos dados MOC. Os testes XSD utilizaram HTML e ZIP controlados, não fontes reais baixadas.
- Quatro suítes JavaScript aprovadas. Sintaxe de app.js conferida por Node.
- `tests/test_browser_xsd_v2328.py`: Chromium com respostas injetadas e os 14 catálogos reais do ZIP. Conferiu as dez famílias iniciais aguardando coleta, navegação recolhida, seleção progressiva, filtros, recolher sem desmarcar, retorno à NF-e, erro auxiliar isolado e HTML offline. PDF real da NF-e com os 22 registros selecionados, em uma página A4 retrato, rotação zero, todos os IDs e versão V2.3.28 presentes no texto. Nenhum erro JavaScript no cenário. O teste de navegador foi executado antes de uma alteração final somente no texto de alerta XSD de redução suspeita; após ela, a sintaxe e os 63 testes Python foram novamente conferidos.
- Não executados: coleta real dos pacotes, acesso HTTPS real, execução remota dos workflows, impressão física, auditoria cruzada integral MOC/XSD e suíte histórica completa de navegador.

## Preservação e instalação
Nenhum arquivo anterior excluído. Os catálogos MOC e históricos da base V2.3.27 permanecem byte a byte iguais. O ZIP incremental contém apenas arquivos novos/alterados, incluindo exclusivamente o novo JSON inicial de monitoramento XSD dentro dos diretórios de dados; NÃO contém os catálogos e históricos MOC. Utilizar o incremental no repositório atual, pois o ZIP completo é backup da base local e pode ter dados anteriores aos do GitHub. Não reinstalar o JSON inicial XSD depois de iniciar as coletas. O workflow de publicação reconstrói o HTML a partir dos dados atuais. O arquivo de SHA-256 é referente ao pacote entregue, não ao estado dinâmico do GitHub.

1. Atualizar os arquivos na raiz do repositório, preservando `.github/workflows/` (sem duplicar a pasta).
2. Conferir Settings > Pages > Source > GitHub Actions.
3. Actions > Importar leiautes de todos os DF-e > Run workflow > main > all. Se já estiver executando, consultar a execução em andamento. A rotina também está agendada às 07:17.
4. Conferir o passo Verificar pacotes XSD e o artefato cobertura-documentos. Após publicação, Ctrl+F5 e abrir Atualizações e histórico > Monitoramento dos pacotes XSD oficiais. Conferir data e quantidade de pacotes efetivamente lidos; situação parcial não significa atualização integral. Se nenhum pacote for lido, enviar os logs para ajuste específico dos links reais ou disponibilizar os ZIPs oficiais.

## Próxima etapa
Confirmar a primeira execução real e ajustar os conectores das fontes com downloads não reconhecidos. Só após obter XSD reais, avançar para a correção dos vínculos hierárquicos pendentes e validação MOC/XSD. O monitor não modifica automaticamente tabelas Oracle ou regras de produção.
