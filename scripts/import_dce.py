"""Importa o leiaute DC-e do manual HTML; nunca substitui NF-e/NFC-e.
Uso: python scripts/import_dce.py [--html arquivo_salvo.html]
A fonte consolidada é material de apoio; XSD e NT originais devem ser conferidos separadamente.
"""
from pathlib import Path
from collections import Counter
from urllib.request import Request, urlopen
import argparse, json, re
from bs4 import BeautifulSoup
from catalog_core import atomic_json, text_of, now_utc, digest

ROOT=Path(__file__).resolve().parents[1]
URL='https://moc.sped.fazenda.pr.gov.br/DCe/Leiaute.html'
DEST=ROOT/'public/data/dce/catalogo_atual.json'
GROUPS=set('A B C D E F H I V W X Z ZA ZB ZX ZZ'.split())
HEAD=['#','ID','Campo','Descrição','Ele','Pai','Tipo','Ocor.','Tam.','Observação']

def extract(html, old=None):
    if len(html)>25_000_000: raise ValueError('HTML excessivamente grande')
    soup=BeautifulSoup(html,'lxml'); rows=[]; groups={}; group='A'; tables=0
    for e in soup.find_all(['h2','h3','h4','table']):
        if e.name!='table':
            m=re.match(r'^Grupo\s+([A-Z]+)\s*[.\-–:]\s*(.+)$',e.get_text(' ',strip=True),re.I)
            if m:
                group=m[1].upper(); groups[group]=m[2]
            continue
        trs=e.find_all('tr'); headings=False
        for tr in trs:
            cells=tr.find_all(['th','td'],recursive=False)
            vals=[text_of(c) for c in cells]
            if vals==HEAD: headings=True; tables+=1; continue
            if not headings: continue
            if len(vals)!=10: raise ValueError(f'Linha inesperada em tabela {group}: {len(vals)} colunas')
            order,i,tag,desc,kind,parent,typ,occ,size,obs=vals
            if not re.fullmatch(r'\d+[a-z]?(?:\.\d+[a-z]?)?',order,re.I) or not tag: raise ValueError(f'Linha sem identificação válida: {order!r}')
            root=order=='0' and tag=='DCe' and i in ['-','–','—','']
            if not root and not i: raise ValueError('ID vazio')
            rows.append(dict(id='ROOT' if root else i,officialId=i,order=order,tag=tag,description=desc,kind=kind,parent=parent,type=typ,occur=occ,length=size,observation=obs,mocGroup='A' if root else group,source=URL))
    ids=Counter(r['id'] for r in rows); keys=set()
    for r in rows:
        r['key']=r['id'] if ids[r['id']]==1 else '|'.join([r['id'],r['parent'],r['tag']]);r['idCollision']=ids[r['id']]>1
        if r['key'] in keys:raise ValueError('Colisão de chave: '+r['key'])
        keys.add(r['key'])
        if r['parent'] not in ('','-','–','—','Raiz') and ids[r['parent']]!=1:raise ValueError('Pai ausente ou ambíguo: '+r['parent'])
    if len(rows)<111 or not GROUPS.issubset({r['mocGroup'] for r in rows}):raise ValueError('Cobertura inferior ao piloto: revisão manual necessária')
    required={'DCe','infDCe','ide','emit','dest','det','prod','total','vDC','infDCeSupl','Signature'}
    if not required.issubset({r['tag'] for r in rows}) or ids['ROOT']!=1:raise ValueError('Estrutura DC-e não reconhecida')
    if old and len(rows)<len(old.get('nodes',[])):raise ValueError('Redução inesperada; versão anterior preservada')
    text=soup.get_text(' ',strip=True)
    note=re.search(r'Atualizado\s+até\s+a\s+(NT\s+[\d.]+\s*v\.?\s*[\d.]+).*?publicada\s+em\s+([\w/]+(?:\s+de\s+\d{4})?)',text,re.I)
    metadata=dict(documentId='dce',title='Leiaute DC-e — extração HTML',source=URL,status='official-html-extracted-unverified-xsd',extractedAt=now_utc(),technicalNote=note[1] if note else None,publicationDate=note[2] if note else None,totalRows=len(rows),tableCount=tables,coverage='Tabelas de leiaute do MOC on-line importadas. Pacote XSD, NT originais e regras condicionais ainda requerem validação.',sourceHash=digest(rows))
    return dict(metadata=metadata,groups=[dict(id=g,description=v,order=i) for i,(g,v) in enumerate(groups.items(),1)],nodes=rows)

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--html',type=Path);args=parser.parse_args()
    if args.html:html=args.html.read_text(encoding='utf8')
    else:
        req=Request(URL,headers={'User-Agent':'DF-e Data Explorer/2.3.20','Accept':'text/html'})
        with urlopen(req,timeout=30) as r:
            if r.geturl().split('?')[0]!=URL: raise ValueError('Redirecionamento inesperado')
            raw=r.read(25_000_001);html=raw.decode(r.headers.get_content_charset() or 'utf-8',errors='strict')
    old=json.loads(DEST.read_text(encoding='utf8'));new=extract(html,old)
    if old['metadata'].get('sourceHash')==new['metadata']['sourceHash']:
        print('DC-e sem alterações');return
    snapshots=ROOT/'data/documents/dce/snapshots'
    atomic_json(snapshots/(now_utc().replace(':','-')+'-'+digest(old)[:10]+'.json'),old)
    atomic_json(DEST,new)
    # Atualiza a base offline da mesma versão; o código não duplica o motor.
    index=ROOT/'public/index.html';s=index.read_text(encoding='utf8');blob=json.dumps(new,ensure_ascii=False).replace('<','\\u003c')
    s,n=re.subn(r'(<script id="dceSeed" type="application/json">).*?(</script>)',lambda m:m[1]+blob+m[2],s,flags=re.S)
    if n!=1:raise ValueError('Seed DC-e não localizado no HTML')
    index.write_text(s,encoding='utf8')
    import subprocess,sys
    subprocess.run([sys.executable,str(ROOT/'scripts/build_offline.py')],check=True)
    print(f'DC-e: {len(new["nodes"])} registros importados; XSD não validado.')
if __name__=='__main__':main()
