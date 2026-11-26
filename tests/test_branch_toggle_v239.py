"""Exercita os botões reais e a impressão integrada, preservando seleção externa."""
from pathlib import Path
from playwright.sync_api import sync_playwright
import os, shutil
ROOT=Path(__file__).resolve().parents[1]

def run():
    with sync_playwright() as p:
        browser=p.chromium.launch(headless=True,executable_path=os.environ.get('CHROMIUM_PATH') or shutil.which('chromium'),args=['--no-sandbox'])
        page=browser.new_page(viewport={'width':1450,'height':900})
        page.set_default_timeout(7000)
        errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
        page.set_content((ROOT/'public/EXPLORADOR_OFFLINE_COMPLETO.html').read_text(),wait_until='load')
        def go(view):page.locator(f'[data-view="{view}"]').click()
        def check(selector,expected):assert page.locator(selector).is_checked()==expected,selector
        def press(selector,expected):
            el=page.locator(selector);assert expected in el.inner_text(),(selector,el.inner_text());el.click()
        go('dicionario');page.locator('#searchDict').fill('B02');page.locator('[data-dict-print="B02"]').check()
        go('moc');page.locator('#groupMoc').select_option('W');page.locator('#expandMoc').click()
        b='[data-moc-descendants="W02"]'
        check('[data-moc-print="W02"]',False);check('[data-moc-print="W03"]',False)
        press(b,'+ filhos');check('[data-moc-print="W02"]',True);check('[data-moc-print="W03"]',True);check('[data-moc-print="W01"]',False)
        press(b,'− filhos');check('[data-moc-print="W02"]',False);check('[data-moc-print="W03"]',False)
        page.locator('[data-moc-print="W03"]').check();press(b,'+ filhos');press(b,'− filhos')
        # Recolher o ramo não impede selecionar os seus descendentes ocultos.
        page.locator('[data-moc-toggle="W02"]').click();press(b,'+ filhos')
        go('arvore');page.locator('#searchTree').fill('W03');check('[data-tree-print="W03"]',True)
        press('[data-tree-descendants="W02"]','− filhos');check('[data-tree-print="W03"]',False)
        # Ficha técnica
        page.locator('#treePanel [data-key="W02"] .tree-item').click();press('#inspectorPrintDesc','Selecionar descendentes');press('#inspectorPrintDesc','Desmarcar descendentes')
        # Diagrama, seleciona e desmarca o ramo sem afetar outro grupo.
        go('diagrama');page.locator('#diagramGroup').select_option('W');page.locator('#diagramFocus').select_option('W02');page.locator('[data-node-key="W02"]').click();press('#diagramSelectDescendants','Selecionar descendentes');press('#diagramSelectDescendants','Desmarcar descendentes')
        go('dicionario');page.locator('#searchDict').fill('W03');check('[data-dict-print="W03"]',False)
        page.locator('#searchDict').fill('B02');check('[data-dict-print="B02"]',True)
        page.locator('#dictPrintSelected').click();page.locator('#printTreeSearch').fill('W03');press('[data-print-desc="W02"]','Selecionar descendentes');press('[data-print-desc="W02"]','Desmarcar descendentes')
        for sec in ('moc','tree','dictionary','diagram'):
            scope=page.locator(f'#printDocument [data-integrated-section="{sec}"]')
            selector='tr[data-key]' if sec=='moc' else '[data-integrated-key]:not([data-context="true"]):not([data-reference="true"])'
            keys=scope.locator(selector).evaluate_all('(els)=>els.map(e=>e.dataset.key||e.dataset.integratedKey)')
            assert keys==['B02'],(sec,keys)
        assert not errors,errors
        browser.close()
    print('PASS V2.3.9: MOC, árvore, ficha, diagrama, central, filtro, seleção parcial e 4 seções de impressão.')

if __name__=='__main__':run()
