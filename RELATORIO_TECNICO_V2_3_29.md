# DF-e DATA EXPLORER — V2.3.29-beta.1

## 1. Base, objetivo e escopo

Base: `dfe-data-explorer-main (1)(2).zip`, commit 64ad042f09e5298d90519149534f172055716dc4, V2.3.28-beta.1, 290 arquivos. Objetivo: corrigir vínculos recuperáveis com as informações dos MOC já importados, mantendo o leiaute e as chaves internas. Não foi feita nova importação, alteração de registros fiscais ou publicação no GitHub. A primeira coleta XSD continua sem comprovação: o JSON de estado contém dez famílias aguardando a primeira verificação e nenhuma referência de pacote; curl para https://dfe-portal.svrs.rs.gov.br/Nf3e/Documentos falhou com código 6 (DNS). A correção é baseada no MOC, não certificada pelo XSD. A NF3-e não possui nível numérico nos 114 registros pendentes; não foram atribuídos pais por suposição.

## 2. Diagnóstico e implementação

`public/app.js` — `harmonizeDocumentRows`:

- A V2.3.28 recuperava GS/SG/Raiz pelo nível da fonte, mas isolava a pilha por seção editorial. O importador fornece `metadata.tables[].scope`, que delimita as seções contínuas do manual, distinguindo variantes e modais. Agora a projeção utiliza esse escopo (fallback para seção quando não disponível). Na NFCom recupera quatro ligações de det para elementos em tabelas distintas: imposto, gProcRef, gRessarc e infAdProd. As seções editoriais são preservadas; o comando + filhos e a árvore utilizam os vínculos globais.
- O caso específico de pgto apresenta Ele.=E e Tipo=G nos próprios dados originais. A descrição indica dados de cada pagamento; o CT-e também registra a divergência da categoria na observação. A regra exige o nome pgto, tipo G em fonte e campo normalizado, categoria E, nível imediatamente anterior, mesma tabela, filho com nome em lista restrita (nPag, idTransacao, tpMeioPgto, CNPJReceb, CNPJBasePSP) e categoria A ou E. Recupera 40 vínculos, sem alterar Ele.=E. Não se generaliza a outros elementos com categoria E.
- Recuperação somente quando o vínculo original está ausente e o aviso é 'Nível aponta para registro não estrutural', sem conflito com pai explicitamente declarado, nem ciclo. Nível ausente, ambíguo ou divergente permanece pendente. Não atribui XPath certificado.
- No mesmo grupo editorial artificial e tabela, filhos recuperados e descendentes compatíveis são apresentados junto ao pai. Seções diferentes permanecem separadas, mesmo quando vinculadas. O inspetor mostra a evidência MOC da recuperação; a mensagem de cobertura diferencia avisos da fonte e pendências na projeção.
- A regra é aplicada a cada carregamento, inclusive após atualização MOC, sem lista de hashes de campos ou modificação dos catálogos; evita alterações em IDs, seleções persistidas, históricos e hashes de conteúdo. O importador continua conservador e o número bruto de avisos permanece no JSON de origem. Os resultados dependem das evidências da fonte futura.

## 3. Contagem dos avisos (projeção de apresentação)

| Documento | Registros | Avisos origem | Recuperados V2.3.28 | Recuperados V2.3.29 | Pendentes V2.3.29 |
|---|---:|---:|---:|---:|---:|
| NF-e/NFC-e | 1173 | 0 | 0 | 0 | 0 |
| DC-e | 111 | 0 | 0 | 0 | 0 |
| CT-e | 978 | 21 | 10 | 20 | 1 |
| CT-e OS | 314 | 5 | 0 | 5 | 0 |
| GTVe | 162 | 0 | 0 | 0 | 0 |
| NF-e ABI | 269 | 1 | 0 | 0 | 1 |
| NFGAS | 464 | 5 | 0 | 0 | 5 |
| NFAG | 350 | 6 | 0 | 5 | 1 |
| NF3-e | 507 | 114 | 0 | 0 | 114 |
| NFCom | 410 | 140 | 24 | 33 | 107 |
| BP-e | 293 | 5 | 0 | 5 | 0 |
| BP-e TM | 228 | 5 | 0 | 5 | 0 |
| BP-e TA | 246 | 6 | 0 | 5 | 1 |
| MDF-e | 325 | 3 | 0 | 0 | 3 |
| **Total** | **5830** | **311** | **34** | **78** | **233** |

