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
        assets={str(f.relative_to(R)):json.loads(f.read_text()) for f in (R/'data').rglob('*.json')};payload=json.dumps(assets).replace('<','\\u003c')
        h=h.replace('</head>','<script>const qaAssets='+payload+';window.fetch=async u=>{const k=String(u).replace(/^\\.\\//,"");if(k==="data/status.json")return new Response("{bad",{headers:{"Content-Type":"application/json"}});return qaAssets[k]?new Response(JSON.stringify(qaAssets[k]),{headers:{"Content-Type":"application/json"}}):new Response("not found",{status:404})};</script></head>')
        p.set_content(h,wait_until='load');p.wait_for_function('document.querySelector("#mocCount").textContent.includes("1173")')
        def closed():
            assert p.locator('#mocTables .moc-group').count()>0
            assert p.locator('#mocTables .moc-group:not(.closed)').count()==0
            assert p.locator('#mocTables .moc-group-body:visible').count()==0
            assert p.locator('#mocTables [data-moc-toggle]').evaluate_all('(els)=>els.every(e=>e.textContent==="▸")')
        def count(): return int(re.search(r'(\d+) selecionados',p.locator('#mocCount').inner_text())[1])
        closed();assert count()==0
        p.locator('[data-view="atualizacoes"]').click();p.wait_for_function('document.querySelectorAll("#xsdMonitorRows tr").length===10');assert 'primeira' in p.locator('#xsdMonitorStatus').inner_text();assert p.locator('#xsdMonitorRows').inner_text().count('Aguardando primeira verificação')==10
        p.locator('[data-document="nfe"]').click();closed();assert count()==0
        p.locator('#groupMoc').select_option('W');assert p.locator('[data-moc-toggle="W01"]').is_visible()
        assert p.locator('[data-moc-print="W02"]').count()==0
        p.locator('[data-moc-toggle="W01"]').click();assert p.locator('[data-moc-print="W01"]').is_checked() and p.locator('[data-moc-print="W02"]').is_checked()
        selected_count=count();assert selected_count>1
        p.locator('#collapseMoc').click();closed();assert count()==selected_count
        p.locator('#searchMoc').fill('W41');assert p.locator('[data-moc-print="W41"]').is_visible() and count()==selected_count
        p.locator('#searchMoc').fill('');p.locator('#expandMoc').click();assert count()==selected_count
        p.locator('#collapseMoc').click();closed();assert count()==selected_count
        fam={'cteos':'cte','gtve':'cte','bpetm':'bpe','bpeta':'bpe'}
        for f in sorted(R.glob('data/*/catalogo_atual.json')):
            d=f.parent.name;n=len(json.loads(f.read_text())['nodes']);g=fam.get(d,d);p.locator(f'[data-document="{g}"]').click()
            if d!=g:p.locator('#documentVariant').select_option(d)
            p.wait_for_function('n=>document.querySelector("#view-moc").classList.contains("active")&&document.querySelector("#mocCount").textContent.includes("de "+n+" registros")',arg=n)
            closed();assert count()==0
            p.locator('#mocTables [data-toggle-moc]').first.click();assert p.locator('#mocTables .moc-group:not(.closed)').count()==1 and count()==0
            p.locator('#collapseMoc').click();closed();print(d,n,'OK',flush=True)
        # NFCom: pai det atravessa tabelas, sem apagar a seção editorial de imposto.
        p.locator('[data-document="nfcom"]').click();closed();assert '107' in p.locator('#sourceNotice').inner_text()
        cat=json.loads((R/'data/nfcom/catalogo_atual.json').read_text())['nodes'];det=next(n for n in cat if n['tag']=='det');imp=next(n for n in cat if n['tag']=='imposto');pg=next(n for n in cat if n['tag']=='pgto');np=next(n for n in cat if n['tag']=='nPag');
        p.locator('#expandMoc').click();p.locator(f'[data-moc-descendants="{det["key"]}"]').click();assert p.locator(f'[data-moc-print="{imp["key"]}"]').is_checked()
        p.locator('#view-moc [data-select-command=clear]').click();p.locator('#collapseMoc').click();p.locator('#groupMoc').select_option(pg['mocGroup']);p.locator('#expandMoc').click();
        assert p.locator(f'[data-moc-print="{np["key"]}"]').is_visible();p.locator(f'[data-moc-descendants="{pg["key"]}"]').click();assert p.locator(f'[data-moc-print="{np["key"]}"]').is_checked()
        p.locator('[data-document="nf3e"]').click();assert '114' in p.locator('#sourceNotice').inner_text();closed()
        p.locator('[data-document="nfe"]').click();assert p.locator('#groupMoc').input_value()=='W';closed();assert count()==selected_count;assert not errors,errors
        p.locator('#view-moc [data-select-command=clear]').click();p.locator('#expandMoc').click()
        keys='W01 W01a W02 W17 W23 W31 W34 W35 W36 W37 W42 W43 W44 W46 W47 W48 W49 W50 W57 W59e W59h W60'.split()
        for k in keys:p.locator(f'[data-moc-print="{k}"]').check()
        p.locator('#collapseMoc').click();closed();assert count()==22
        p.locator('#mocPrintSelected').click();p.locator('#pageOrient').select_option('portrait')
        assert p.locator('#printDocument [data-integrated-section="moc"] tr[data-key]').count()==22
        with p.expect_download() as dl:p.locator('#btnDownloadPdf').click()
        import fitz,tempfile,os
        qa=Path(os.environ.get('DFE_QA_DIR',tempfile.mkdtemp()));qa.mkdir(parents=True,exist_ok=True);out=qa/'nfe-W22.pdf';dl.value.save_as(out)
        with fitz.open(out) as pdf:
            assert len(pdf)==1 and pdf[0].rect.height>pdf[0].rect.width and pdf[0].rotation==0
            content=pdf[0].get_text();assert 'V2.3.29' in content and all(k in content for k in keys)
            pdf[0].get_pixmap().save(qa/'nfe-W22.png')
        p.set_content((R/'EXPLORADOR_OFFLINE_COMPLETO.html').read_text(),wait_until='load');closed();assert count()==0;assert not errors,errors
        print('NF-e: seleção e filtro preservados; PDF V2.3.29; JSON auxiliar inválido não bloqueia; erros JS: 0.',flush=True);b.close()
if __name__=='__main__':run()
