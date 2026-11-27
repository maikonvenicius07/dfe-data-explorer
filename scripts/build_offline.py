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
# The offline artifact has no server request: embed the last published NF-e catalog.
current=PUBLIC/'data/catalogo_atual.json'
if current.exists():
    cat=json.loads(current.read_text(encoding='utf8'))
    if not cat.get('nodes') or cat.get('metadata',{}).get('documentId') not in (None,'nfe'):
        raise ValueError('Catálogo NF-e inválido para o HTML offline')
    seed=json.dumps(cat,ensure_ascii=False).replace('<','\\u003c')
    html,n=re.subn(r'(<script id="seedData" type="application/json">).*?(</script>)',lambda m:m[1]+seed+m[2],html,count=1,flags=re.S)
    if n!=1:raise ValueError('Seed NF-e ausente')
catalogs={}
for f in (PUBLIC/'data').glob('*/catalogo_atual.json'):
    cat=json.loads(f.read_text(encoding='utf8'));catalogs[f.parent.name]=cat
blob=json.dumps(catalogs,ensure_ascii=False).replace('<','\\u003c')
html=html.replace('</head>','<script id="offlineDocuments" type="application/json">'+blob+'</script></head>',1)
(PUBLIC/'EXPLORADOR_OFFLINE_COMPLETO.html').write_text(html,encoding='utf8')
print('HTML offline gerado:',len(html),'caracteres')
