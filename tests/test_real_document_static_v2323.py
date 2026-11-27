"""Exercise asynchronous catalog loading with exact static files, via injected fetch responses. No remote HTTP validation."""
from pathlib import Path
from playwright.sync_api import sync_playwright
import json,shutil,mimetypes,re
R=Path(__file__).resolve().parents[1]/'public'
def run():
    with sync_playwright() as pw:
     b=pw.chromium.launch(executable_path=shutil.which('chromium'),args=['--no-sandbox']);p=b.new_page(viewport={'width':1500,'height':900});err=[];p.on('pageerror',lambda e:err.append(str(e)))
     html=(R/'index.html').read_text();html=re.sub(r'<link rel="stylesheet" href="\./styles\.css(?:\?[^"]*)?">',lambda _: '<style>'+(R/'styles.css').read_text()+'</style>',html)
     for name in ('documents.js','selection.js','diagram-state.js','pdf-export.js','app.js'):
      html=re.sub(r'<script src="\./'+re.escape(name)+r'(?:\?[^"]*)?"></script>',lambda _: '<script>'+(R/name).read_text().replace('</script','<\\/script')+'</script>',html)
     assets={str(f.relative_to(R)):json.loads(f.read_text()) for f in (R/'data').rglob('*.json')};payload=json.dumps(assets).replace('<','\\u003c');html=html.replace('</head>','<script>const qaAssets='+payload+';window.fetch=async u=>{const k=String(u).replace(/^\\.\\//,"");return qaAssets[k]?new Response(JSON.stringify(qaAssets[k]),{headers:{"Content-Type":"application/json"}}):new Response("not found",{status:404})};</script></head>');p.set_content(html,wait_until='load');p.wait_for_function('document.querySelector("#mocCount").textContent.includes("1173")')
     fam={'cteos':'cte','gtve':'cte','bpetm':'bpe','bpeta':'bpe'}
     for f in sorted(R.glob('data/*/catalogo_atual.json')):
      d=f.parent.name;c=json.loads(f.read_text());n=len(c['nodes']);g=fam.get(d,d);p.locator(f'[data-document="{g}"]').click()
      if d!=g:p.locator('#documentVariant').select_option(d)
      p.wait_for_function('n=>document.querySelector("#view-moc").classList.contains("active")&&document.querySelector("#mocCount").textContent.includes("de "+n+" registros")',arg=n)
      print(d,n,'HTTP assets OK',flush=True)
     p.locator('[data-document="nfe"]').click();p.set_viewport_size({'width':390,'height':844});assert p.locator('#view-moc').is_visible();assert not err,err;b.close()
if __name__=="__main__":run()
