from pathlib import Path
import json,re
R=Path(__file__).resolve().parents[1]

def test_import_workflow_is_at_repository_root():
    p=R/'.github/workflows/importar_documentos.yml'
    assert p.is_file()
    assert p.read_bytes()==(R/'COPIAR_PARA_WORKFLOW_GITHUB.txt').read_bytes()
    s=p.read_text()
    assert 'workflow_dispatch:' in s and 'contents: write' in s
    assert 'scripts/import_documents.py' in s
    assert 'git push' in s and 'cobertura-documentos' in s
    assert (R/'.github/workflows/importar_dce.yml').is_file()

def test_pages_package_uses_public_url():
    s=(R/'.github/workflows/publicar_paginas.yml').read_text()
    assert 'cp -a public _site/public' in s
    assert 'cp index.html .nojekyll _site/' in s
    assert './public/' in (R/'index.html').read_text()

def test_offline_embeds_published_nfe_and_available_documents():
    h=(R/'public/EXPLORADOR_OFFLINE_COMPLETO.html').read_text()
    n=json.loads(re.search(r'<script id="seedData" type="application/json">(.*?)</script>',h,re.S)[1])
    assert n==json.loads((R/'public/data/catalogo_atual.json').read_text())
    docs=json.loads(re.search(r'<script id="offlineDocuments" type="application/json">(.*?)</script>',h,re.S)[1])
    for path in (R/'public/data').glob('*/catalogo_atual.json'):
        assert docs[path.parent.name]==json.loads(path.read_text())
    assert 'pendingDiagnostic' in h
