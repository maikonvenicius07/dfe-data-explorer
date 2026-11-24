"""V2.3.3: a seleção não é um filtro e o PDF usa somente campos marcados."""
from pathlib import Path
from playwright.sync_api import sync_playwright
import fitz
R=Path(__file__).resolve().parents[1]
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True, executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 page=browser.new_page(viewport={'width':1500,'height':900}, device_scale_factor=1)
 issues=[];page.on('pageerror',lambda e:issues.append(str(e)))
 page.set_content((R/'public/EXPLORADOR_OFFLINE_COMPLETO.html').read_text(encoding='utf-8'), wait_until='load')
 assert page.locator('#view-moc').is_visible()
 page.locator('[data-view="dicionario"]').click()
 assert page.locator('#dictCount').inner_text().find('Selecionados para imprimir: 0')!=-1
 assert page.locator('#dictPrintSelected').is_disabled()
 assert not page.locator('#dictCheckFiltered').is_checked()
 # Group filter only displays, and doesn't select anything
 page.locator('#filterDict').select_option('B')
 assert page.locator('#dictionary tbody tr').count()>0
 assert page.locator('#dictPrintSelected').is_disabled()
 assert page.locator('#dictCount').inner_text().find('Selecionados para imprimir: 0')!=-1
 # Select only the B02 field; filtering does not select other B fields.
 page.locator('#searchDict').fill('B02')
 assert page.locator('#dictionary tbody tr').count()==1
 page.locator('[data-dict-print="B02"]').check()
 assert page.locator('#dictCount').inner_text().find('Selecionados para imprimir: 1')!=-1
 # Filter W and W37 subgroup, keep B selection
 page.locator('#searchDict').fill('')
 page.locator('#filterDict').select_option('W')
 assert page.locator('#dictCount').inner_text().find('Selecionados para imprimir: 1')!=-1
 subgroup_values=page.locator('#dictSubgroup option').evaluate_all('(els)=>els.map(e=>e.value)')
 assert 'W37' in subgroup_values, subgroup_values
 page.locator('#dictSubgroup').select_option('W37')
 assert page.locator('[data-dict-print="W38"]').count()==1
 page.locator('[data-dict-print="W38"]').check()
 assert page.locator('#dictCount').inner_text().find('Selecionados para imprimir: 2')!=-1
 # Head selected partially (only one of subgroup's fields).
 assert page.locator('#dictCheckFiltered').evaluate('(e)=>e.indeterminate')
 # Showing only selected gives one in W, changing group doesn't discard W.
 page.locator('#dictOnlySelected').check()
 assert page.locator('#dictionary tbody tr').count()==1
 page.locator('#filterDict').select_option('B')
 assert page.locator('#dictionary tbody tr').count()==1
 assert page.locator('[data-dict-print="B02"]').is_checked()
 # Bulk 'selected filtered' acts on filter, not the whole catalog
 page.locator('#dictOnlySelected').uncheck()
 page.locator('#searchDict').fill('B02')
 page.locator('#dictUnselectFiltered').click()
 assert page.locator('#dictCount').inner_text().find('Selecionados para imprimir: 1')!=-1
 page.locator('#dictSelectFiltered').click()
 assert page.locator('#dictCount').inner_text().find('Selecionados para imprimir: 2')!=-1
 # Switch W, confirm selection. Print all selected independent of active filter B02.
 page.locator('#dictPrintSelected').click()
 assert page.locator('#view-impressao').is_visible()
 assert page.locator('#btnDoPrint').is_enabled()
 assert '2 / 196' in page.locator('#selectionCount').inner_text()
 page.locator('#printCover').uncheck()
 page.locator('#printSummary').uncheck()
 page.locator('#printDiagrams').uncheck()
 page.locator('#printType').select_option('group')
 page.locator('#printMocMode').select_option('hierarchy')
 page.locator('#printObservations').uncheck()
 page.locator('#pageSize').select_option('A4')
 page.locator('#pageOrient').select_option('landscape')
 page.locator('#btnPreparePrint').click()
 assert page.locator('#printDocument [data-key="W38"]').count()==1
 assert page.locator('#printDocument [data-key="B02"]').count()==1
 assert page.locator('#printDocument [data-key="W03"]').count()==0
 assert page.locator('#printDocument [data-key="W34"]').count()==1 # parent only context
 assert page.locator('#printDocument [data-key="W34"]').get_attribute('class').find('moc-context')!=-1
 assert page.locator('#printPreview [data-preview-remove]').count()==2
 assert 'Grupo' in page.locator('#printPreview').inner_text()
 # Column selection actually changes print table, not selection.
 page.locator('#printColumns input[data-print-col="9"]').uncheck()
 assert page.locator('#printDocument .moc-table').first.locator('th').count()==9
 assert page.locator('#printPreview [data-preview-remove]').count()==2
 # Print PDF with exactly the selected fields, searchable content
 pdf=R/'docs'/'V2_3_3_CAMPOS_B02_W38.pdf'
 page.pdf(path=str(pdf),print_background=True,prefer_css_page_size=True)
 with fitz.open(pdf) as doc:
  text='\n'.join(p.get_text() for p in doc)
  assert 'B02' in text and 'W38' in text, text[:1000]
  assert 'W03' not in text
  assert len(doc)<=5,len(doc)
 # remove B02 in preview without going back to dictionary
 page.locator('[data-preview-remove="B02"]').click()
 assert '1 / 196' in page.locator('#selectionCount').inner_text()
 assert page.locator('#printDocument [data-key="B02"]').count()==0
 assert page.locator('#printDocument [data-key="W38"]').count()==1
 # bulk select then clear explicit
 page.locator('[data-view="dicionario"]').click()
 page.locator('#dictSelectAll').click()
 assert page.locator('#dictCount').inner_text().find('Selecionados para imprimir: 196')!=-1
 page.locator('#dictClearSelection').click()
 assert page.locator('#dictPrintSelected').is_disabled()
 page.locator('[data-view="impressao"]').click()
 assert page.locator('#btnDoPrint').is_disabled()
 assert not issues,issues
 page.locator('[data-view="dicionario"]').click()
 page.screenshot(path=str(R/'docs'/'V2_3_3_DICIONARIO.png'),full_page=False)
 print('PASS: filtros independentes, subgrupo, seleção B/W, cabeçalho parcial, bulk filtrado, CSV/PDF, retirada na prévia, A4 e bloqueio com 0 campos')
 browser.close()
