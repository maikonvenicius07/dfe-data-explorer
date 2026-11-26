"""Menu simplificado, seleção reversível e PDF sem dependência das telas retiradas."""
from pathlib import Path
from playwright.sync_api import sync_playwright
import fitz, shutil, os, tempfile
ROOT=Path(__file__).resolve().parents[1]
PUBLIC=['moc','oracle','atualizacoes','impressao']
INTERNAL=['arvore','dicionario','diagrama','xsd']

def run():
    with sync_playwright() as p:
        browser=p.chromium.launch(headless=True,executable_path=os.environ.get('CHROMIUM_PATH') or shutil.which('chromium'),args=['--no-sandbox'])
        page=browser.new_page(viewport={'width':1450,'height':900},accept_downloads=True)
        page.set_default_timeout(7000)
        errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
        page.set_content((ROOT/'public/EXPLORADOR_OFFLINE_COMPLETO.html').read_text(),wait_until='load')
        assert page.locator('.navlink').evaluate_all('(els)=>els.map(e=>e.dataset.view)')==PUBLIC
        assert page.locator('#view-moc').is_visible()
        for view in PUBLIC:
            page.locator(f'[data-view="{view}"]').click()
            assert page.locator(f'#view-{view}').is_visible()
            assert page.locator('.view:visible').count()==1
            for old in INTERNAL:
                assert page.locator(f'#view-{old}').is_hidden()
        page.locator('[data-view="moc"]').click()
        assert page.locator('[data-moc-to-diagram]').count()==0
        for mode in ('official','hierarchy','oracle'):
            page.locator('#mocMode').select_option(mode)
            page.locator('#groupMoc').select_option('')
            page.locator('#expandMoc').click()
            assert page.locator('#mocTables .moc-group').count()>1
            assert page.locator('#mocTables .moc-subgroup-nav, #mocTables [data-moc-subgroup]').count()==0
            assert page.locator('#mocTables').get_by_text('Divisões XML neste grupo:',exact=True).count()==0
            assert page.locator('#mocTables .moc-group-body > .table-scroller').count()==page.locator('#mocTables .moc-group').count()
        page.locator('#mocMode').select_option('hierarchy')
        print('Faixa removida em todos os grupos e nos três modos do MOC.',flush=True)
        page.locator('#groupMoc').select_option('B');page.locator('#expandMoc').click()
        page.locator('[data-moc-print="B02"]').check()
        page.locator('#groupMoc').select_option('W');page.locator('#expandMoc').click()
        branch=page.locator('[data-moc-descendants="W02"]')
        assert '+ filhos' in branch.inner_text();branch.click()
        assert page.locator('[data-moc-print="W03"]').is_checked()
        assert '− filhos' in branch.inner_text();branch.click()
        assert not page.locator('[data-moc-print="W03"]').is_checked()
        page.locator('[data-moc-print="W03"]').check()
        page.locator('#mocPrintSelected').click()
        assert page.locator('#view-impressao').is_visible()
        assert page.locator('#printDiagramFormat').input_value()=='horizontal'
        assert page.locator('#printDocument [data-integrated-section]').count()==1
        for sec in ('moc',):
            scope=page.locator(f'#printDocument [data-integrated-section="{sec}"]')
            selector='tr[data-key]' if sec=='moc' else '[data-integrated-key]:not([data-context="true"]):not([data-reference="true"])'
            keys=scope.locator(selector).evaluate_all('(els)=>els.map(e=>e.dataset.key||e.dataset.integratedKey)')
            assert sorted(keys)==['B02','W03'],(sec,keys)
        assert page.locator('#printDocument figure').count()==0
        with tempfile.TemporaryDirectory() as tmp:
            for size,orient in [('A4','landscape'),('A4','portrait'),('A3','landscape')]:
                page.locator('#pageSize').select_option(size);page.locator('#pageOrient').select_option(orient)
                with page.expect_download() as dl:page.locator('#btnDownloadPdf').click()
                path=Path(tmp)/'report.pdf';dl.value.save_as(path)
                with fitz.open(path) as doc:
                    text='\n'.join(pg.get_text() for pg in doc)
                    assert 'B02' in text and 'W03' in text and 'W04a' not in text
                    assert all(pg.rotation==0 and ((pg.rect.width>pg.rect.height)==(orient=='landscape')) for pg in doc)
                    for pg in doc:
                        for b in pg.get_text('dict')['blocks']:
                            for l in b.get('lines',[]): assert abs(l['dir'][0]-1)<.01 and abs(l['dir'][1])<.01
                print(f'PDF {size} {orient}: orientação e seleção OK',flush=True)
        assert page.locator('#integratedSections').is_hidden()
        assert page.locator('#printDocument [data-integrated-section]').count()==1
        page.locator('#printClearSelection').click();assert page.locator('#btnDownloadPdf').is_disabled()
        assert not errors,errors
        browser.close()
    print('PASS: menu de quatro telas, módulos ocultos, seleção e PDF exclusivo do MOC.')

if __name__=='__main__':run()
