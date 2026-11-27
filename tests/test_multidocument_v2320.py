from pathlib import Path
from playwright.sync_api import sync_playwright
import os,shutil,fitz,tempfile,re
R=Path(__file__).resolve().parents[1];Q=Path(os.environ.get('DFE_QA_DIR',tempfile.mkdtemp(prefix='dfe2320_')));Q.mkdir(parents=True,exist_ok=True)

def run():
 with sync_playwright() as p:
  b=p.chromium.launch(executable_path=shutil.which('chromium'),args=['--no-sandbox']);page=b.new_page(accept_downloads=True,viewport={'width':1600,'height':1000});errors=[];page.on('pageerror',lambda e:errors.append(str(e)));html=(R/'public/EXPLORADOR_OFFLINE_COMPLETO.html').read_text();cat=(R/'public/data/catalogo_atual.json').read_text();html=re.sub(r'(<script id="seedData" type="application/json">).*?(</script>)',lambda m:m[1]+cat+m[2],html,count=1,flags=re.S);html=html.replace('normalize(data);fetchServer();','normalize(data);');page.set_content(html,wait_until='load');page.wait_for_function("document.querySelector('#mocCount').textContent.includes('1173')",timeout=15000)
  assert page.locator('[data-document]').count()==10
  def choose_doc(doc):page.locator(f'[data-document="{doc}"]').click();page.wait_for_function("document.querySelector('#view-moc').classList.contains('active')")
  def mark(key):page.locator(f'#mocTables [data-moc-print="{key}"]').check()
  def checked(key):return page.locator(f'#mocTables [data-moc-print="{key}"]').is_checked()
  def pdf(name,required,forbidden,orientation="landscape",pages=None):
   page.locator('#mocPrintSelected').click();page.locator('#pageOrient').select_option(orientation)
   with page.expect_download() as dl:page.locator('#btnDownloadPdf').click()
   dest=Q/(name+'.pdf');dl.value.save_as(dest)
   with fitz.open(dest) as doc:
    text='\n'.join(p.get_text() for p in doc)
    assert all(t in text for t in required),(name,required,text)
    assert all(t not in text for t in forbidden),(name,forbidden,text)
    assert all(p.rotation==0 for p in doc)
    if pages is not None:assert len(doc)==pages,(name,len(doc))
    for i,p in enumerate(doc):p.get_pixmap(matrix=fitz.Matrix(1.2,1.2)).save(Q/(name+f'_{i+1}.png'))
   print(name,'OK',flush=True)
  page.locator('#groupMoc').select_option('W');mark('W03');assert checked('W03');pdf('NF-e',['vBC','V2.3.20'],['vDC'])
  choose_doc('nfe');page.locator('#view-moc [data-select-command=clear]').click();keys='W01 W01a W02 W17 W23 W31 W34 W35 W36 W37 W42 W43 W44 W46 W47 W48 W49 W50 W57 W59e W59h W60'.split()
  for k in keys:mark(k)
  pdf('NF-e-W22',['vNFTot','V2.3.20'],['vDC'],'portrait',1)
  choose_doc('nfe');page.locator('#view-moc [data-select-command=clear]').click();mark('W03')
  choose_doc('dce');assert '111' in page.locator('#mocCount').inner_text();assert 'cobertura parcial' in page.locator('#badgeStatus').inner_text();assert not page.locator('#mocTables [data-moc-print]:checked').count();page.locator('#groupMoc').select_option('W');page.locator('[data-moc-toggle="W01"]').click();assert not checked('W01') and not checked('W16');mark('W16');assert checked('W16');pdf('DC-e',['vDC','DC-e','V2.3.20'],['vICMS','IBSCBSTot']);
  choose_doc('dce');page.locator('#groupMoc').select_option('Z');page.locator('#searchMoc').fill('Z06');mark('Z06|Z05|xCampo');assert checked('Z06|Z05|xCampo') and not checked('Z06|Z05|xTexto')
  page.locator('.document-tools summary').click();page.locator('[data-goto="dicionario"]').click();assert page.locator('#view-dicionario').is_visible();page.locator('#searchDict').fill('Z06');assert page.locator('#dictionary tbody tr').count()==2;page.locator('#view-dicionario .document-back').click()
  page.locator('[data-document="nf3e"]').click();assert page.locator('#view-pending').is_visible();assert page.locator('[data-view="impressao"]').is_disabled();assert not page.locator('#view-moc').is_visible()
  choose_doc('nfe');assert checked('W03');assert not page.locator('#mocTables [data-moc-print="W16"]').is_checked()
  choose_doc('dce');page.locator('#groupMoc').select_option('W');page.locator('#searchMoc').fill('');assert checked('W16')
  page.locator('#view-moc [data-select-command=clear]').click();page.locator('#groupMoc').select_option('C');page.locator('[data-moc-descendants="C01"]').click();pdf('DC-e-emitente',['enderEmit','CNPJ','CPF','DC-e'],['ICMSTot','IBSCBSTot']);choose_doc('dce');page.locator('[data-view="oracle"]').click();assert 'DC_DOCUMENTO' in page.locator('#oracleEntities').inner_text();assert 'NF_DOCUMENTO' not in page.locator('#oracleEntities').inner_text()
  assert not errors,errors
  offline=b.new_page();offline.on('pageerror',lambda e:errors.append(str(e)));offline.set_content((R/'public/EXPLORADOR_OFFLINE_COMPLETO.html').read_text().replace('normalize(data);fetchServer();','normalize(data);'),wait_until='load');offline.locator('[data-document="dce"]').click();assert '111' in offline.locator('#mocCount').inner_text();assert not errors,errors;b.close()
 print('Testes de navegação, isolamento, PDF e offline aprovados.',flush=True)
if __name__=='__main__':run()
