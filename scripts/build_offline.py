"""Gera o HTML independente diretamente dos arquivos da mesma versão.
Garante que o HTML offline não fique defasado do JavaScript da implantação.
"""
from pathlib import Path
import re
ROOT=Path(__file__).resolve().parents[1];PUBLIC=ROOT/'public'
html=(PUBLIC/'index.html').read_text(encoding='utf8')
html=re.sub(r'<link rel="stylesheet" href="\./styles\.css(?:\?[^"]*)?">',lambda _:  '<style>'+ (PUBLIC/'styles.css').read_text(encoding='utf8')+'</style>',html)
for name in ('documents.js','selection.js','diagram-state.js','pdf-export.js','app.js'):
    html=re.sub(r'<script src="\./'+re.escape(name)+r'(?:\?[^"]*)?"></script>',lambda _:  '<script>'+ (PUBLIC/name).read_text(encoding='utf8').replace('</script','<\\/script')+'</script>',html)
(PUBLIC/'EXPLORADOR_OFFLINE_COMPLETO.html').write_text(html,encoding='utf8')
print('HTML offline gerado:',len(html),'caracteres')
