"""Browser checks with actual published assets and injected network responses.
The environment blocks browser navigation to local HTTP, so no live HTTP is claimed.
"""
from pathlib import Path
import re,json,shutil
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1]/'public'
def run():
    with sync_playwright() as pw:
        b=pw.chromium.launch(executable_path=shutil.which('chromium'),args=['--no-sandbox'])
        p=b.new_page(viewport={'width':1500,'height':900},accept_downloads=True);p.set_default_timeout(15000)
        errors=[];p.on('pageerror',lambda e:errors.append(str(e)))
        h=(R/'index.html').read_text();h=re.sub(r'<link rel="stylesheet" href="\./styles\.css(?:\?[^"]*)?">',lambda _: '<style>'+(R/'styles.css').read_text()+'</style>',h)
        for name in ('documents.js','selection.js','diagram-state.js','pdf-export.js','app.js'):
            h=re.sub(r'<script src="\./'+re.escape(name)+r'(?:\?[^"]*)?"></script>',lambda _: '<script>'+(R/name).read_text().replace('</script','<\\/script')+'</script>',h)
        assets={str(f.relative_to(R)):json.loads(f.read_text()) for f in (R/'data').rglob('*.json')}
        monitor=assets['data/monitoramento.json'];monitor['checkedAt']='2026-11-27T11:17:00Z';d=monitor['documents']['nf3e'];d.update(status='atualizado',lastCheckAt=monitor['checkedAt'],lastSuccessAt=monitor['checkedAt']);d['events']=[{'id':'fixture-1','date':monitor['checkedAt'],'technicalNote':'NT TESTE','changes':[{'id':'x','field':'vTeste','status':'alterado','changes':{'length':{'before':'10','after':'20'}}}]}];d=monitor['documents']['nfcom'];d.update(status='falha-preservado',error='DNS simulado',lastCheckAt=monitor['checkedAt']);payload=json.dumps(assets).replace('<','\\u003c')
        h=h.replace('</head>','<script>const qaAssets='+payload+';window.fetch=async u=>{const k=String(u).replace(/^\\.\\//,"");if(k==="data/status.json")return new Response("{bad",{headers:{"Content-Type":"application/json"}});return qaAssets[k]?new Response(JSON.stringify(qaAssets[k]),{headers:{"Content-Type":"application/json"}}):new Response("not found",{status:404})};</script></head>')
        p.set_content(h,wait_until='load');p.wait_for_function('document.querySelector("#mocCount").textContent.includes("1173")')
        p.locator('[data-view=atualizacoes]').click();p.wait_for_function('document.querySelectorAll("#monitorRows tr").length===14');assert p.locator('#monitorUnread').is_visible();p.locator('#monitorDoc').select_option('nf3e');assert 'vTeste' in p.locator('#monitorDetail').inner_text();assert '10' in p.locator('#monitorDetail').inner_text() and '20' in p.locator('#monitorDetail').inner_text();p.locator('#monitorDoc').select_option('nfcom');assert 'DNS simulado' in p.locator('#monitorDetail').inner_text();print('Central: 14 documentos, comparação anterior/atual e falha isolada OK',flush=True);p.locator('[data-document=nfe]').click();p.locator('#groupMoc').select_option('W');p.locator('#collapseMoc').click();p.locator('[data-moc-toggle="W01"]').click();assert p.locator('[data-moc-print="W01"]').is_checked()
        fam={'cteos':'cte','gtve':'cte','bpetm':'bpe','bpeta':'bpe'}
        for f in sorted(R.glob('data/*/catalogo_atual.json')):
            d=f.parent.name;n=len(json.loads(f.read_text())['nodes']);g=fam.get(d,d);p.locator(f'[data-document="{g}"]').click()
            if d!=g:p.locator('#documentVariant').select_option(d)
            p.wait_for_function('n=>document.querySelector("#view-moc").classList.contains("active")&&document.querySelector("#mocCount").textContent.includes("de "+n+" registros")',arg=n)
            print(d,n,'OK',flush=True)
        p.locator('[data-document="nfe"]').click();assert p.locator('#groupMoc').input_value()=='W';assert p.locator('[data-moc-print="W01"]').is_checked();assert not errors,errors
        p.locator('#view-moc [data-select-command=clear]').click();p.locator('#expandMoc').click()
        keys='W01 W01a W02 W17 W23 W31 W34 W35 W36 W37 W42 W43 W44 W46 W47 W48 W49 W50 W57 W59e W59h W60'.split()
        for k in keys:p.locator(f'[data-moc-print="{k}"]').check()
        p.locator('#mocPrintSelected').click();p.locator('#pageOrient').select_option('portrait')
        assert p.locator('#printDocument [data-integrated-section="moc"] tr[data-key]').count()==22
        with p.expect_download() as dl:p.locator('#btnDownloadPdf').click()
        import fitz,tempfile,os
        qa=Path(os.environ.get('DFE_QA_DIR',tempfile.mkdtemp()));qa.mkdir(parents=True,exist_ok=True);out=qa/'nfe-W22.pdf';dl.value.save_as(out)
        with fitz.open(out) as pdf:
            assert len(pdf)==1 and pdf[0].rect.height>pdf[0].rect.width and pdf[0].rotation==0
            content=pdf[0].get_text();assert 'V2.3.25' in content and all(k in content for k in keys)
            pdf[0].get_pixmap().save(qa/'nfe-W22.png')
        print('NF-e: seleção e filtro preservados; PDF V2.3.25; JSON auxiliar inválido não bloqueia; erros JS: 0.',flush=True);b.close()
if __name__=='__main__':run()
