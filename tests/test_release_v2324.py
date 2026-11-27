from pathlib import Path
import json,re
R=Path(__file__).resolve().parents[1];P=R/'public'
def test_online_seed_matches_real_catalog():
 h=(P/'index.html').read_text();seed=json.loads(re.search(r'<script id="seedData" type="application/json">(.*?)</script>',h,re.S)[1]);assert seed==json.loads((P/'data/catalogo_atual.json').read_text());assert len(seed['nodes'])>196

def test_release_assets_and_registry():
 v=(R/'VERSION').read_text().strip().split('-')[0];h=(P/'index.html').read_text();assert f'data-app-version="{v}"' in h
 for f in ('app.js','documents.js','diagram-state.js','selection.js','pdf-export.js','styles.css'):
  assert f'./{f}?v={v}' in h and (P/f).is_file()
 registry=json.loads(re.search(r'<script id="documentRegistry" type="application/json">(.*?)</script>',h,re.S)[1]);assert len(registry)==13
 for k,r in registry.items():
  c=json.loads((P/'data'/k/'catalogo_atual.json').read_text());assert c['metadata']['documentId']==k and len(c['nodes'])==r['rows']
