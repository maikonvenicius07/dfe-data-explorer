"""Browser regression, real PDF, three print modes and four shared views."""
from pathlib import Path
from playwright.sync_api import sync_playwright
import os, tempfile, shutil
import fitz
R=Path(__file__).resolve().parents[1]

def run():
    with sync_playwright() as p:
        browser=p.chromium.launch(headless=True,executable_path=os.environ.get('CHROMIUM_PATH') or shutil.which('chromium'),args=['--no-sandbox'])
        page=browser.new_page(viewport={'width':1450,'height':900})
        page.set_default_timeout(5000)
        errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
        page.set_content((R/'public/EXPLORADOR_OFFLINE_COMPLETO.html').read_text(),wait_until='load')
        def go(v): page.locator(f'[data-view="{v}"]').click()
        def selected_keys():
            return sorted(page.locator('#printDocument [data-integrated-section="moc"] tr[data-key]').evaluate_all('(els)=>els.map(e=>e.dataset.key)'))
        def assert_sections(expected):
            expected=sorted(expected)
            assert selected_keys()==expected,(selected_keys(),expected)
            for sec in ('tree','dictionary','diagram'):
                keys=page.locator(f'#printDocument [data-integrated-section="{sec}"] [data-integrated-key]:not([data-context="true"]):not([data-reference="true"])').evaluate_all('(els)=>els.map(e=>e.getAttribute("data-integrated-key"))')
                assert sorted(keys)==expected,(sec,keys,expected)
        assert page.locator('#mocPrintSelected').is_disabled()
        page.locator('#groupMoc').select_option('W');page.locator('#searchMoc').fill('W38')
        assert page.locator('#mocPrintSelected').is_disabled()
        page.locator('[data-moc-print="W38"]').check()
        go('dicionario');page.locator('#searchDict').fill('W38');assert page.locator('[data-dict-print="W38"]').is_checked()
        page.locator('#searchDict').fill('B02');page.locator('[data-dict-print="B02"]').check()
        go('arvore');page.locator('#searchTree').fill('W38');assert page.locator('[data-tree-print="W38"]').is_checked();page.locator('[data-tree-print="W38"]').uncheck();page.locator('[data-tree-print="W38"]').check()
        go('diagrama');page.locator('#diagramGroup').select_option('W');page.locator('#diagramFocus').select_option('W37');page.locator('#diagramMode').select_option('horizontal');page.locator('[data-expand-key="W37"]').click()
        assert page.locator('[data-diagram-check="W38"]').get_attribute('aria-checked')=='true'
        page.locator('[data-diagram-check="W38"]').click();assert page.locator('[data-diagram-check="W38"]').get_attribute('aria-checked')=='false';page.locator('[data-diagram-check="W38"]').click()
        page.locator('[data-diagram-check="W37"]').click();assert page.locator('[data-diagram-check="W39"]').get_attribute('aria-checked')=='false';page.locator('[data-diagram-check="W37"]').click()
        page.locator('#diagramPrintManual').click();assert page.locator('#printType').input_value()=='integrated'
        page.locator('#printCover').uncheck();page.locator('#printSummary').uncheck();page.locator('#pageOrient').select_option('landscape')
        assert_sections(['B02','W38'])
        assert page.locator('#printDocument [data-print-edge="W37|W38"]').count()==1
        assert page.locator('#printDocument [data-integrated-key="W39"]').count()==0
        assert page.locator('#printDocument [data-integrated-section="diagram"] svg').count()>0
        assert page.locator('#printPreviewRender [data-integrated-section]').count()==4
        assert page.locator('#printDocument [data-integrated-section="moc"] th').first.inner_text()=='#'
        # All 4 views yield the same selected report, regardless of previous type.
        for view,button in [('moc','#mocPrintSelected'),('arvore','#treePrintSelected'),('dicionario','#dictPrintSelected')]:
            page.locator('#printType').select_option('diagram-current');go(view);page.locator(button).click();assert page.locator('#printType').input_value()=='integrated';assert_sections(['B02','W38'])
        # A real PDF with all four sections, verify extracted text and page bounds.
        output=os.environ.get('DFE_PDF_DIR')
        for format,orientation in [('horizontal','landscape'),('vertical','portrait'),('compact','landscape')]:
            go('diagrama');page.locator('#diagramMode').select_option(format);page.locator('#diagramPrintManual').click();page.locator('#pageOrient').select_option(orientation)
            assert_sections(['B02','W38']);assert page.locator('#printDocument [data-print-edge="W37|W38"]').count()==1
            path=Path(output or tempfile.gettempdir())/f'EXEMPLO_INTEGRADO_V237_{format}.pdf';page.pdf(path=str(path),print_background=True,prefer_css_page_size=True)
            with fitz.open(path) as doc:
                text='\n'.join(x.get_text() for x in doc)
                assert all(x in text for x in ['B02','W38','Diagrama XML','Dicionário de Dados','Explorador Hierárquico','Leiaute do MOC']),text[:1000]
                assert 'W39' not in text and 'W03' not in text
                assert all(len(x.get_text().strip())>20 for x in doc), 'Página vazia'
                for pg in doc:
                    for x0,y0,x1,y1,*_ in pg.get_text('words'):
                        assert x0>=0 and y0>=0 and x1<=pg.rect.width+1 and y1<=pg.rect.height+1,(format,pg.number,(x0,y0,x1,y1),pg.rect)
                print(f'PDF {format}: {len(doc)} páginas',flush=True)
            if not output:path.unlink()
        page.locator('#printSectionMoc').uncheck();page.locator('#printSectionTree').uncheck();assert page.locator('#printDocument [data-integrated-section]').count()==2
        page.locator('#printSectionMoc').check();page.locator('#printSectionTree').check();assert_sections(['B02','W38'])
        # Current print ignores manually marked fields and captures only view's records.
        go('dicionario');page.locator('#searchDict').fill('W39');page.locator('[data-current-print="dicionario"]').click();assert page.locator('#printType').input_value()=='integrated-current';assert_sections(['W39'])
        page.locator('#printType').select_option('integrated');assert_sections(['B02','W38'])
        for view,selector in [('moc','#mocTables .moc-group:not(.closed) tr[data-key]'),('arvore','#treePanel .tree-line[data-key]'),('diagrama','#diagramSvg [data-diagram-key]')]:
            go(view)
            if view=='diagrama':
                expected=page.locator('#diagramSvg [data-diagram-check]').evaluate_all('(els)=>els.map(e=>e.getAttribute("data-diagram-check"))')
                expected=list(set(expected))
            else:
                expected=page.locator(selector).evaluate_all('(els)=>els.filter(e=>e.getClientRects().length).map(e=>e.dataset.key)')
            assert expected,view
            page.locator(f'[data-current-print="{view}"]').click();assert_sections(expected)
            page.locator('#printType').select_option('integrated');assert_sections(['B02','W38'])
        # Full catalog print: every node appears once as data, even with pagination references.
        page.locator('#printType').select_option('integrated-full');assert len(selected_keys())==196
        assert_sections(selected_keys())
        page.locator('#printType').select_option('integrated');assert_sections(['B02','W38'])
        page.locator('[data-preview-remove="B02"]').click();assert_sections(['W38']);page.locator('[data-preview-remove="W38"]').click();assert page.locator('#btnDoPrint').is_disabled()
        assert not errors,errors
        print('PASS V2.3.7: quatro entradas, quatro seções, PDF vetorial, formatos, seleção atual/completa, revisão e vazio.',flush=True)
        browser.close()

if __name__=='__main__':run()