44 recuperações adicionais em relação aos 277 avisos projetados anteriormente (-15,88%). Destes 44, 40 correspondem a pgto e quatro à continuidade entre tabelas NFCom. NF3-e (114) e NFCom (107) concentram 221 dos 233 avisos restantes. As contagens não certificam todos os vínculos existentes, regras fiscais ou cardinalidades; representam avisos do importador e a projeção da interface.

## 4. Testes executados

- 63 testes Python aprovados: `test_import.py`, `test_publication_v232.py`, `test_import_documents_v2321.py`, `test_import_dce.py`, `test_deployment_v2322.py`, `test_monitor_documents_v2325.py`, `test_release_v2324.py`, `test_publication_receipt_v2326.py`, `test_monitor_xsd_v2328.py`.
- 5 suítes JavaScript aprovadas: diagrama progressivo, seleção lógica, seleção integrada, toggle de ramificação e novo teste de recuperação. Teste novo utiliza os catálogos entregues e fixtures de escopo, conflito, nível ausente, homônimos, tipo incompatível, agrupamento e regra pgto; verifica preservação das chaves, pais existentes e inexistência de ciclos. Contagens fixas são exigidas apenas para hashes da base conhecida.
- `node --check public/app.js` aprovado. `python scripts/prepare_release.py` reconstruiu registry, seed e HTML offline.
- `tests/test_browser_hierarchy_v2329.py`: Chromium com respostas fetch injetadas e os catálogos reais do ZIP. 14 catálogos, todos inicialmente recolhidos, expansão e seleção, filtros, seleção persistida por documento, painel XSD inicial, seleção de imposto por + filhos de det (NFCom), agrupamento e seleção de nPag por pgto, 114 avisos NF3-e preservados, HTML offline e ausência de erros JS. PDF NF-e Grupo W com 22 registros, uma página A4 retrato, rotação zero e versão 2.3.29 confirmada.
- Não executados: coleta real XSD, validação integral de schemas, GitHub Actions remoto, GitHub Pages remoto, impressão física, suíte histórica completa. Os testes de monitoramento XSD usam dados controlados. O teste de navegador foi executado com dados locais e não representa teste de rede.

## 5. Arquivos da entrega

Alterados: `.github/workflows/validar.yml` (adiciona teste Node); `CHANGELOG.md`; `README.md`; `VERSION`; `public/app.js`; `public/index.html`; `public/pdf-export.js` (identificação da versão); `public/EXPLORADOR_OFFLINE_COMPLETO.html` (regenerado); `ARQUIVOS_SHA256.txt` (manifesto do pacote).

Novos: `tests/test_hierarchy_recovery_v2329.js`; `tests/test_browser_hierarchy_v2329.py`; `RELATORIO_TECNICO_V2_3_29.md`.

Nenhum arquivo removido. Nenhum arquivo em `data/` ou `public/data/` alterado. CSS, demais módulos, fontes fiscais, rotina de monitoramento, agendamento, seleção e motor PDF preservados, exceto a versão do PDF. ZIP completo 293 arquivos; incremental 12, mesmos bytes e caminhos relativos à raiz.

## 6. Atualização e próxima etapa

1. Faça backup do repositório. Prefira o ZIP incremental para preservar dados e históricos que tenham sido produzidos pelo GitHub após a exportação.
2. Sobreponha na raiz do repositório, incluindo `.github/workflows/`. Não aninhe pastas. Use o fluxo de publicação existente; se necessário execute `Publicar GitHub Pages` manualmente, ou a importação geral `Importar leiautes de todos os DF-e` > all para verificar também os XSD. Confirme versão 2.3.29 após Ctrl+F5.
3. Abra NFCom e teste det, imposto e pgto; abra NF3-e e confira o alerta de vínculos pendentes. Confirme grupos recolhidos e impressão seletiva.
4. Acesse Atualizações e histórico > Monitoramento dos pacotes XSD oficiais e confirme pacotes realmente lidos. Se a coleta falhar, inspecione os logs da etapa Verificar pacotes XSD ou disponibilize os ZIPs oficiais. Não substitua o estado de monitoramento por uma referência vazia.

V2.3.30: validação cruzada MOC/XSD, condicionada à disponibilidade de schemas oficiais verificáveis e correspondentes ao documento e versão. Prioridade NF3-e e NFCom; resolver ambiguidades antes de sugerir alterações Oracle. Não tratar uma coleta parcial como validação integral.
