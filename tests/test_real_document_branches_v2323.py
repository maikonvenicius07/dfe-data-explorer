from pathlib import Path
import json,shutil,fitz,os,tempfile
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];Q=Path(os.environ.get('DFE_QA_DIR',tempfile.mkdtemp()));Q.mkdir(parents=True,exist_ok=True)
def run():
    with sync_playwright() as pw:
     b=pw.chromium.launch(executable_path=shutil.which('chromium'),args=['--no-sandbox']);p=b.new_page(accept_downloads=True,viewport={'width':1600,'height':1000});p.set_default_timeout(12000);err=[];p.on('pageerror',lambda e:err.append(str(e)));p.set_content((R/'public/EXPLORADOR_OFFLINE_COMPLETO.html').read_text().replace('normalize(data);fetchServer();','normalize(data);'),timeout=60000)
     for doc,tag in [('nf3e','total'),('nfcom','gFidelidade'),('mdfe','ide'),('cte','emit')]:
      p.locator(f'[data-document="{doc}"]').click();c=json.loads((R/'public/data'/doc/'catalogo_atual.json').read_text());n=next(n for n in c['nodes'] if n['tag']==tag);k=n['key'];print(doc,p.locator('#sourceNotice').inner_text()[:800],flush=True)
      p.locator('#groupMoc').select_option(n['mocGroup']);p.locator('#expandMoc').click();p.locator(f'[data-moc-descendants="{k}"]').click();sel=p.locator('#mocTables [data-moc-print]:checked').count();assert sel>1
      p.screenshot(path=str(Q/(doc+'-tela.png')));p.locator('#mocPrintSelected').click();
      keys=p.locator('#printDocument tr[data-key]').evaluate_all('(els)=>els.map(e=>e.dataset.key)');assert k in keys and len(keys)==len(set(keys))
      with p.expect_download() as dl:p.locator('#btnDownloadPdf').click()
      out=Q/(doc+'-ramo.pdf');dl.value.save_as(out)
      with fitz.open(out) as f:
       assert tag in ''.join(x.get_text() for x in f);print('ramo',doc,sel,len(keys),len(f),flush=True);f[0].get_pixmap().save(Q/(doc+'-ramo.png'))
     assert not err,err;b.close()
if __name__=="__main__":run()
