from pathlib import Path
from playwright.sync_api import sync_playwright
import re,fitz
import os, tempfile, shutil
R=Path(__file__).resolve().parents[1];Q=Path(os.environ.get('DFE_QA_DIR',tempfile.mkdtemp(prefix='dfe2319_')));Q.mkdir(parents=True,exist_ok=True);keys='W01 W01a W02 W17 W23 W31 W34 W35 W36 W37 W42 W43 W44 W46 W47 W48 W49 W50 W57 W59e W59h W60'.split()
def run():
 with sync_playwright() as p:
  b=p.chromium.launch(executable_path=shutil.which('chromium'),args=['--no-sandbox']);page=b.new_page(accept_downloads=True,viewport={'width':1600,'height':1000});errors=[];page.on('pageerror',lambda e:errors.append(str(e)));html=(R/'public/EXPLORADOR_OFFLINE_COMPLETO.html').read_text();cat=(R/'public/data/catalogo_atual.json').read_text();html=re.sub(r'(<script id="seedData" type="application/json">).*?(</script>)',lambda m:m[1]+cat+m[2],html,count=1,flags=re.S);html=html.replace('normalize(data);fetchServer();','normalize(data);window.qa={printSelection,go,printable,nodes};');page.set_content(html,wait_until='load');page.evaluate('(keys)=>{qa.printSelection.changeKeys(keys,true);qa.go("impressao");}',keys)
  def pdf(name,expected):
   meta=page.locator('#printPreview').inner_text(); print(name,meta.replace('\n',' '),flush=True)
   source=page.locator('#printDocument tr[data-key]').evaluate_all('es=>es.map(e=>[e.dataset.key,e.dataset.depth,e.dataset.rails,e.dataset.ends,e.dataset.child])');prev=page.locator('#printPreviewRender tr[data-key]').evaluate_all('es=>es.map(e=>[e.dataset.key,e.dataset.depth,e.dataset.rails,e.dataset.ends,e.dataset.child])');assert source==prev and {a[0] for a in prev}==set(expected)
   n=page.locator('#printPreviewRender .physical-preview').count();assert n>0
   page.pdf(path=str(Q/(name+'_browser.pdf')),print_background=True,prefer_css_page_size=True)
   with page.expect_download() as dl:page.locator('#btnDownloadPdf').click()
   dl.value.save_as(Q/(name+'_direto.pdf'))
   for suffix in ['browser','direto']:
    with fitz.open(Q/(name+'_'+suffix+'.pdf')) as d:
     assert len(d)==n,(name,suffix,len(d),n)
     assert all('V2.3.19' in pg.get_text() for pg in d)
     assert all(pg.rotation==0 for pg in d)
     # Exact IDs by location of ID column, excluding the parent column and headings.
     m=int(page.locator('#printMargin').input_value())*72/25.4; weights=118; ids=[]
     for pg in d:
      width=pg.rect.width-2*m; x0=m+6/weights*width; x1=m+14/weights*width
      words=pg.get_text('words'); assert all(w[0]>=0 and w[2]<=pg.rect.width+1 and w[1]>=0 and w[3]<=pg.rect.height+1 for w in words)
      clip=fitz.Rect(x0-.4,0,x1-.4,pg.rect.height); ids.extend(match.group(0) for l in pg.get_text(clip=clip).splitlines() if (match:=re.search(r'W[0-9]+[a-z0-9.]*$',l.strip())) and match.group(0) in expected)
     assert ids==[a[0] for a in source],(name,suffix,ids)
     print(suffix,len(d),'páginas, IDs íntegros',flush=True)
   return n
  page.locator('#pageOrient').select_option('portrait');assert pdf('W22_A4_retrato',keys)==1
  assert 'fonte da tabela 8.5 pt' in page.locator('#printPreview').inner_text()
  # Both print buttons must use identical PDF bytes; intercept the viewer URL only.
  page.evaluate("window.open=(url)=>{window.qaPdfUrl=url;return {opener:null}}")
  page.locator('#btnDoPrint').click()
  import base64
  raw=page.evaluate("async()=>{const a=new Uint8Array(await (await fetch(window.qaPdfUrl)).arrayBuffer());return btoa(Array.from(a,x=>String.fromCharCode(x)).join(''))}")
  assert base64.b64decode(raw)==(Q/'W22_A4_retrato_direto.pdf').read_bytes()
  assert 'PDF aberto' in page.locator('#printOutputStatus').inner_text()
  page.locator('#pageOrient').select_option('landscape');pdf('W22_A4_paisagem',keys)
  page.locator('#pageSize').select_option('A3');assert pdf('W22_A3_paisagem',keys)==1
  page.locator('#pageOrient').select_option('portrait');pdf('W22_A3_retrato',keys)
  page.locator('#pageSize').select_option('A4');page.locator('#printFit').select_option('real');pdf('W22_tamanho_real',keys)
  page.locator('#printFit').select_option('auto');pdf('W22_auto',keys)
  old=keys[:5]+'W24 W25 W26 W27 W28 W29 W30'.split()+keys[5:];page.evaluate('(keys)=>{qa.printSelection.all(false);qa.printSelection.changeKeys(keys,true);qa.printable()}',old);page.locator('#printFit').select_option('one');assert pdf('W29_A4_retrato',old)==2
  full=page.evaluate('()=>qa.nodes.filter(n=>n.group==="W").map(n=>n.key)');page.evaluate('(keys)=>{qa.printSelection.all(false);qa.printSelection.changeKeys(keys,true);qa.printable()}',full);page.locator('#pageOrient').select_option('landscape');assert pdf('W_completo_A4',full)>1
  assert not errors,errors;b.close()

if __name__=='__main__':run()
