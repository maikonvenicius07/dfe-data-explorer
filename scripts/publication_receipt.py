"""Build a receipt for the actual Pages artifact, then verify public bytes after deploy.
No source collection, mutation of catalogs, or GitHub credentials required.
"""
import argparse
import hashlib
import json
import re
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin, urlsplit, urlencode
from urllib.request import Request, urlopen

DOCS = 'nfe dce cte cteos gtve abi nfgas nfag nf3e nfcom bpe bpetm bpeta mdfe'.split()
ASSETS = ('index.html','app.js','documents.js','selection.js','diagram-state.js','pdf-export.js','styles.css','EXPLORADOR_OFFLINE_COMPLETO.html','data/monitoramento.json','data/catalogo_atual.json')
RECEIPT = 'publicacao.json'

def digest(data):
    return hashlib.sha256(data).hexdigest()

def make(public, version, commit):
    public = Path(public)
    if not re.fullmatch(r'[0-9a-f]{40}', commit):
        raise ValueError('Commit inválido')
    short = version.split('-')[0]
    if f'data-app-version="{short}"' not in (public/'index.html').read_text(encoding='utf8'):
        raise ValueError('Versão do HTML diverge do pacote')
    monitor = json.loads((public/'data/monitoramento.json').read_bytes())
    if monitor.get('schemaVersion') != 1 or set(monitor.get('documents',{})) != set(DOCS):
        raise ValueError('Monitoramento não contém os 14 catálogos esperados')
    paths = list(ASSETS)
    docs = {}
    for doc in DOCS:
        rel = 'data/catalogo_atual.json' if doc == 'nfe' else f'data/{doc}/catalogo_atual.json'
        if rel not in paths: paths.append(rel)
        raw = (public/rel).read_bytes()
        cat = json.loads(raw); meta = cat.get('metadata',{})
        if not cat.get('nodes') or meta.get('documentId') not in ((None,'nfe') if doc=='nfe' else (doc,)):
            raise ValueError(f'Catálogo incompatível: {doc}')
        if monitor['documents'][doc].get('rows') != len(cat['nodes']):
            raise ValueError(f'Contagem do monitor diverge do catálogo: {doc}')
        docs[doc] = {'rows':len(cat['nodes']), 'path':rel}
    return {'schemaVersion':1,'version':version,'commit':commit,
            'preparedAt':datetime.now(timezone.utc).isoformat(), 'checkedAt':monitor.get('checkedAt'),
            'documents':docs, 'files':{p:digest((public/p).read_bytes()) for p in paths}}

def fetch(url):
    request = Request(url,headers={'Cache-Control':'no-cache','User-Agent':'DFE-Data-Explorer-publication-check/1.0','Accept-Encoding':'identity'})
    with urlopen(request,timeout=25) as response:
        return response.read()

def verify_once(base, receipt, fetcher=fetch, nonce=None):
    if urlsplit(base).scheme != 'https': raise ValueError('URL de publicação deve ser HTTPS')
    base = base.rstrip('/')+'/'
    nonce = str(nonce if nonce is not None else time.time_ns())
    def get(path): return fetcher(urljoin(base,path)+'?'+urlencode({'verification':nonce}))
    current = json.loads(get(RECEIPT))
    if current != receipt: raise ValueError('Comprovante público não corresponde ao artefato esperado (versão, commit ou conteúdo)')
    for path, sha in receipt['files'].items():
        if digest(get(path)) != sha: raise ValueError(f'Arquivo público diverge do artefato: {path}')
    return len(receipt['files'])

def main():
    p=argparse.ArgumentParser(); sub=p.add_subparsers(dest='action',required=True)
    b=sub.add_parser('build'); b.add_argument('--public',type=Path,required=True); b.add_argument('--version-file',type=Path,required=True); b.add_argument('--commit',required=True)
    v=sub.add_parser('verify'); v.add_argument('--base',required=True); v.add_argument('--receipt',type=Path,required=True); v.add_argument('--attempts',type=int,default=8); v.add_argument('--delay',type=int,default=15)
    args=p.parse_args()
    if args.action=='build':
        receipt=make(args.public,args.version_file.read_text().strip(),args.commit)
        (args.public/RECEIPT).write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
        print('Comprovante preparado:',receipt['version'],receipt['commit'],len(receipt['files']),'arquivos');return
    receipt=json.loads(args.receipt.read_bytes())
    for attempt in range(1,args.attempts+1):
        try:
            count=verify_once(args.base,receipt)
            print(f'Publicação confirmada: {receipt["version"]} / {receipt["commit"]} / {count} arquivos');return
        except Exception as exc:
            print(f'Tentativa {attempt}/{args.attempts}: {exc}',flush=True)
            if attempt<args.attempts:time.sleep(args.delay)
    raise SystemExit('Publicação NÃO confirmada: verifique o URL, a propagação e os arquivos publicados.')

if __name__=='__main__': main()
