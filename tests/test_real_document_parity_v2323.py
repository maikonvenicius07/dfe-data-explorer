"""Real catalogs from the supplied ZIP. Requires Playwright, Chromium and PyMuPDF."""
from pathlib import Path
import os,json,shutil,tempfile
import fitz
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1]; Q=Path(os.environ.get('DFE_QA_DIR',tempfile.mkdtemp()));Q.mkdir(parents=True,exist_ok=True)
def run():
    cats={'nfe':json.loads((R/'public/data/catalogo_atual.json').read_text())}
    cats.update({p.parent.name:json.loads(p.read_text()) for p in (R/'public/data').glob('*/catalogo_atual.json')})
    families={'cteos':'cte','gtve':'cte','bpetm':'bpe','bpeta':'bpe'}
    with sync_playwright() as pw:
        b=pw.chromium.launch(executable_path=shutil.which('chromium'),args=['--no-sandbox']);p=b.new_page(accept_downloads=True,viewport={'width':1550,'height':950});p.set_default_timeout(15000);errors=[];p.on('pageerror',lambda e:errors.append(str(e)))
        html=(R/'public/EXPLORADOR_OFFLINE_COMPLETO.html').read_text().replace('normalize(data);fetchServer();','normalize(data);');p.set_content(html,wait_until='load',timeout=60000)
        def switch(doc):
            fam=families.get(doc,doc);p.locator(f'[data-document="{fam}"]').click()
            if doc!=fam:p.locator('#documentVariant').select_option(doc)
            p.wait_for_function('n=>document.querySelector("#mocCount").textContent.includes("de "+n+" registros")',arg=len(cats[doc]['nodes']))
        def clear():
            btn=p.locator('#view-moc [data-select-command=clear]')
            if btn.is_enabled():btn.click()
        def pdf(doc,orientation='landscape'):
            p.locator('#mocPrintSelected').click();p.locator('#pageOrient').select_option(orientation)
            expected=p.locator('#printDocument [data-integrated-section="moc"] tr[data-key]').count();assert expected>0
            with p.expect_download(timeout=30000) as dl:p.locator('#btnDownloadPdf').click()
            out=Q/(doc+'.pdf');dl.value.save_as(out)
            with fitz.open(out) as f:
                assert 'V2.3.23' in ''.join(x.get_text() for x in f);assert all(x.rotation==0 and (x.rect.width>x.rect.height)==(orientation=='landscape') for x in f)
                f[0].get_pixmap().save(Q/(doc+'.png'))
                return len(f),expected
        for doc in ['nfe','dce','cte','cteos','gtve','abi','nfgas','nfag','nf3e','nfcom','bpe','bpetm','bpeta','mdfe']:
            switch(doc);clear();p.locator('#collapseMoc').click();assert p.locator('#mocTables [data-moc-print]:checked').count()==0
            button=p.locator('#mocTables [data-moc-toggle]').first;key=button.get_attribute('data-moc-toggle');group=button.evaluate('(e)=>e.closest("article").dataset.group')
            p.locator('#groupMoc').select_option(group);button=p.locator(f'[data-moc-toggle="{key}"]');button.click();assert p.locator(f'[data-moc-print="{key}"]').is_checked();count=p.locator('#mocTables [data-moc-print]:checked').count();assert count>=2,(doc,count)
            button.click();assert p.locator(f'[data-moc-print="{key}"]').is_checked();button.click();assert p.locator('#mocTables [data-moc-print]:checked').count()==count
            p.locator('#expandMoc').click();assert p.locator('#mocTables [data-moc-print]:checked').count()==count
            branch=p.locator(f'[data-moc-descendants="{key}"]');branch.click()
            if branch.inner_text().startswith('−'):branch.click()
            clear();p.locator('#collapseMoc').click();p.locator(f'[data-moc-toggle="{key}"]').click();pages,expected=pdf(doc);assert expected==count,(doc,expected,count)
            print(doc,len(cats[doc]['nodes']),count,pages,'OK',flush=True)
        switch('nfe');assert p.locator('#mocTables [data-moc-print]:checked').count()>0
        clear();p.locator('#groupMoc').select_option('W');p.locator('#expandMoc').click()
        for k in 'W01 W01a W02 W17 W23 W31 W34 W35 W36 W37 W42 W43 W44 W46 W47 W48 W49 W50 W57 W59e W59h W60'.split():p.locator(f'[data-moc-print="{k}"]').check()
        pages,expected=pdf('nfe-W22','portrait');assert pages==1 and expected==22
        assert not errors,errors; print('NF-e W22 OK; erros JS: 0',flush=True);b.close()
if __name__=='__main__':run()
