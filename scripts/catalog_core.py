"""Extração MOC, versionamento transacional e comparação de catálogos.
Dados oficiais só são marcados como verificados após extração bem-sucedida.
"""
from __future__ import annotations
import hashlib
import json
import re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from bs4 import BeautifulSoup

HEADERS = ['#','ID','Campo','Descrição','Ele','Pai','Tipo','Ocor.','Tam.','Observação']
OFFICIAL_URL = 'https://moc.sped.fazenda.pr.gov.br/NFe_NFCe/Leiaute.html'

def now_utc(): return datetime.now(timezone.utc).isoformat(timespec='seconds')

def canonical(o): return json.dumps(o, ensure_ascii=False, sort_keys=True, separators=(',',':'))

def digest(o): return hashlib.sha256(canonical(o).encode('utf8')).hexdigest()

def text_of(cell):
    # preserve long observations and line breaks, but normalize insignificant whitespace
    for br in cell.find_all('br'): br.replace_with('\n')
    for p in cell.find_all(['p','li']): p.insert_before('\n')
    val=cell.get_text(' ',strip=False).replace('\xa0',' ')
    return re.sub(r'\n\s*\n+', '\n', re.sub(r'[ \t]+',' ',val)).strip()

def is_group_title(txt):
    m=re.match(r'^Grupo\s+([A-Z]{1,3}\d*[a-z]?)\s*[.\-–:]\s*(.*)$',txt,re.I)
    return m

def parse_moc(html_text: str, url: str=OFFICIAL_URL):
    """Extrai tabelas do MOC com as dez colunas; sem inventar atributos ausentes."""
    if len(html_text) > 25_000_000: raise ValueError('HTML excede limite de 25 MB')
    soup=BeautifulSoup(html_text,'lxml')
    alltext=soup.get_text(' ',strip=True)
    m=re.search(r'Atualizado\s+até\s+a\s+(NT\s+[\d.]+\s*v[.]?\s*[\d.]+).*?publicada\s+em\s+(\d{2}/\d{2}/\d{4})',alltext,re.I)
    note=m.group(1).strip() if m else None
    publication=m.group(2) if m else None
    rows=[]; groups=[]; group=None; table_count=0
    for element in soup.find_all(['h1','h2','h3','h4','h5','h6','p','div','section','table']):
        if element.name != 'table':
            # do not take parent divs with enormous descendant text
            if element.find(['table','h1','h2','h3','h4','h5','h6']): continue
            txt=element.get_text(' ',strip=True)
            if len(txt)>230:continue
            mg=is_group_title(txt)
            if mg:
                grp,desc=mg.groups();group=grp
                if not any(g['id']==grp for g in groups):groups.append({'id':grp,'description':desc,'order':len(groups)+1})
            continue
        trs=element.find_all('tr')
        if not trs:continue
        # a table must contain the official header, which may be th or td
        first=[]
        for tr in trs[:4]:
            h=[text_of(c) for c in tr.find_all(['td','th'],recursive=False)]
            if ('ID' in h and 'Campo' in h and any('Ocor' in k for k in h)):
                first=h;break
        if not first:continue
        table_count+=1
        for tr in trs:
            cells=tr.find_all(['td','th'],recursive=False)
            if len(cells)<10:continue
            vals=[text_of(c) for c in cells[:10]]
            order,idv,field,desc,ele,pai,typ,ocor,tam,obs=vals
            if not idv or (idv=='ID' and field=='Campo') or order.startswith('---'):continue
            if not re.match(r'^(\d+[a-z]?(?:\.\d+[a-z]?)?|0|-)$',order,re.I):continue
            # ID may be '-' for the root NFe: keep a stable synthetic key only for tree-linking
            key=idv if idv!='-' else 'ROOT'
            row={
                'id':key, 'officialId':idv,'order':order,'tag':field,'description':desc,
                'kind':ele,'parent':pai,'type':typ,'occur':ocor,'length':tam,
                'observation':obs,'mocGroup':group,'source':url
            }
            rows.append(row)
    if not rows: raise ValueError('Nenhuma tabela oficial de dez colunas encontrada. Preservada a versão anterior.')
    # Distinguish duplicate official IDs without pretending there is a canonical unique ID
    byid=Counter(r['id'] for r in rows)
    seen=Counter()
    for r in rows:
        if byid[r['id']]>1:
            seen[r['id']]+=1
            r['key']=f"{r['id']}|{r['parent']}|{seen[r['id']]}"
            r['idCollision']=True
        else:r['key']=r['id']
    return {
      'metadata':{'title':'Leiaute da NF-e e NFC-e — extração do MOC','source':url,
                  'status':'official-html-extracted-unverified-xsd',
                  'extractedAt':now_utc(),'technicalNote':note,'publicationDate':publication,
                  'totalRows':len(rows),'tableCount':table_count,'coverage':'MOC HTML — tabelas encontradas; XSD requer validação separada'},
      'groups':groups,'nodes':rows
    }

def quality_gate(new,old=None,min_rows=350,min_ratio=.70):
    nodes=new.get('nodes') or []
    if len(nodes)<min_rows:raise ValueError(f'Extração incompleta: {len(nodes)} linhas, mínimo {min_rows}. Versão anterior preservada.')
    ids={r.get('id') for r in nodes}
    if len(ids)<int(len(nodes)*.65):raise ValueError('Identificadores inválidos/repetidos: revisar origem')
    if old and old.get('metadata',{}).get('status','').startswith('official'):
        if len(nodes)<len(old.get('nodes',[]))*min_ratio:
            raise ValueError('Redução inesperada de registros. Atualização bloqueada para proteger histórico.')
    for required in ['infNFe','ide','emit','dest','det','imposto','total','IBSCBS']:
        if not any(n.get('tag')==required for n in nodes):
            raise ValueError(f'Campo estrutural {required} ausente: extração não aprovada')
    return True

def comparable(node):
    return {k:node.get(k,'') for k in ('order','officialId','tag','description','kind','parent','type','occur','length','observation','mocGroup')}

def diff_catalogs(old,new):
    a={x['key']:comparable(x) for x in old.get('nodes',[]) if x.get('key')}
    b={x['key']:comparable(x) for x in new.get('nodes',[]) if x.get('key')}
    out=[]
    for key in sorted(set(a)|set(b)):
        if key not in a:out.append({'id':key,'status':'incluído','new':b[key]})
        elif key not in b:out.append({'id':key,'status':'excluído','old':a[key]})
        elif a[key]!=b[key]:
            changes={field:{'before':a[key].get(field,''),'after':b[key].get(field,'')}
                     for field in a[key] if a[key].get(field,'')!=b[key].get(field,'')}
            out.append({'id':key,'status':'alterado','changes':changes})
    return out

def atomic_json(path,obj):
    path=Path(path); path.parent.mkdir(parents=True,exist_ok=True)
    target=path.with_suffix(path.suffix+'.tmp')
    with open(target,'w',encoding='utf-8') as f:
        json.dump(obj,f,ensure_ascii=False,indent=2)
        f.flush(); import os; os.fsync(f.fileno())
    target.replace(path)
