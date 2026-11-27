"""Browser integration with explicitly synthetic fixtures for NEW documents; never writes production catalogs."""
from pathlib import Path
from tempfile import TemporaryDirectory
from threading import Thread
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from functools import partial
import shutil,sys,re,json,os
from playwright.sync_api import sync_playwright
import fitz
from test_import_documents_v2321 import fixture
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'scripts'))
from import_documents import extract,SOURCES

def run():
    with TemporaryDirectory(prefix='dfe-new-docs-fixtures-') as tmp:
        p=Path(tmp);shutil.copytree(R/'public',p/'public');pub=p/'public'
        registry={}
        for doc in SOURCES:
            if doc=='dce':continue
            cat=extract(doc,fixture(doc));cat['metadata']['coverage']='FIXTURE SINTÉTICO — NÃO É DOCUMENTO FISCAL';cat['metadata']['status']='fixture-only'
            f=pub/'data'/doc/'catalogo_atual.json';f.parent.mkdir(parents=True,exist_ok=True);f.write_text(json.dumps(cat));registry[doc]={'rows':len(cat['nodes'])}
        registry['dce']={'rows':111}
        index=pub/'index.html';index.write_text(re.sub(r'(<script id="documentRegistry" type="application/json">).*?(</script>)',lambda m:m[1]+json.dumps(registry)+m[2],index.read_text(),flags=re.S))
        class Quiet(SimpleHTTPRequestHandler):
            def log_message(self,*args):pass
        srv=ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=str(p)));Thread(target=srv.serve_forever,daemon=True).start()
        try:
            with sync_playwright() as pw:
                b=pw.chromium.launch(executable_path=shutil.which('chromium'),args=['--no-sandbox']);page=b.new_page(accept_downloads=True,viewport={'width':1500,'height':900});errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
                # Browser policy blocks navigation even to localhost in this environment.
                # Inject the exact static assets and intercept fetch responses in-memory.
                # This exercises the actual async switchDocument path, not a UI imitation.
                assets={str(f.relative_to(pub)):json.loads(f.read_text()) for f in (pub/'data').rglob('*.json')}
                html=(pub/'index.html').read_text()
                html=re.sub(r'<link rel="stylesheet" href="\./styles\.css(?:\?[^"]*)?">',lambda _: '<style>'+(pub/'styles.css').read_text()+'</style>',html)
                for name in ('documents.js','selection.js','diagram-state.js','pdf-export.js','app.js'):
                    html=re.sub(r'<script src="\./'+re.escape(name)+r'(?:\?[^"]*)?"></script>',lambda _: '<script>'+(pub/name).read_text().replace('</script','<\\/script')+'</script>',html)
                payload=json.dumps(assets).replace('<','\\u003c')
                html=html.replace('</head>', '<script>const fixtureAssets='+payload+';window.fetch=async u=>{const k=String(u).replace(/^\\.\\//,"");return fixtureAssets[k]?new Response(JSON.stringify(fixtureAssets[k]),{headers:{"Content-Type":"application/json"}}):new Response("not found",{status:404})};</script></head>')
                page.set_content(html,wait_until='load');page.wait_for_function("document.querySelector('#mocCount').textContent.includes('1173')")
                def choose(doc):
                    family={'cteos':'cte','gtve':'cte','bpetm':'bpe','bpeta':'bpe'}.get(doc,doc)
                    page.locator(f'[data-document="{family}"]').click()
                    if family!=doc:
                        page.locator('#documentVariant').select_option(doc)
                    page.wait_for_function("document.querySelector('#view-moc').classList.contains('active')")
                    page.wait_for_function("document.querySelector('#activeDocumentTitle').textContent.includes("+json.dumps({'cte':'CT-e / CT-e OS / GTVe'}.get(doc,SOURCES[doc][0]))+")")
                for doc in SOURCES:
                    if doc=='dce':continue
                    choose(doc);cat=json.loads((pub/'data'/doc/'catalogo_atual.json').read_text());tag=cat['nodes'][0]['tag'];key=cat['nodes'][0]['key']
                    assert page.locator('#mocTables [data-moc-print]:checked').count()==0
                    page.locator('#searchMoc').fill(tag)
                    chk=page.locator(f'#mocTables [data-moc-print="{key}"]');chk.check();assert chk.is_checked()
                    page.locator('#mocPrintSelected').click();page.locator('#pageOrient').select_option('landscape')
                    with page.expect_download() as dl:page.locator('#btnDownloadPdf').click()
                    pdf=p/(doc+'.pdf');dl.value.save_as(pdf)
                    with fitz.open(pdf) as f:
                        t='\n'.join(pg.get_text() for pg in f);assert tag in t and 'V2.3.21' in t;assert all(pg.rotation==0 for pg in f)
                    choose(doc);assert page.locator(f'#mocTables [data-moc-print="{key}"]').is_checked()
                    print(doc,'fixture UI + PDF OK',flush=True)
                page.locator('[data-document="nfe"]').click();assert page.locator('#mocTables [data-moc-print]:checked').count()==0
                page.set_viewport_size({'width':390,'height':844});assert page.locator('#view-moc').is_visible()
                assert not errors,errors;b.close()
        finally:srv.shutdown();srv.server_close()
if __name__=='__main__':run()
