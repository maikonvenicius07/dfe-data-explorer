"""A Visão Geral foi removida a pedido do usuário; o MOC é a tela inicial."""
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
with sync_playwright() as pw:
    browser=pw.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
    page=browser.new_page(viewport={"width":1366,"height":768})
    errors=[]
    page.on('pageerror',lambda e:errors.append(str(e)))
    page.set_content((ROOT/'public/EXPLORADOR_OFFLINE_COMPLETO.html').read_text(encoding='utf-8'),wait_until='load',timeout=20000)
    assert page.locator('[data-view="resumo"]').count()==0
    assert page.locator('#view-resumo').count()==0
    assert page.locator('#view-moc').is_visible()
    assert 'active' in page.locator('[data-view="moc"]').get_attribute('class')
    assert page.locator('#mocTables tr[data-key]').count()==196
    for view in ['arvore','dicionario','diagrama','xsd','oracle','atualizacoes','impressao','moc']:
        page.locator('[data-view="'+view+'"]').click()
        assert page.locator('#view-'+view).is_visible(), view
    page.locator('[data-view="diagrama"]').click()
    assert page.locator('#diagramSvg').get_attribute('width')
    page.locator('[data-view="impressao"]').click()
    assert '0 / 196' in page.locator('#selectionCount').inner_text()
    assert page.locator('#btnPreparePrint').is_disabled()
    page.locator('#printTreeSearch').fill('W38')
    page.locator('[data-tree-key="W38"]').check()
    assert page.locator('#btnPreparePrint').is_enabled()
    page.locator('#btnPreparePrint').click()
    assert len(page.locator('#printDocument').inner_text())>100
    assert not errors,errors
    print('PASS: Visão Geral ausente, MOC inicial, catálogo de 196 nós, menu, diagramas e impressão.')
    browser.close()
