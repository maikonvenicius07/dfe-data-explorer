from pathlib import Path
import sys, json, shutil
from urllib.parse import urlsplit
import pytest
R=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(R/'scripts'))
from publication_receipt import make, verify_once, DOCS, RECEIPT

@pytest.fixture
def package(tmp_path):
    p=tmp_path/'public';shutil.copytree(R/'public',p)
    receipt=make(p,(R/'VERSION').read_text().strip(),'a'*40)
    (p/RECEIPT).write_text(json.dumps(receipt))
    return p,receipt

def server(p,override=None):
    def fetch(url):
        path=urlsplit(url).path.removeprefix('/dfe-data-explorer/public/')
        assert urlsplit(url).query.startswith('verification=')
        return (override or {}).get(path,(p/path).read_bytes())
    return fetch

def test_real_catalogs_and_bytes(package):
    p,r=package
    assert set(r['documents'])==set(DOCS)
    assert sum(d['rows'] for d in r['documents'].values())==sum(len(json.loads((p/d['path']).read_bytes())['nodes']) for d in r['documents'].values())
    assert r['version']==(R/'VERSION').read_text().strip() and len(r['files'])==24
    assert verify_once('https://example.test/dfe-data-explorer/public/',r,server(p))==24

def test_old_commit_and_receipt_rejected(package):
    p,r=package;old={**r,'commit':'b'*40}
    with pytest.raises(ValueError,match='Comprovante público'):
        verify_once('https://example.test/dfe-data-explorer/public',r,server(p,{RECEIPT:json.dumps(old).encode()}))

def test_current_version_with_stale_monitor_rejected(package):
    p,r=package
    with pytest.raises(ValueError,match='monitoramento.json'):
        verify_once('https://example.test/dfe-data-explorer/public',r,server(p,{'data/monitoramento.json':b'{}'}))

def test_catalog_bytes_rejected(package):
    p,r=package
    with pytest.raises(ValueError,match='mdfe/catalogo_atual.json'):
        verify_once('https://example.test/dfe-data-explorer/public',r,server(p,{'data/mdfe/catalogo_atual.json':b'{}'}))

def test_wrong_catalog_count_blocks_deploy(package):
    p,r=package;f=p/'data/monitoramento.json';m=json.loads(f.read_text());m['documents']['nf3e']['rows']-=1;f.write_text(json.dumps(m))
    with pytest.raises(ValueError,match='nf3e'):make(p,r['version'],r['commit'])

def test_wrong_catalog_identity_blocks_deploy(package):
    p,r=package;f=p/'data/mdfe/catalogo_atual.json';m=json.loads(f.read_text());m['metadata']['documentId']='nf3e';f.write_text(json.dumps(m))
    with pytest.raises(ValueError,match='mdfe'):make(p,r['version'],r['commit'])

def test_workflow_validates_deployed_artifact():
    s=(R/'.github/workflows/publicar_paginas.yml').read_text()
    assert s.index('scripts/prepare_release.py\n')<s.index('cp -a public _site/public')<s.index('publication_receipt.py build')<s.index('actions/deploy-pages@v4')<s.index('publication_receipt.py verify')
    assert 'needs.build.outputs.commit' in s and 'comprovante-publicacao' in s
    assert 'publicacao.json' in (R/'public/app.js').read_text()
