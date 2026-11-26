"""Regression: shared MOC hierarchy, exact selected rows, PDF depth and repeated headers."""
from pathlib import Path
from playwright.sync_api import sync_playwright
import re, os, shutil, tempfile, fitz
ROOT=Path(__file__).resolve().parents[1]
UF=['W36','W37','W38','W39','W41']
MUN=['W36','W42','W43','W44','W46']
BOTH=['W36','W37','W38','W39','W41','W42','W43','W44','W46','W47','W48','W49']

def run(out):
    out.mkdir(parents=True,exist_ok=True)
    with sync_playwright() as p:
        browser=p.chromium.launch(headless=True,executable_path=os.environ.get('CHROMIUM_PATH') or shutil.which('chromium'),args=['--no-sandbox'])
        for mode in ('static','offline'):
            page=browser.new_page(viewport={'width':1600,'height':1000},accept_downloads=True)
            page.set_default_timeout(15000);errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
            html=(ROOT/'public/EXPLORADOR_OFFLINE_COMPLETO.html').read_text()
            if mode=='static':
                catalog=(ROOT/'public/data/catalogo_atual.json').read_text()
                html=re.sub(r'(<script id="seedData" type="application/json">).*?(</script>)',lambda m:m[1]+catalog+m[2],html,count=1,flags=re.S)
            page.set_content(html,wait_until='load')
            def choose(keys,groups=('W',)):
                page.locator('[data-view="moc"]').click()
                if page.locator('#view-moc [data-select-command=clear]').is_enabled():page.locator('#view-moc [data-select-command=clear]').click()
                expected=[]
                for g in groups:
                    page.locator('#groupMoc').select_option(g);page.locator('#expandMoc').click()
                    rows=page.locator('#mocTables tr[data-key]').evaluate_all('(es)=>es.map(e=>[e.dataset.key,Number(e.dataset.depth),e.dataset.kind])')
                    wanted=[r for r in rows if r[0] in keys] if keys else rows
                    expected.extend(wanted)
                    if keys:
                        for k,_,_ in wanted:page.locator(f'[data-moc-print="{k}"]').check()
                    else:page.locator('#mocSelectFiltered').click()
                page.locator('#mocPrintSelected').click()
                for root in ('#printDocument','#printPreviewRender'):
                    got=page.locator(root+' tr[data-key]').evaluate_all('(es)=>es.map(e=>[e.dataset.key,Number(e.dataset.depth),e.dataset.kind])')
                    assert got==expected,(got,expected)
                    assert page.locator(root+' thead th').first.is_visible() if root=='#printPreviewRender' else True
                    assert all(n==10 for n in page.locator(root+' .moc-table').evaluate_all('(es)=>es.map(e=>e.querySelectorAll("thead th").length)'))
                assert page.locator('#printDocument [data-preview-remove]').count()==0
                return expected
            def pdf(name,paper='A4',orientation='landscape',via='direct',check=None):
                page.locator('#pageSize').select_option(paper);page.locator('#pageOrient').select_option(orientation)
                path=out/(name+'.pdf')
                if via=='direct':
                    with page.expect_download() as dl:page.locator('#btnDownloadPdf').click()
                    dl.value.save_as(path)
                else:page.pdf(path=str(path),print_background=True,prefer_css_page_size=True)
                with fitz.open(path) as d:
                    assert len(d)>0
                    for pg in d:
                        assert pg.rotation==0 and (pg.rect.width>pg.rect.height)==(orientation=='landscape')
                        assert all(w[0]>=0 and w[2]<=pg.rect.width+1 and w[1]>=0 and w[3]<=pg.rect.height+1 for w in pg.get_text('words'))
                    if check:check(d)
                    print(name,len(d),'páginas',flush=True)
                return path
            def check_branches(d,expected,absent):
                text='\n'.join(pg.get_text() for pg in d)
                for k in expected:assert re.search(r'(?<!\w)'+re.escape(k)+r'(?!\w)',text),k
                # IDs may legitimately appear in Pai; test omitted siblings that cannot be parents of selected nodes.
                for k in absent:assert not re.search(r'(?<!\w)'+re.escape(k)+r'(?!\w)',text),k
                pg=d[0];positions={tag:pg.search_for(tag)[0].x0 for tag in ['gIBS','gIBSUF' if 'W37' in expected else 'gIBSMun','vDif']}
                assert positions['gIBS']<positions['gIBSUF' if 'W37' in expected else 'gIBSMun']<positions['vDif'],positions
                assert 'Grupo W' in text
                assert 'Diagrama XML' not in text
            for keys,name,absent in [(UF,'UF',['W42','W43','W44','W46']),(MUN,'MUN',['W37','W38','W39','W41'])]:
                if mode=='offline' and name=='MUN':continue
                choose(keys)
                if mode=='static':assert page.locator('#printDocument tr[data-key]').count()==5
                else:assert page.locator('#printDocument tr[data-key]').count()>=4
                if mode=='static':
                    for via in ('direct','browser'):
                        pdf(f'{mode}_{name}_{via}',via=via,check=lambda d:check_branches(d,keys,absent))
                else:pdf('offline_UF',check=lambda d:check_branches(d,[k for k in keys if k!='W41'],absent))
            if mode=='static':
                choose(BOTH)
                pdf('W_IBS_A4',check=lambda d:check_branches(d,BOTH,['W35','W50']))
                pdf('W_IBS_A3','A3',check=lambda d:check_branches(d,BOTH,['W35','W50']))
                pdf('W_IBS_retrato','A4','portrait')
                page.locator('#printColor').select_option('bw');pdf('W_IBS_PB');page.locator('#printColor').select_option('color')
                # Missing intermediates must not flatten original depths.
                choose(['W38','W47']);assert page.locator('#printDocument tr[data-key="W38"]').get_attribute('data-depth')=='4'
                assert page.locator('#printDocument tr[data-key="W47"]').get_attribute('data-depth')=='3'
                # Simple group and cross-group selection.
                choose(['A02','A03'],('A',));pdf('A_simples')
                choose(['B02','W38'],('B','W'));pdf('B_W')
                page.locator('#printPreviewRender [data-preview-remove="B02"]').click();assert page.locator('#printDocument tr[data-key]').count()==1
                page.locator('[data-print-col="0"]').uncheck();assert page.locator('#printDocument thead th').count()==9
                page.locator('[data-print-col="0"]').check()
                choose([],('W',))
                def multiple(d):
                    assert len(d)>1
                    for pg in d:assert 'Grupo W' in pg.get_text() and 'Campo' in pg.get_text(),pg.get_text()[:200]
                pdf('W_completo_A4',check=multiple);pdf('W_completo_navegador',via='browser',check=multiple)
            assert not errors,errors
            page.close()
        browser.close()
if __name__=='__main__':
    with tempfile.TemporaryDirectory() as tmp:run(Path(os.environ.get('DFE_QA_DIR',tmp)))
