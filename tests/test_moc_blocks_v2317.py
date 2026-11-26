"""MOC branch blocks, optional structural map, real browser and direct PDF."""
from pathlib import Path
import os, shutil, re, tempfile, fitz
from playwright.sync_api import sync_playwright
from test_branch_print_v2316 import REFERENCE, BOTH
ROOT=Path(__file__).resolve().parents[1]
def run(out):
    out.mkdir(parents=True,exist_ok=True)
    with sync_playwright() as p:
        b=p.chromium.launch(executable_path=shutil.which('chromium'),args=['--no-sandbox']);page=b.new_page(accept_downloads=True,viewport={'width':1600,'height':1000});page.set_default_timeout(15000)
        errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
        html=(ROOT/'public/EXPLORADOR_OFFLINE_COMPLETO.html').read_text();catalog=(ROOT/'public/data/catalogo_atual.json').read_text()
        assert '?v=2.3.17' in (ROOT/'public/index.html').read_text() and 'src="./app.js' not in html
        html=re.sub(r'(<script id="seedData" type="application/json">).*?(</script>)',lambda m:m[1]+catalog+m[2],html,count=1,flags=re.S);page.set_content(html,wait_until='load')
        def choose(keys,group='W'):
            page.locator('[data-view="moc"]').click();page.locator('#groupMoc').select_option(group);page.locator('#expandMoc').click();clear=page.locator('#view-moc [data-select-command=clear]');
            if clear.is_enabled():clear.click()
            for k in keys:page.locator(f'[data-moc-print="{k}"]').check()
            page.locator('#mocPrintSelected').click()
            def meta(root):return page.locator(root+' tr[data-key]').evaluate_all('es=>es.map(e=>[e.dataset.key,Number(e.dataset.depth),e.dataset.rails,e.dataset.ends,e.dataset.child,e.querySelector(".print-branch-label")?.textContent||"",e.querySelector("[data-moc-col=\\"5\\"]").textContent])')
            a=meta('#printDocument');assert a==meta('#printPreviewRender');assert {x[0] for x in a}==set(keys);assert all(len(row)==10 for row in page.locator('#printDocument tr[data-key]').evaluate_all('es=>es.map(e=>[...e.cells].map(c=>c.textContent))'))
            return {x[0]:x for x in a}
        def pdf(name,paper='A4',orient='landscape',direct=True):
            page.locator('#pageSize').select_option(paper);page.locator('#pageOrient').select_option(orient);path=out/(name+'.pdf')
            if direct:
                with page.expect_download() as dl:page.locator('#btnDownloadPdf').click()
                assert 'V2_3_17' in dl.value.suggested_filename;dl.value.save_as(path)
            else:page.pdf(path=str(path),print_background=True,prefer_css_page_size=True)
            with fitz.open(path) as d:
                text='\n'.join(pg.get_text() for pg in d);assert 'V2.3.17' in text and 'Campo' in text
                for pg in d:
                    assert pg.get_text().strip() and pg.rotation==0 and (pg.rect.width>pg.rect.height)==(orient=='landscape')
                    assert all(w[0]>=-1 and w[2]<=pg.rect.width+1 and w[1]>=-1 and w[3]<=pg.rect.height+1 for w in pg.get_text('words')),(name,pg.number)
                print(name,len(d),'páginas',flush=True)
            return path
        a=choose(['A02','A03'],'A');pdf('simples_A4');a=choose(['W01','W23','W24','W25','W31','W33']);pdf('intermediario_A4')
        a=choose(BOTH);assert a['W37'][1]==a['W42'][1]==a['W47'][1]==3;assert a['W43'][1]==a['W46'][1]==4 and a['W46'][3]=='4';assert a['W47'][6]=='W36' and a['W47'][2]=='';assert 'NÍVEL 3' in a['W42'][5]
        pdf('complexo_A4');pdf('complexo_A4_browser',direct=False);pdf('complexo_A3','A3');pdf('complexo_A4_retrato','A4','portrait')
        # Optional map uses exactly the same selected keys, with ancestors separately labelled.
        page.locator('#printMap').check();m=page.locator('#printDocument [data-map-key]').evaluate_all('es=>es.map(e=>[e.dataset.mapKey,e.dataset.context])');assert {x[0] for x in m if x[1]=='false'}==set(BOTH);assert {x[0] for x in m if x[1]=='true'}=={'W01','W34'}
        pdf('mapa_A4');pdf('mapa_A4_browser',direct=False);pdf('mapa_A3','A3')
        page.locator('#printMap').uncheck();assert page.locator('#printDocument [data-map-key]').count()==0
        a=choose(['W43']);assert a['W43'][1]==4;pdf('isolado_A4')
        a=choose(REFERENCE);pdf('referencia_A4_retrato','A4','portrait');pdf('referencia_A4_paisagem');page.locator('#printMap').check();pdf('referencia_mapa_A4',direct=False);page.locator('#printMap').uncheck()
        assert not errors,errors;b.close()
if __name__=='__main__':
    with tempfile.TemporaryDirectory() as tmp:run(Path(os.environ.get('DFE_QA_DIR',tmp)))
