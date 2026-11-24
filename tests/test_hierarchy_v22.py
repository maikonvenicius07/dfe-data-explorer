from pathlib import Path
from playwright.sync_api import sync_playwright
root=Path(__file__).resolve().parents[1]
with sync_playwright() as playwright:
 browser=playwright.chromium.launch(headless=True, executable_path='/usr/bin/chromium', args=['--no-sandbox'])
 page=browser.new_page(viewport={'width':1560,'height':930}, device_scale_factor=1)
 errors=[]
 page.on('pageerror',lambda e: errors.append(str(e)))
 page.set_content((root/'public/EXPLORADOR_OFFLINE_COMPLETO.html').read_text(encoding='utf-8'),wait_until='load',timeout=25000)
 assert page.locator('#stats').inner_text().startswith('196')
 page.locator('[data-view="moc"]').click()
 page.locator('#groupMoc').select_option('W')
 assert page.locator('#mocTables tr[data-key]').count()==42
 for item in ['W01','W02','W34','W36','W37','W38','W39','W42']:
  assert page.locator('#mocTables tr[data-key="'+item+'"]').count()==1,item
 assert page.locator('#mocTables tr[data-key="W38"]').get_attribute('class').find('moc-level-')!=-1
 assert page.locator('#mocTables tr[data-key="W38"]').get_attribute('class').find('moc-level-4')!=-1
 assert page.locator('#mocTables [data-moc-subgroup="W34"]').count()==1
 page.screenshot(path=str(root/'docs/v22_verificacao/01_grupo_W_hierarquia.png'),full_page=True)
 # Collapse only W02 and preserve sibling W34
 page.locator('[data-moc-toggle="W02"]').click()
 assert page.locator('#mocTables tr[data-key="W03"]').count()==0
 assert page.locator('#mocTables tr[data-key="W34"]').count()==1
 page.locator('#expandMoc').click()
 assert page.locator('#mocTables tr[data-key="W03"]').count()==1
 # deep search reveals ancestors
 page.locator('#searchMoc').fill('W38')
 assert page.locator('#mocTables tr[data-key="W01"]').count()==1
 assert page.locator('#mocTables tr[data-key="W34"]').count()==1
 assert page.locator('#mocTables tr[data-key="W38"]').count()==1
 page.locator('#searchMoc').fill('')
 # Mode official preserves columns; hierarchy mode technical includes XPath
 page.locator('#mocMode').select_option('official')
 assert page.locator('#mocTables .moc-table th').count()==10
 page.locator('#mocMode').select_option('oracle')
 assert 'XPath:' in page.locator('#mocTables').inner_text()
 page.locator('#mocMode').select_option('hierarchy')
 # Report -> diagram -> report
 page.locator('#mocTables [data-moc-to-diagram="W38"]').click()
 assert page.locator('#view-diagrama').is_visible()
 assert page.locator('#diagramSelection').inner_text().find('W38')!=-1
 assert page.locator('#diagramMode').input_value()=='compact'
 page.screenshot(path=str(root/'docs/v22_verificacao/02_grupo_W_diagrama.png'),full_page=True)
 page.locator('#diagramFindMoc').click()
 assert page.locator('#view-moc').is_visible()
 assert page.locator('#mocTables tr.moc-selected').count()==1
 # Directly select W group and check diagram node count, rendering natural size
 page.locator('[data-view="diagrama"]').click()
 page.locator('#diagramGroup').select_option('W')
 page.locator('#diagramFocus').select_option('')
 page.locator('#diagramMode').select_option('compact')
 page.locator('#diagramDepth').select_option('5')
 page.locator('#zoomReset').click()
 assert page.locator('#diagramSvg [data-node-key]').count()>35
 assert page.locator('#diagramSvg').evaluate('(el)=>getComputedStyle(el).width')==page.locator('#diagramSvg').get_attribute('width')+'px'
 page.screenshot(path=str(root/'docs/v22_verificacao/03_diagrama_geral_W.png'),full_page=False)
 # print hierarchy keeps 10 columns and nested elements, official mode no indentation
 page.locator('[data-view="impressao"]').click()
 page.locator('#printScope').select_option('group')
 page.locator('#printGroup').select_option('W')
 page.locator('#printType').select_option('group')
 page.locator('#printCover').uncheck()
 page.locator('#printSummary').uncheck()
 page.locator('#printDiagrams').uncheck()
 page.locator('#printMocMode').select_option('hierarchy')
 page.locator('#btnPreparePrint').click()
 assert page.locator('#printDocument .moc-hierarchy-table').count()==1
 assert page.locator('#printDocument .moc-hierarchy-table tbody tr').count()==42
 assert page.locator('#printDocument .moc-hierarchy-table th').count()==10
 page.pdf(path=str(root/'docs/v22_verificacao/04_relatorio_hierarquico_W_A4.pdf'),print_background=True,prefer_css_page_size=True)
 # diagram paginated view
 page.locator('#printType').select_option('diagram-group')
 page.locator('#pageSize').select_option('A3')
 page.locator('#printDiagrams').check()
 page.locator('#printDiagramFormat').select_option('compact')
 page.locator('#btnPreparePrint').click()
 assert page.locator('#printDocument .print-block').count()>=6
 page.pdf(path=str(root/'docs/v22_verificacao/05_diagrama_W_A3.pdf'), print_background=True,prefer_css_page_size=True)
 assert not errors, errors
 print('PASSOU: W=42, 10 colunas, subgrupos, expansão, pesquisa, navegação bidirecional, zoom 100%, impressão')
 print('Pdf samples',[(p.name,p.stat().st_size) for p in sorted((root/'docs/v22_verificacao').glob('*.pdf'))])
 browser.close()
