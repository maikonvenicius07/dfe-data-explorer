"""Validação local do fluxo de seleção e impressão sem acesso à internet."""
from pathlib import Path
from playwright.sync_api import sync_playwright

R=Path(__file__).resolve().parents[1]
with sync_playwright() as p:
 b=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 page=b.new_page(viewport={'width':1480,'height':950},device_scale_factor=1)
 errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
 page.set_content((R/'public/EXPLORADOR_OFFLINE_COMPLETO.html').read_text(encoding='utf8'),wait_until='load',timeout=20000)
 assert page.locator('#view-moc').is_visible()
 assert page.locator('#mocTables tr[data-key]').count()==196
 assert page.locator('[data-view="resumo"]').count()==0
 page.locator('[data-view="impressao"]').click()
 assert '196 / 196' in page.locator('#selectionCount').inner_text()
 page.locator('#printClearSelection').click()
 assert '0 / 196' in page.locator('#selectionCount').inner_text()
 assert page.locator('#btnDoPrint').is_disabled()
 # selecionar W inteiro e depois um subgrupo individual
 page.locator('#printTreeSearch').fill('W34')
 page.locator('[data-tree-key="W34"]').check()
 assert int(page.locator('#selectionCount strong').inner_text().split('/')[0].strip())>1
 assert page.locator('#printTree [data-tree-group="W"]').evaluate('(e)=>e.indeterminate')
 page.locator('#printTreeSearch').fill('')
 page.locator('#printClearSelection').click()
 page.locator('#printTreeSearch').fill('W38')
 page.locator('[data-tree-key="W38"]').check()
 # W38 não possui filhos; selecioná-lo não marca outros campos do grupo W.
 assert '1 / 196' in page.locator('#selectionCount').inner_text()
 page.locator('#printCover').uncheck()
 page.locator('#printSummary').uncheck()
 page.locator('#printDiagrams').uncheck()
 page.locator('#printType').select_option('group')
 page.locator('#btnPreparePrint').click()
 assert page.locator('#printDocument [data-key="W38"]').count()==1
 assert page.locator('#printDocument [data-key="W03"]').count()==0
 assert page.locator('#printDocument [data-key="W34"]').count()==1
 assert page.locator('#printDocument .moc-context').count()>0
 assert page.locator('#printDocument .moc-table thead th').count()==10
 assert '1 / 196' in page.locator('#selectionCount').inner_text()
 # Save & reload, printing and diagram integration
 page.locator('#printPresetName').fill('Somente W38')
 page.locator('#printSavePreset').click()
 page.locator('#printSelectAll').click()
 page.locator('#printPresetList').select_option('Somente W38')
 page.locator('#printLoadPreset').click()
 assert '1 / 196' in page.locator('#selectionCount').inner_text()
 page.screenshot(path=str(R/'docs/v23_selecao_impressao.png'),full_page=False)
 # PDF real: a capa é opcional, texto deve ser pesquisável.
 pdf=R/'docs/v23_relatorio_selecao_W38.pdf'
 page.pdf(path=str(pdf),print_background=True,prefer_css_page_size=True)
 assert pdf.stat().st_size>10000
 page.locator('[data-view="dicionario"]').click()
 page.locator('#dictColumnsToggle').click()
 assert page.locator('#dictColumnPanel input[type="checkbox"]').count()>=10
 page.locator('#searchDict').fill('W38')
 assert page.locator('#dictionary tbody tr').count()==1
 page.locator('#dictPrintSelected').click()
 assert page.locator('#view-impressao').is_visible()
 assert '1 / 196' in page.locator('#selectionCount').inner_text()
 # preserva requisito da barra de apenas tela cheia
 page.locator('[data-view="diagrama"]').click()
 assert page.locator('.diagram-toolbar button:visible').count()==1
 assert page.locator('.diagram-toolbar button:visible').inner_text()=='Tela cheia'
 assert not errors,errors
 print('PASS: 196 nós, tela inicial MOC, seleção de subgrupo, campo W38, estados parciais, presets, impressão, PDF, dicionário, tela cheia')
 b.close()
