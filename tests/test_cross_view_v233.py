from pathlib import Path
from playwright.sync_api import sync_playwright
r=Path(__file__).resolve().parents[1]
with sync_playwright() as p:
 b=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 page=b.new_page(viewport={'width':1450,'height':850})
 issues=[];page.on('pageerror',lambda e:issues.append(str(e)))
 page.set_content((r/'public/EXPLORADOR_OFFLINE_COMPLETO.html').read_text(encoding='utf8'),wait_until='load')
 assert page.locator('[data-view="resumo"]').count()==0
 page.locator('#groupMoc').select_option('W')
 page.locator('#searchMoc').fill('W38')
 assert page.locator('[data-moc-print="W38"]').count()==1
 page.locator('[data-moc-print="W38"]').check()
 page.locator('[data-view="dicionario"]').click()
 page.locator('#searchDict').fill('W38')
 assert page.locator('[data-dict-print="W38"]').is_checked()
 page.locator('[data-view="arvore"]').click()
 # tree may start collapsed; expand search to show W38
 page.locator('#searchTree').fill('W38')
 assert page.locator('[data-tree-print="W38"]').is_checked()
 page.locator('[data-tree-print="W38"]').uncheck()
 page.locator('[data-view="dicionario"]').click()
 assert not page.locator('[data-dict-print="W38"]').is_checked()
 page.locator('[data-view="diagrama"]').click()
 page.locator('#diagramGroup').select_option('W')
 page.locator('#diagramFocus').select_option('W37')
 page.locator('#diagramDepth').select_option('3')
 # Select the node in diagram; controls should sync with dictionary.
 page.locator('#diagramSvg [data-node-key="W38"]').first.click()
 assert page.locator('#diagramPrintSelected').count()==1
 page.locator('#diagramPrintSelected').check()
 page.locator('[data-view="dicionario"]').click()
 assert page.locator('[data-dict-print="W38"]').is_checked()
 assert not issues,issues
 print('PASS: MOC ⇄ árvore ⇄ diagrama ⇄ dicionário, seleção manual sincronizada')
 b.close()
