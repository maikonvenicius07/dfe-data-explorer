from pathlib import Path
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1]
html=(R/'public/EXPLORADOR_OFFLINE_COMPLETO.html').read_text(encoding='utf8')
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True, executable_path='/usr/bin/chromium', args=['--no-sandbox'])
 page=browser.new_page(viewport={"width":1400,"height":850})
 issues=[];page.on('pageerror',lambda e:issues.append(str(e)))
 page.set_content(html,wait_until='load',timeout=30000)
 page.locator('[data-view="diagrama"]').click()
 assert page.locator('.diagram-toolbar button:visible').count()==1
 assert page.locator('.diagram-toolbar button:visible').inner_text()=='Tela cheia'
 for id in ['diagramSidebar','diagramCenter','diagramFit','diagramFitAll','zoomOut','zoomReset','zoomIn','diagramDpi']:
  assert not page.locator('#'+id).is_visible(),id
 # Operation of original renderer, XML hierarchy and print controls retained.
 for mode in ['horizontal','vertical','compact','oracle']:
  page.locator('#diagramMode').select_option(mode)
  assert page.locator('#diagramSvg').get_attribute('width')
 page.locator('#diagramMode').select_option('compact')
 page.locator('#diagramFullscreen').click()
 assert page.evaluate('document.fullscreenElement?.id')=='diagramViewport'
 page.evaluate('document.exitFullscreen()')
 assert page.evaluate('document.fullscreenElement===null')
 page.screenshot(path=str(R/'docs/preview_v221_fullscreen_only.png'))
 page.locator('[data-view="moc"]').click()
 assert page.locator('#mocTables').locator('table').count()>0
 page.locator('[data-view="impressao"]').click()
 page.locator('#btnPreparePrint').click()
 assert len(page.locator('#printDocument').inner_text())>500
 assert not issues,issues
 print('PASS: only Tela cheia visible; fullscreen enters/exits; modes, MOC and printing intact')
 browser.close()
