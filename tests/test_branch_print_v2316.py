"""True branch rails and selected-only rows; vector PDFs in both engines."""
from pathlib import Path
from playwright.sync_api import sync_playwright
import fitz, re, os, shutil, tempfile
ROOT=Path(__file__).resolve().parents[1]
# IDs visually transcribed from the two-page user PDF (no extra children).
REFERENCE='W01 W01a W02 W17 W18 W19 W20 W21 W22 W22a W22b W22c W22d W22e W22f W22g W23 W24 W25 W26 W27 W28 W29 W30 W31 W34 W35 W36 W37 W42 W43 W44 W46 W47 W48 W49 W50 W57 W59e W59h W60'.split()
BOTH='W36 W37 W38 W39 W41 W42 W43 W44 W46 W47 W48 W49'.split()
def run(out):
    out.mkdir(parents=True,exist_ok=True)
    with sync_playwright() as p:
        b=p.chromium.launch(executable_path=shutil.which('chromium'),args=['--no-sandbox'])
        page=b.new_page(accept_downloads=True,viewport={'width':1600,'height':1000});page.set_default_timeout(20000)
        errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
        html=(ROOT/'public/EXPLORADOR_OFFLINE_COMPLETO.html').read_text();catalog=(ROOT/'public/data/catalogo_atual.json').read_text()
        html=re.sub(r'(<script id="seedData" type="application/json">).*?(</script>)',lambda m:m[1]+catalog+m[2],html,count=1,flags=re.S)
        page.set_content(html,wait_until='load')
        def choose(keys):
            page.locator('[data-view="moc"]').click();page.locator('#groupMoc').select_option('W');page.locator('#expandMoc').click()
            clear=page.locator('#view-moc [data-select-command=clear]')
            if clear.is_enabled():clear.click()
            # Exercise real selection, not data injection into print scope.
            for k in keys:page.locator(f'[data-moc-print="{k}"]').check()
            page.locator('#mocPrintSelected').click()
            def get(root):return page.locator(root+' tr[data-key]').evaluate_all('es=>es.map(e=>({key:e.dataset.key,depth:Number(e.dataset.depth),rails:e.dataset.rails,tail:e.dataset.tail,child:e.dataset.child,parent:e.querySelector("[data-moc-col=\\\"5\\\"]").textContent,path:e.dataset.path,context:e.querySelector(".print-field-context")?.textContent||""}))')
            a=get('#printDocument');assert a==get('#printPreviewRender');assert set(x['key'] for x in a)==set(keys);return {x['key']:x for x in a}
        def pdf(name,paper='A4',orient='landscape',direct=True):
            page.locator('#pageSize').select_option(paper);page.locator('#pageOrient').select_option(orient);path=out/(name+'.pdf')
            if direct:
                with page.expect_download() as dl:page.locator('#btnDownloadPdf').click()
                dl.value.save_as(path)
            else:page.pdf(path=str(path),print_background=True,prefer_css_page_size=True)
            with fitz.open(path) as d:
                for pg in d:
                    assert pg.get_text().strip() and pg.rotation==0
                    assert (pg.rect.width>pg.rect.height)==(orient=='landscape')
                    assert all(w[0]>=0 and w[2]<=pg.rect.width+1 and w[1]>=0 and w[3]<=pg.rect.height+1 for w in pg.get_text('words'))
                    assert 'Grupo W' in pg.get_text() and 'Campo' in pg.get_text()
                assert len(d[0].get_drawings())>0
                if len(d)>1:assert all('continuação' in x.get_text() for x in list(d)[1:])
                print(name,len(d),'páginas',flush=True)
            return path
        a=choose(BOTH)
        assert a['W37']['depth']==a['W42']['depth']==3 and a['W37']['tail']=='true'
        assert a['W38']['rails']=='3' and a['W38']['tail']=='true' and a['W41']['tail']=='false'
        assert a['W42']['tail']=='true' and a['W43']['rails']=='3' and a['W46']['tail']=='false'
        assert all(a[k]['parent']=='W36' and a[k]['depth']==3 and a[k]['rails']=='' for k in ['W47','W48','W49'])
        assert a['W49']['tail']=='false' and a['W36']['child']=='true'
        pdf('IBS_A4_direto');pdf('IBS_A4_navegador',direct=False);pdf('IBS_A3_direto','A3');pdf('IBS_A3_navegador','A3',direct=False);pdf('IBS_A3_retrato','A3','portrait')
        a=choose(['W43']);assert a['W43']['depth']==4 and 'W42 gIBSMun' in a['W43']['context'] and 'não selecionado' in a['W43']['context'];pdf('W43_isolado')
        a=choose(['W37','W42']);assert a['W37']['tail']=='true' and a['W42']['tail']=='false' and a['W37']['depth']==a['W42']['depth'];pdf('W37_W42_irmaos')
        a=choose(REFERENCE);assert a['W37']['child']=='false' and a['W42']['child']=='true' and a['W47']['parent']=='W36';assert 'W38' not in a
        pdf('Referencia_A4_retrato_direto','A4','portrait');pdf('Referencia_A4_retrato_navegador','A4','portrait',False);pdf('Referencia_A4_paisagem_direto');pdf('Referencia_A4_paisagem_navegador',direct=False)
        assert not errors,errors;b.close()
if __name__=='__main__':
    with tempfile.TemporaryDirectory() as tmp:run(Path(os.environ.get('DFE_QA_DIR',tmp)))
