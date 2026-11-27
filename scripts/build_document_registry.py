"""Generate availability from real files, never from hard-coded flags."""
from pathlib import Path
import json,re
ROOT=Path(__file__).resolve().parents[1]; PUBLIC=ROOT/'public'
ids='dce cte cteos gtve abi nfgas nfag nf3e nfcom bpe bpetm bpeta mdfe'.split()
registry={}
for doc in ids:
    p=PUBLIC/'data'/doc/'catalogo_atual.json'
    if not p.exists():continue
    cat=json.loads(p.read_text(encoding='utf8'));meta=cat.get('metadata',{})
    if meta.get('documentId')!=doc or not cat.get('nodes'):raise ValueError('Catálogo incompatível: '+doc)
    registry[doc]={'rows':len(cat['nodes']),'status':meta.get('status'),'sourceHash':meta.get('sourceHash')}
index=PUBLIC/'index.html';html=index.read_text(encoding='utf8')
blob=json.dumps(registry,ensure_ascii=False).replace('<','\\u003c')
tag='<script id="documentRegistry" type="application/json">'+blob+'</script>'
if 'id="documentRegistry"' in html:html=re.sub(r'<script id="documentRegistry" type="application/json">.*?</script>',lambda _:tag,html,flags=re.S)
else:html=html.replace('<script id="dceSeed"',tag+'\n<script id="dceSeed"',1)
# Preserve the previous pilot fallback, but refresh when the source is actually imported.
p=PUBLIC/'data/dce/catalogo_atual.json'
if p.exists():
    blob=json.dumps(json.loads(p.read_text(encoding='utf8')),ensure_ascii=False).replace('<','\\u003c')
    html,n=re.subn(r'(<script id="dceSeed" type="application/json">).*?(</script>)',lambda m:m[1]+blob+m[2],html,flags=re.S)
    if n!=1:raise ValueError('Seed DC-e ausente')
index.write_text(html,encoding='utf8')
print('Catálogos disponíveis:',registry.keys())
