"""Impressão exclusivamente dos registros escolhidos, sem outras seções."""
from pathlib import Path
from playwright.sync_api import sync_playwright
import fitz, shutil, os, tempfile
ROOT=Path(__file__).resolve().parents[1]

def run():
    with sync_playwright() as p:
        browser=p.chromium.launch(headless=True,executable_path=os.environ.get('CHROMIUM_PATH') or shutil.which('chromium'),args=['--no-sandbox'])
        page=browser.new_page(viewport={'width':1450,'height':900},accept_downloads=True)
        page.set_default_timeout(8000);errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
        page.set_content((ROOT/'public/EXPLORADOR_OFFLINE_COMPLETO.html').read_text(),wait_until='load')
        page.locator('#btnPrintTop').click()
        assert page.locator('#btnDownloadPdf').is_disabled() and page.locator('#btnDoPrint').is_disabled()
        for selector in ('#integratedSections','#printType','#printCover','#printSummary','#printDiagramFormat'):
            assert page.locator(selector).is_hidden(),selector
        page.locator('[data-view="moc"]').click()
        page.locator('#groupMoc').select_option('B');page.locator('#expandMoc').click();page.locator('[data-moc-print="B02"]').check()
        page.locator('#groupMoc').select_option('W');page.locator('#expandMoc').click();page.locator('[data-moc-print="W03"]').check()
        page.locator('#mocPrintSelected').click()
        def verify(keys):
            for root in ('#printDocument','#printPreviewRender'):
                assert page.locator(root+' [data-integrated-section]').evaluate_all('(els)=>els.map(e=>e.dataset.integratedSection)')==['moc']
                assert sorted(page.locator(root+' tr[data-key]').evaluate_all('(els)=>els.map(e=>e.dataset.key)'))==sorted(keys)
                assert page.locator(root+' .moc-table').first.locator('thead th').count()==10
                assert page.locator(root+' .print-cover, '+root+' .print-integrated-summary, '+root+' svg').count()==0
        verify(['B02','W03'])
        # Mesmo controles legados alterados programaticamente não podem produzir outras seções.
        page.evaluate("""()=>{for(const id of ['printSectionTree','printSectionDict','printSectionDiagram','printCover','printSummary'])document.getElementById(id).checked=true; document.getElementById('printType').value='';}""")
        page.locator('#btnPreparePrint').click();verify(['B02','W03'])
        def check_pdf(path,land=True,paper='A4'):
            with fitz.open(path) as d:
                text='\n'.join(pg.get_text() for pg in d)
                assert 'B02' in text and 'W03' in text and 'W04a' not in text and 'B03' not in text
                assert all(t not in text for t in ('Explorador Hierárquico','Dicionário de Dados','Diagrama XML','Sumário da seleção'))
                assert len(d)==1,len(d)
                for pg in d:
                    assert pg.rotation==0 and ((pg.rect.width>pg.rect.height)==land)
                    assert abs(max(pg.rect.width,pg.rect.height)-(841.89 if paper=='A4' else 1190.55))<1
                    assert all(abs(l['dir'][0]-1)<.01 for block in pg.get_text('dict')['blocks'] for l in block.get('lines',[]))
        with tempfile.TemporaryDirectory() as tmp:
            for size,orient in [('A4','landscape'),('A4','portrait'),('A3','landscape')]:
                page.locator('#pageSize').select_option(size);page.locator('#pageOrient').select_option(orient)
                with page.expect_download() as dl:page.locator('#btnDownloadPdf').click()
                path=Path(tmp)/'report.pdf';dl.value.save_as(path);check_pdf(path,orient=='landscape',size)
                if size=='A4' and orient=='landscape' and os.environ.get('DFE_PDF_DIR'):
                    shutil.copyfile(path,Path(os.environ['DFE_PDF_DIR'])/'QA_MOC_V2313.pdf')
            page.locator('#pageSize').select_option('A4');page.locator('#pageOrient').select_option('landscape')
            path=Path(tmp)/'browser.pdf';page.pdf(path=str(path),print_background=True,prefer_css_page_size=True);check_pdf(path)
        page.locator('[data-preview-remove="B02"]').click();verify(['W03'])
        page.locator('#printClearSelection').click();assert page.locator('#btnDownloadPdf').is_disabled()
        assert not errors,errors
        browser.close()
    print('PASS V2.3.13: MOC exclusivo, seleção exata, A4/A3, PDF direto e navegador, sem seções extras.')
if __name__=='__main__':run()
