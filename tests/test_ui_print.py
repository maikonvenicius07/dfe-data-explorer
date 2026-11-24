"""Browser smoke tests and demo PDF fixtures; no network or official data assertions."""
from pathlib import Path
import json
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1]
H=(R/'public/index.html').read_text(encoding='utf-8')
H=H.replace('<link rel="stylesheet" href="./styles.css">','<style>'+(R/'public/styles.css').read_text(encoding='utf-8')+'</style>')
H=H.replace('<script src="./selection.js"></script>','<script>'+(R/'public/selection.js').read_text(encoding='utf-8')+'</script>')
H=H.replace('<script src="./app.js"></script>','<script>'+(R/'public/app.js').read_text(encoding='utf-8')+'</script>')
OUT=R/'docs'/'pdf_examples';OUT.mkdir(parents=True,exist_ok=True)
with sync_playwright() as p:
 b=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 page=b.new_page(viewport={'width':1440,'height':900},device_scale_factor=1)
 errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
 page.set_content(H,wait_until='load',timeout=25000)
 assert page.locator('#stats').inner_text().startswith('196'), 'seed dataset changed'
 for view in ['moc','arvore','dicionario','diagrama','xsd','oracle','atualizacoes','impressao']:
  page.locator('[data-view="'+view+'"]').click();assert page.locator('#view-'+view).is_visible(),view
 page.locator('[data-view="diagrama"]').click()
 for mode in ['horizontal','vertical','compact','oracle']:
  page.locator('#diagramMode').select_option(mode)
  assert int(page.locator('#diagramSvg').get_attribute('width'))>0,mode
 page.locator('#diagramMode').select_option('horizontal');page.evaluate("document.querySelector('#zoomReset').click()")
 assert page.locator('#diagramSvg').evaluate('(e)=>getComputedStyle(e).width')==page.locator('#diagramSvg').get_attribute('width')+'px', '100% zoom not 1:1'
 page.locator('#diagramGroup').select_option('B');page.locator('#diagramDepth').select_option('5')
 assert page.locator('#diagramSvg .diagram-node').count()>9
 page.locator('#diagramMode').select_option('compact');page.screenshot(path=str(R/'docs/preview_v22_diagrama.png'))
 page.locator('[data-view="impressao"]').click()
 presets=[
  ('GRUPO_PEQUENO_A4', 'group','A','A4','portrait'),
  ('GRUPO_EXTENSO_A4','group','W','A4','landscape'),
  ('GRUPO_TRIBUTARIO_A4','group','UB','A4','landscape'),
  ('DIAGRAMA_HIERARQUICO_A3','diagram-group','B','A3','landscape'),
  ('PADRAO_MOC_10_COLUNAS_A4','official',None,'A4','landscape'),
  ('MODELAGEM_ORACLE_A4','oracle','A','A4','landscape'),
  ('RELATORIO_TECNICO_INTEGRADO_A4','integrated','B','A4','landscape'),
 ]
 results=[]
 for title,mode,group,paper,orientation in presets:
  page.locator('#printType').select_option(mode)
  page.locator('#pageSize').select_option(paper)
  page.locator('#pageOrient').select_option(orientation)
  if group:
   page.locator('#printScope').select_option('group');page.locator('#printGroup').select_option(group)
  else:page.locator('#printScope').select_option('all')
  page.locator('#btnPreparePrint').click()
  assert len(page.locator('#printDocument').inner_text())>250,title
  path=OUT/(title+'_DEMONSTRATIVO.pdf')
  page.pdf(path=str(path),print_background=True,prefer_css_page_size=True)
  results.append((path.name,path.stat().st_size))
  print(path.name,path.stat().st_size,flush=True)
 page.screenshot(path=str(R/'docs/preview_v22_impressao.png'))
 assert not errors,'Browser JavaScript errors: '+json.dumps(errors,ensure_ascii=False)
 print('UI smoke tests passed',len(presets),'sample PDFs',flush=True)
 b.close()
