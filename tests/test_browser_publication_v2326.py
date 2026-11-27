"""Chromium DOM/PDF tests with injected network responses and SHA-256 bridge. Native WebCrypto is not tested in this sandbox."""
from pathlib import Path
import json, hashlib, re, shutil, sys
from urllib.parse import urlsplit
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1]; P=R/'public'
sys.path.insert(0,str(R/'scripts'))
from publication_receipt import make

def run():
    receipt=make(P,(R/'VERSION').read_text().strip(),'a'*40)
    with sync_playwright() as pw:
        b=pw.chromium.launch(executable_path=shutil.which('chromium'),args=['--no-sandbox']);p=b.new_page(accept_downloads=True,viewport={'width':1500,'height':900});p.set_default_timeout(20000)
        errs=[];p.on('pageerror',lambda e:errs.append(str(e)))
        p.expose_function('qaSha256',lambda values:list(hashlib.sha256(bytes(values)).digest()))
        h=(P/'index.html').read_text();h=re.sub(r'<link rel="stylesheet" href="\./styles\.css(?:\?[^"]*)?">',lambda _: '<style>'+(P/'styles.css').read_text()+'</style>',h)
        for name in ('documents.js','selection.js','diagram-state.js','pdf-export.js','app.js'):
            h=re.sub(r'<script src="\./'+re.escape(name)+r'(?:\?[^"]*)?"></script>',lambda _: '<script>'+(P/name).read_text().replace('</script','<\\/script')+'</script>',h)
        assets={str(f.relative_to(P)):f.read_text() for f in (P/'data').rglob('*.json')};assets['publicacao.json']=json.dumps(receipt)
        payload=json.dumps(assets).replace('<','\\u003c')
        setup="""<script>window.qaMode='ok';const qaAssets="""+payload+r""";if(!crypto.subtle)Object.defineProperty(crypto,'subtle',{value:{digest:async (algorithm,raw)=>Uint8Array.from(await qaSha256(Array.from(new Uint8Array(raw)))).buffer}});window.fetch=async u=>{const k=String(u).replace(/^\.\//,'');if(k==='publicacao.json'&&qaMode==='missing')return new Response('not found',{status:404});let raw=qaAssets[k];if(k==='publicacao.json'&&qaMode==='old'){const x=JSON.parse(raw);x.version='2.3.25-beta.1';raw=JSON.stringify(x)}if(k==='data/monitoramento.json'&&qaMode==='stale'){const x=JSON.parse(raw);x.checkedAt='2026-11-27T11:17:00Z';raw=JSON.stringify(x)}return raw?new Response(raw,{headers:{'Content-Type':'application/json'}}):new Response('not found',{status:404})};</script>"""
        h=h.replace('</head>',setup+'</head>',1);p.set_content(h,wait_until='load')
        p.locator('[data-view=atualizacoes]').click();p.wait_for_function('document.querySelector("#publicationReceipt").textContent.includes("corresponde ao pacote publicado")');assert p.locator('#monitorRows tr').count()==14
        for mode,phrase in [('stale','diverge do pacote'),('old','versão da página diverge'),('missing','sem comprovante verificável'),('ok','corresponde ao pacote publicado')]:
            p.evaluate('mode=>window.qaMode=mode',mode);p.locator('#monitorReload').click();p.wait_for_function('s=>document.querySelector("#publicationReceipt").textContent.includes(s)',arg=phrase);print('Comprovante:',mode,'OK',flush=True)
        p.locator('[data-document=nfe]').click();p.locator('#groupMoc').select_option('W');p.locator('#collapseMoc').click();p.locator('[data-moc-toggle="W01"]').click();assert p.locator('[data-moc-print="W01"]').is_checked()
        p.locator('#view-moc [data-select-command=clear]').click();p.locator('#expandMoc').click()
        keys='W01 W01a W02 W17 W23 W31 W34 W35 W36 W37 W42 W43 W44 W46 W47 W48 W49 W50 W57 W59e W59h W60'.split()
        for k in keys:p.locator(f'[data-moc-print="{k}"]').check()
        p.locator('#mocPrintSelected').click();p.locator('#pageOrient').select_option('portrait');assert p.locator('#printDocument [data-integrated-section="moc"] tr[data-key]').count()==22
        with p.expect_download() as dl:p.locator('#btnDownloadPdf').click()
        import fitz,tempfile,os
        qa=Path(os.environ.get('DFE_QA_DIR',tempfile.mkdtemp()));qa.mkdir(parents=True,exist_ok=True);out=qa/'nfe-W22.pdf';dl.value.save_as(out)
        with fitz.open(out) as pdf:
            assert len(pdf)==1 and pdf[0].rect.height>pdf[0].rect.width and pdf[0].rotation==0
            text=pdf[0].get_text();assert 'V2.3.26' in text and all(k in text for k in keys)
        assert not errs,errs;print('PDF NF-e: 22 registros em 1 página A4; erros JS: 0.',flush=True);b.close()
if __name__=='__main__':run()
