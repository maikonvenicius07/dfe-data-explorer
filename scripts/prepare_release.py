"""Sincroniza a base inicial NF-e e os artefatos do site; sem rede."""
from pathlib import Path
import json,re,subprocess,sys
R=Path(__file__).resolve().parents[1];P=R/'public'
version=(R/'VERSION').read_text().strip().split('-')[0]
html=(P/'index.html').read_text(encoding='utf8')
assert f'data-app-version="{version}"' in html, 'Versão HTML incompatível'
for name in ('documents.js','selection.js','diagram-state.js','pdf-export.js','app.js','styles.css'):
    assert (P/name).is_file() and f'./{name}?v={version}' in html, 'Asset incompatível: '+name
assert f"version:'{version}'" in (P/'pdf-export.js').read_text(encoding='utf8'), 'Versão PDF incompatível'
cat=json.loads((P/'data/catalogo_atual.json').read_text(encoding='utf8'))
assert cat.get('nodes') and cat.get('metadata',{}).get('documentId') in (None,'nfe'), 'Catálogo NF-e inválido'
blob=json.dumps(cat,ensure_ascii=False).replace('<','\\u003c')
html,n=re.subn(r'(<script id="seedData" type="application/json">).*?(</script>)',lambda m:m[1]+blob+m[2],html,count=1,flags=re.S)
assert n==1, 'Seed NF-e ausente'
(P/'index.html').write_text(html,encoding='utf8')
for script in ('build_document_registry.py','build_offline.py'):
    subprocess.run([sys.executable,str(R/'scripts'/script)],check=True)
print('Publicação preparada:',version,len(cat['nodes']),'registros NF-e')
