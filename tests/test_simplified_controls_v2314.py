"""V2.3.14: interface sem comandos duplicados; testes em catálogo offline e estático real."""
from pathlib import Path
from playwright.sync_api import sync_playwright
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from functools import partial
from threading import Thread
import tempfile, os, shutil, fitz
ROOT=Path(__file__).resolve().parents[1]

def run():
    server=ThreadingHTTPServer(('127.0.0.1',0),partial(SimpleHTTPRequestHandler,directory=str(ROOT/'public')))
    Thread(target=server.serve_forever,daemon=True).start()
    try:
        with sync_playwright() as p:
            browser=p.chromium.launch(headless=True,executable_path=os.environ.get('CHROMIUM_PATH') or shutil.which('chromium'),args=['--no-sandbox'])
            for mode in ('offline','static'):
                page=browser.new_page(viewport={'width':1450,'height':900},accept_downloads=True)
                page.set_default_timeout(15000);errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
                # Isolated browser: use the generated standalone artifact. The static case
                # injects the exact catalog from public/data; network and storage are simulated.
                import re
                html=(ROOT/'public/EXPLORADOR_OFFLINE_COMPLETO.html').read_text()
                if mode=='static':
                    catalog=(ROOT/'public/data/catalogo_atual.json').read_text()
                    html=re.sub(r'(<script id="seedData" type="application/json">).*?(</script>)',lambda m:m[1]+catalog+m[2],html,count=1,flags=re.S)
                html=html.replace('<body>','<body><script>Object.defineProperty(window,"localStorage",{value:(()=>{const m=new Map();return {getItem:k=>m.get(k)||null,setItem:(k,v)=>m.set(k,v),removeItem:k=>m.delete(k)}})()});</script>',1)
                page.set_content(html,wait_until='load')
                assert ('1173' if mode=='static' else '196') in page.locator('#mocCount').inner_text()
                assert page.locator('[data-view]').count()==4
                assert page.locator('#btnPrintTop, [data-goto="impressao"], #printTree, #btnPreparePrint, #printObservations, #mocSelectionNote').count()==0
                assert page.locator('a[href="https://moc.sped.fazenda.pr.gov.br/NFe_NFCe/Leiaute.html"]').count()==1
                assert page.locator('#view-moc [data-select-command=all]').is_hidden()
                assert page.locator('#mocPrintSelected').is_disabled()
                page.locator('[data-view="impressao"]').click();assert page.locator('#btnDownloadPdf').is_disabled()
                page.locator('[data-view="moc"]').click()
                page.locator('#groupMoc').select_option('B');page.locator('#expandMoc').click()
                assert page.locator('#view-moc [data-select-command=all]').is_visible()
                page.locator('[data-moc-print="B02"]').check()
                page.locator('#groupMoc').select_option('W');page.locator('#collapseMoc').click()
                page.locator('[data-moc-toggle="W01"]').click()
                assert page.locator('[data-moc-print="W02"]').is_checked()
                assert page.locator('[data-moc-print="W03"]').count()==0
                page.locator('[data-moc-toggle="W02"]').click();assert page.locator('[data-moc-print="W03"]').is_checked()
                page.locator('[data-moc-descendants="W02"]').click()
                # If all W02 descendants were already marked, collective toggle clears; otherwise it completes.
                if page.locator('[data-moc-print="W03"]').is_checked():page.locator('[data-moc-descendants="W02"]').click()
                assert not page.locator('[data-moc-print="W03"]').is_checked()
                page.locator('[data-moc-print="W03"]').check()
                # Filtered bulk operations do not touch another group.
                page.locator('#searchMoc').fill('W03');page.locator('#mocUnselectFiltered').click();assert not page.locator('[data-moc-print="W03"]').is_checked()
                page.locator('#searchMoc').fill('');page.locator('[data-moc-print="W03"]').check()
                page.locator('#mocPrintSelected').click()
                def keys(root):return page.locator(root+' tr[data-key]').evaluate_all('(els)=>els.map(e=>e.dataset.key)')
                expected=keys('#printDocument');assert 'B02' in expected and 'W03' in expected and 'W04a' not in expected
                assert keys('#printPreviewRender')==expected
                assert page.locator('#printDocument [data-integrated-section]').count()==1
                assert page.locator('#printPreviewRender [data-preview-remove]').count()==len(expected)
                assert page.locator('#printDocument [data-preview-remove]').count()==0
                assert page.locator('#printDocument .moc-table').first.locator('thead th').count()==10
                page.locator('[data-preview-remove="B02"]').click();expected.remove('B02');assert keys('#printDocument')==expected
                # Presets, columns and exports remain distinct capabilities.
                page.locator('.print-presets summary').click();page.locator('#printPresetName').fill('Teste');page.locator('#printSavePreset').click()
                page.locator('[data-preview-remove="W03"]').click();assert 'W03' not in keys('#printDocument')
                page.locator('#printLoadPreset').click();assert keys('#printDocument')==expected
                page.locator('[data-print-col="9"]').uncheck();assert page.locator('#printDocument .moc-table').first.locator('thead th').count()==9
                page.locator('[data-print-col="9"]').check()
                with tempfile.TemporaryDirectory() as tmp:
                    for size,orient in [('A4','landscape'),('A4','portrait'),('A3','landscape')]:
                        page.locator('#pageSize').select_option(size);page.locator('#pageOrient').select_option(orient)
                        with page.expect_download() as dl:page.locator('#btnDownloadPdf').click()
                        path=Path(tmp)/'out.pdf';dl.value.save_as(path)
                        with fitz.open(path) as doc:
                            text='\n'.join(pg.get_text() for pg in doc)
                            assert 'W03' in text and 'B02' not in text and 'W04a' not in text
                            assert all(pg.rotation==0 and (pg.rect.width>pg.rect.height)==(orient=='landscape') for pg in doc)
                            assert all(x not in text for x in ('Explorador Hierárquico','Dicionário de Dados','Diagrama XML','Retirar da seleção'))
                            if size=='A4' and orient=='landscape' and mode=='static' and os.environ.get('DFE_QA_DIR'):
                                doc[0].get_pixmap(matrix=fitz.Matrix(1.4,1.4)).save(str(Path(os.environ['DFE_QA_DIR'])/'v2314_pdf.png'))
                    page.locator('#pageSize').select_option('A4');page.locator('#pageOrient').select_option('landscape')
                    page.pdf(path=str(Path(tmp)/'browser.pdf'),print_background=True,prefer_css_page_size=True)
                    with fitz.open(Path(tmp)/'browser.pdf') as doc:assert all(pg.rect.width>pg.rect.height for pg in doc)
                page.locator('[data-view="moc"]').click();page.locator('#view-moc [data-select-command=clear]').click();assert page.locator('#mocPrintSelected').is_disabled()
                assert not errors,errors
                page.close();print('PASS V2.3.14',mode,flush=True)
            browser.close()
    finally:server.shutdown()
if __name__=='__main__':run()
