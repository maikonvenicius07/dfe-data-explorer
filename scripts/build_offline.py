"""Gera o HTML independente diretamente dos arquivos da mesma versão.
Garante que o HTML offline não fique defasado do JavaScript da implantação.
"""
from pathlib import Path
import re, json
ROOT=Path(__file__).resolve().parents[1];PUBLIC=ROOT/'public'
html=(PUBLIC/'index.html').read_text(encoding='utf8')
html=re.sub(r'<link rel="stylesheet" href="\./styles\.css(?:\?[^"]*)?">',lambda _:  '<style>'+ (PUBLIC/'styles.css').read_text(encoding='utf8')+'</style>',html)
for name in ('documents.js','selection.js','diagram-state.js','pdf-export.js','app.js'):
    html=re.sub(r'<script src="\./'+re.escape(name)+r'(?:\?[^"]*)?"></script>',lambda _:  '<script>'+ (PUBLIC/name).read_text(encoding='utf8').replace('</script','<\\/script')+'</script>',html)
catalogs={}
for f in (PUBLIC/'data').glob('*/catalogo_atual.json'):
    cat=json.loads(f.read_text(encoding='utf8'));catalogs[f.parent.name]=cat
blob=json.dumps(catalogs,ensure_ascii=False).replace('<','\\u003c')
html=html.replace('</head>','<script id="offlineDocuments" type="application/json">'+blob+'</script></head>',1)
(PUBLIC/'EXPLORADOR_OFFLINE_COMPLETO.html').write_text(html,encoding='utf8')
print('HTML offline gerado:',len(html),'caracteres')
