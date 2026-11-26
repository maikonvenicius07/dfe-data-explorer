"""Browser regression: row caret selects one level, not an entire subtree."""
from pathlib import Path
from playwright.sync_api import sync_playwright
import os, shutil, tempfile, fitz
ROOT=Path(__file__).resolve().parents[1]

def run():
    with sync_playwright() as p:
        b=p.chromium.launch(headless=True, executable_path=os.environ.get('CHROMIUM_PATH') or shutil.which('chromium'), args=['--no-sandbox'])
        page=b.new_page(viewport={'width':1450,'height':900},accept_downloads=True)
        page.set_default_timeout(8000)
        errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
        page.set_content((ROOT/'public/EXPLORADOR_OFFLINE_COMPLETO.html').read_text(),wait_until='load')
        def picked():
            return set(page.locator('#dictionary [data-dict-print]:checked').evaluate_all('(els)=>els.map(e=>e.dataset.dictPrint)'))
        def checked(key):return page.locator(f'[data-moc-print="{key}"]').is_checked()
        def arrow(key):page.locator(f'[data-moc-toggle="{key}"]').click()
        page.locator('#groupMoc').select_option('B');page.locator('[data-moc-print="B02"]').check()
        page.locator('#groupMoc').select_option('W');page.locator('#collapseMoc').click()
        assert picked()=={'B02'}
        assert page.locator('[data-moc-print="W02"]').count()==0
        arrow('W01')
        expected={'B02','W01','W02','W17','W23','W31','W34','W60'}
        assert picked()==expected,picked()
        assert checked('W02') and page.locator('[data-moc-print="W03"]').count()==0
        arrow('W34');expected|={'W35','W36'};assert picked()==expected
        arrow('W36');expected|={'W37','W42'};assert picked()==expected
        arrow('W37');expected|={'W38','W39','W41'};assert picked()==expected
        # Collapsing is not a deselection; manually unmark an individual record.
        arrow('W37');assert picked()==expected
        arrow('W37');assert picked()==expected
        page.locator('[data-moc-print="W39"]').uncheck();expected.remove('W39');assert picked()==expected
        # Explicit mass selection remains reversible and isolated.
        branch=page.locator('[data-moc-descendants="W37"]');assert '+ filhos' in branch.inner_text()
        branch.click();assert checked('W39');branch.click();expected-={'W37','W38','W41'};assert picked()==expected
        # Search and bulk visual actions do not mark anything on their own.
        page.locator('#searchMoc').fill('W04a');assert picked()==expected
        page.locator('#searchMoc').fill('');page.locator('#expandMoc').click();assert picked()==expected
        page.locator('#collapseMoc').click();assert picked()==expected
        # Technical mode uses the same row caret.
        page.locator('#mocMode').select_option('oracle');arrow('W01');arrow('W23');expected|={'W24','W25','W26','W27','W28','W29','W30'};assert picked()==expected
        page.locator('#mocPrintSelected').click()
        assert page.locator('#printDocument [data-integrated-section]').count()==1
        for sec in ('moc',):
            scope=page.locator(f'#printDocument [data-integrated-section="{sec}"]')
            selector='tr[data-key]' if sec=='moc' else '[data-integrated-key]:not([data-context="true"]):not([data-reference="true"])'
            keys=scope.locator(selector).evaluate_all('(els)=>els.map(e=>e.dataset.key||e.dataset.integratedKey)')
            assert set(keys)==expected and len(keys)==len(expected),(sec,keys,expected)
        with tempfile.TemporaryDirectory() as tmp:
            with page.expect_download() as dl:page.locator('#btnDownloadPdf').click()
            path=Path(tmp)/'report.pdf';dl.value.save_as(path)
            with fitz.open(path) as doc:
                text='\n'.join(pg.get_text() for pg in doc)
                assert all(k in text for k in expected)
                assert 'W04a' not in text and 'W39' not in text
                assert all(pg.rotation==0 and pg.rect.width>pg.rect.height for pg in doc)
        assert not errors,errors
        b.close()
    print('PASS V2.3.12: expansão progressiva, seleção exata, recolhimento, filtros, MOC exclusivo e PDF.')

if __name__=='__main__':run()
