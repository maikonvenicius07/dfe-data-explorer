"""Reproduces the 13 selected fields in the user's rotated PDF; tests real downloads."""
from pathlib import Path
from playwright.sync_api import sync_playwright
import fitz, os, shutil, tempfile
ROOT=Path(__file__).resolve().parents[1]
KEYS=['W01','W02','W03','W04','W04a','W15','W16','W16a','W17','W23','W31','W34','W60']
def run():
    with sync_playwright() as p:
        browser=p.chromium.launch(headless=True,executable_path=os.environ.get('CHROMIUM_PATH') or shutil.which('chromium'),args=['--no-sandbox'])
        page=browser.new_page(viewport={'width':1450,'height':900},accept_downloads=True)
        page.set_default_timeout(6000);errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
        page.set_content((ROOT/'public/EXPLORADOR_OFFLINE_COMPLETO.html').read_text(),wait_until='load')
        assert page.locator('#diagramMode').input_value()=='horizontal'
        # Same 13 fields as in the user's PDF, without selecting siblings.
        page.locator('[data-view="dicionario"]').click()
        page.locator('#filterDict').select_option('W')
        for key in KEYS:page.locator(f'[data-dict-print="{key}"]').check()
        page.locator('#btnPrintTop').click()
        assert page.locator('#printDiagramFormat').input_value()=='screen'
        assert page.locator('#pageOrient').input_value()=='landscape'
        def verify_graph():
            q=page.locator('#printDocument [data-integrated-section="diagram"]')
            assert q.locator('figure[data-layout="horizontal"]').count()>0
            got=q.locator('[data-integrated-key][data-context="false"][data-reference="false"]').evaluate_all('(els)=>els.map(e=>e.dataset.integratedKey)')
            assert sorted(got)==sorted(KEYS),(got,KEYS)
            assert q.locator('[data-integrated-key="W05"]').count()==0
            assert q.locator('[data-print-edge="W01|W02"]').count()>0
            assert q.locator('[data-print-edge="W02|W03"]').count()>0
            assert ' C' in q.locator('[data-print-edge="W01|W02"]').first.get_attribute('d')
        verify_graph()
        # Exercise direct PDF button, not Chromium's simulated print. Check upright text and physical page size.
        out=Path(os.environ.get('DFE_PDF_DIR',tempfile.gettempdir()))
        for size,orient in [('A4','landscape'),('A4','portrait'),('A3','landscape')]:
            page.locator('#pageSize').select_option(size);page.locator('#pageOrient').select_option(orient);verify_graph()
            with page.expect_download() as dl: page.locator('#btnDownloadPdf').click()
            path=out/f'EXEMPLO_W_V238_{size}_{orient}.pdf';dl.value.save_as(path)
            with fitz.open(path) as doc:
                expected=(841.89,595.28) if size=='A4' else (1190.55,841.89)
                if orient=='portrait':expected=expected[::-1]
                t='\n'.join(pg.get_text() for pg in doc)
                assert all(k in t for k in KEYS),t
                assert 'W05' not in t and 'W38' not in t
                assert all(k in t for k in ('Leiaute do MOC','Explorador Hierárquico','Dicionário de Dados','Diagrama XML','Totalização'))
                for pg in doc:
                    assert pg.rotation==0 and abs(pg.rect.width-expected[0])<1 and abs(pg.rect.height-expected[1])<1,pg.rect
                    assert len(pg.get_text().strip())>30
                    for b in pg.get_text('dict')['blocks']:
                        for l in b.get('lines',[]):
                            assert abs(l['dir'][0]-1)<.01 and abs(l['dir'][1])<.01,l['dir']
                            x0,y0,x1,y1=l['bbox'];assert x0>=0 and y0>=0 and x1<=pg.rect.width+1 and y1<=pg.rect.height+1,(pg.number,l)
                print(f'{size} {orient}: {len(doc)} páginas, /Rotate 0, texto horizontal e pesquisável',flush=True)
        # Native browser PDF is also landscape with explicit page size.
        page.locator('#pageSize').select_option('A4');page.locator('#pageOrient').select_option('landscape')
        path=out/'EXEMPLO_W_V238_NAVEGADOR.pdf';page.pdf(path=str(path),print_background=True,prefer_css_page_size=True)
        with fitz.open(path) as d:assert all(pg.rect.width>pg.rect.height and pg.rotation==0 for pg in d)
        # Central print's override is respected, and switching back follows the screen.
        page.locator('#printDiagramFormat').select_option('vertical');assert page.locator('#printDocument figure[data-layout="horizontal"]').count()==0
        page.locator('#printDiagramFormat').select_option('screen');verify_graph()
        # Direct PDF also works for a full catalog without adding selected nodes.
        page.locator('#printType').select_option('integrated-full')
        with page.expect_download() as dl:page.locator('#btnDownloadPdf').click()
        tmp=out/'FULL_V238_TEST.pdf';dl.value.save_as(tmp)
        with fitz.open(tmp) as d:assert len(d)>4 and all(pg.rotation==0 for pg in d)
        tmp.unlink()
        assert not errors,errors
        print('PASS V2.3.8: formato aprovado, 13 campos, PDF direto, orientação e catálogo completo.',flush=True)
        browser.close()
if __name__=='__main__':run()
