# Pendências documentadas — não confundir com funcionalidades implementadas

| Gravidade | Item | Estado |
|---|---|---|
| Crítico para cobertura | Coleta integral do MOC vigente e auditoria de todas as linhas | Pendente: base embutida contém somente 196 registros selecionados |
| Crítico para tipos XSD | Download e importação verificada do pacote XSD oficial | Pendente: 0 schemas verificados nesta base |
| Alto | Monitoramento contínuo, histórico e notificações em hospedagem real | Código preparado, não ativado nem testado remotamente |
| Médio | Exportação XLSX da seleção exata de campos | Não implementada; CSV atende à seleção, XLSX do backend é geral |
| Médio | Sincronização das seleções pessoais entre dispositivos | Não implementada; perfis locais no navegador |
| Médio | Validação integral do leitor de layouts com milhares de registros e todos os schemas | Pendente: teste local com 196 nós e casos selecionados |
| Médio | Testes de regressão de longos diagramas legados | Teste antigo extenso esgotou o limite de execução local nesta revisão; requer reteste |
| Baixo | Versão expandida do modo apresentação com roteiro e telas próprias | Modo em tela cheia implementado; roteiro próprio ainda não existe |

O MOC e o pacote XSD não podem ser substituídos por campos inventados. Verificar diariamente o log de sincronização; falhas não validam exclusões de campos.
