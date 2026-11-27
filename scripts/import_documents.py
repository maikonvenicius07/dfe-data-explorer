"""Importação rastreável de tabelas LEIAUTE. Não usa páginas Visão Geral.
Executar com acesso à rede ou --html-dir contendo <documento>.html.
Não valida XSD. Tabelas e vínculos não resolvidos são registrados explicitamente.
"""
from pathlib import Path
from collections import Counter, defaultdict
from urllib.request import Request, urlopen
import argparse, hashlib, json, re, subprocess, sys, unicodedata
from bs4 import BeautifulSoup
from catalog_core import atomic_json, now_utc, digest, text_of
from import_dce import extract as extract_dce
ROOT=Path(__file__).resolve().parents[1]
BASE='https://moc.sped.fazenda.pr.gov.br/'
SOURCES={'dce':('DC-e','DCe','DCe'),'cte':('CT-e','CTe','infCte'),'cteos':('CT-e OS','CTe','infCte'),'gtve':('GTVe','CTe','infCte'),'abi':('NF-e ABI','NFe_ABI','NFeABI'),'nfgas':('NFGAS','NFGAS','infNFGas'),'nfag':('NFAG','NFAG','infNFAg'),'nf3e':('NF3-e','NF3e','infNF3e'),'nfcom':('NFCom','NFCom','infNFCom'),'bpe':('BP-e','BPe','infBPe'),'bpetm':('BP-e TM','BPe','infBPe'),'bpeta':('BP-e TA','BPe','infBPe'),'mdfe':('MDF-e','MDFe','infMDFe')}
BLANK={'','-','–','—','raiz','n/a'}

def url(doc): return BASE+SOURCES[doc][1]+'/Leiaute.html'
def canon(s): return re.sub(r'[^a-z0-9#]','',unicodedata.normalize('NFKD',s).encode('ascii','ignore').decode().lower())
def col(s):
    s=canon(s)
    return {'#':'order','id':'officialId','campo':'tag','tag':'tag','nivel':'level','descricao':'description','descricaoobservacao':'description','observacaodescricao':'description','ele':'kind','elemento':'kind','pai':'officialParent','tipo':'type','ocor':'occur','ocorr':'occur','ocorrencia':'occur','tam':'length','tamanho':'length','dominio':'domain','expreg':'regex','expressaoregular':'regex','observacao':'observation','observacoes':'observation'}.get(s,s)
def section_num(s):
    m=re.match(r'\s*(\d+)(?:\.|\s|$)',s);return int(m[1]) if m else None

def table_rows(table):
    """Expand HTML spans deterministically; retain original active/struck text."""
    grid={}; out=[]
    for i,tr in enumerate(table.find_all('tr')):
        if tr.find_parent('table') is not table:continue
        j=0
        for c in tr.find_all(['td','th'],recursive=False):
            while (i,j) in grid:j+=1
            # Preserve historical wording separately; current value excludes struck text.
            raw=c.get_text(' ',strip=True)
            copy=BeautifulSoup(str(c),'lxml')
            for old in copy.select('del,s,strike'):old.decompose()
            val=text_of(copy)
            rs,cs=int(c.get('rowspan',1)),int(c.get('colspan',1))
            if not (1<=rs<=1000 and 1<=cs<=30):raise ValueError('Span HTML inválido')
            for a in range(rs):
                for b in range(cs):
                    if (i+a,j+b) in grid:raise ValueError('Sobreposição de células')
                    grid[i+a,j+b]=(val,raw)
            j+=cs
        idx=[b for a,b in grid if a==i]
        if idx:out.append([grid.get((i,b),('','')) for b in range(max(idx)+1)])
    return out

def extract(doc,html):
    if len(html)>25_000_000:raise ValueError('HTML excessivo')
    if doc=='dce':return extract_dce(html)
    label,folder,root_tag=SOURCES[doc]; soup=BeautifulSoup(html,'lxml')
    # The actual page title and expected root prevent importing a different manual.
    title=soup.title.get_text(' ',strip=True) if soup.title else ''
    if 'leiaute' not in canon(title+' '+ ' '.join(h.get_text(' ',strip=True) for h in soup.find_all('h1'))):raise ValueError('Página não identificada como Leiaute')
    heading={};rows=[];tables=[];skipped=[];warnings=[];groups={};stacks=defaultdict(dict);id_lists=defaultdict(list);scoped_rows=defaultdict(list);wrappers={};recognized=0
    for el in soup.find_all(['h1','h2','h3','h4','h5','h6','table']):
        if el.name!='table':
            n=int(el.name[1]); heading={k:v for k,v in heading.items() if k<n};heading[n]=el.get_text(' ',strip=True);continue
        h2=heading.get(2,''); major=section_num(h2); path=' / '.join(v for k,v in sorted(heading.items()) if k>=2); path=path or 'Leiaute'
        if doc in ('cte','cteos','gtve') and major not in {'cte':{2,3},'cteos':{4},'gtve':{5}}[doc]:continue
        if doc in ('bpe','bpetm','bpeta') and major!={'bpe':2,'bpetm':3,'bpeta':4}[doc]:continue
        raw=table_rows(el); header_idx=None; names=None
        for j,r in enumerate(raw):
            cols=[col(x[0]) for x in r]
            if {'tag','description','kind'}.issubset(cols) and ('level' in cols or 'officialParent' in cols):header_idx=j;names=cols;break
        if names is None:
            if raw:skipped.append({'section':path,'header':[x[0] for x in raw[0]],'rows':max(0,len(raw)-1)})
            continue
        if len(set(names))!=len(names):raise ValueError('Cabeçalho ambíguo: '+path)
        # Level tables for a modal/variant can start again at 0; each main section is isolated.
        # For explicit ID tables the main section holds cross-group references.
        scope=(h2 if major is not None else 'principal') if 'level' in names else (h2 if major and major>1 else 'principal')
        if doc=='cte' and major==3:scope=path
        if doc=='cte' and major==2 and ('simplificado' in canon(path) or 'evento' in canon(path)):scope=path
        table_id=len(tables)+1;count=0
        for ri,r in enumerate(raw[header_idx+1:],header_idx+2):
            if not any(x[0] for x in r):continue
            if [col(x[0]) for x in r]==names:continue
            if len(r)!=len(names):raise ValueError(f'Tabela {table_id}, linha {ri}: {len(r)} colunas, esperado {len(names)}')
            fields=dict(zip(names,(x[0] for x in r)));original=dict(zip(names,(x[1] for x in r)))
            if not fields['tag'] and not fields.get('description'):raise ValueError(f'Campo e descrição vazios na tabela {table_id}, linha {ri}')
            recognized+=1;count+=1;tag=fields['tag'];oid=fields.get('officialId','');level=fields.get('level','');parent_label=fields.get('officialParent','')
            mapped_tag=not tag and bool(re.fullmatch(r'[A-Za-z_][\w.-]*:[A-Za-z_][\w.-]*',fields.get('description','')))
            tag=tag or (fields['description'] if mapped_tag else '—')
            marker=bool(re.fullmatch(r'[-–—\s]+[xX][-–—\s]+',tag)) or 'sequenciaxml'==canon(fields.get('description',''))
            # Internal key is not an official ID. Keep all original columns separately.
            # Scope+table+row disambiguates repeated IDs and numbering between modals/variants.
            key=f'{doc}:t{table_id}:r{ri}'; kind=fields['kind']; p=None; issue=None; wrapper=False
            if 'level' in names:
                stack=stacks[scope]; match=re.fullmatch(r'\d+',level.strip())
                if canon(level)=='raiz':
                    dep=None;wrapper=True
                elif marker:
                    dep=None # source sequence separator is not an XML ancestor
                elif match:
                    dep=int(level); p=stack.get(dep-1) if dep else wrappers.get(scope)
                    if dep and p is None:issue='Nível sem ancestral anterior na seção'
                    if p and p['kind'] not in ('G','CG','SG','CE','ES','') and not p.get('sourceRootWrapper'):issue='Nível aponta para registro não estrutural';p=None
                    if p and parent_label.lower() not in BLANK and parent_label!=p['tag'] and parent_label!=p.get('officialId'):issue='Pai declarado diverge do nível';p=None
                    for d in list(stack):
                        if d>=dep:del stack[d]
                else:dep=None;issue='Nível não numérico na fonte'
            else:dep=None
            group=path if 'level' in names else scope
            # Editorial groups retain the entire branch for numeric-level manuals.
            # Main explicit-ID manual uses ID prefixes just to label editorial groups (not for parent resolution).
            if 'level' not in names and doc=='abi' and scope=='principal':
                m=re.match(r'[A-Z]+',oid);group=m[0] if m else 'Raiz'
            if group not in groups:groups[group]=f'S{len(groups)+1:02}' if len(group)>12 else group
            obs=fields.get('observation','')
            extra=[f'{name}: {fields.get(k)}' for k,name in [('domain','Domínio'),('regex','Exp. Reg.')] if fields.get(k)]
            if extra:obs=' · '.join(([obs] if obs else [])+extra)
            row=dict(id=key,key=key,officialId=oid or '—',order=fields.get('order',''),tag=tag,description=fields.get('description',''),kind=kind,parent=p['id'] if p else None,officialParent=parent_label or (p['tag'] if p else '—'),type=fields.get('type',''),occur=fields.get('occur',''),length=fields.get('length',''),observation=obs,mocGroup=groups[group],source=url(doc),sourceSection=path,sourceTable=table_id,sourceRow=ri,sourceLevel=level,original=original,sourceValues=fields)
            if issue:row['hierarchyIssue']=issue
            if not fields['tag'] and not mapped_tag:row['hierarchyIssue']='Campo sem nome na fonte'
            if mapped_tag:row['sourceMapping']='Nome explícito presente na descrição; coluna Campo vazia na fonte'
            if marker:row['nonXmlMarker']=True
            if wrapper:row['sourceRootWrapper']=True;wrappers[scope]=row
            if 'level' in names and dep is not None:stacks[scope][dep]=row
            if 'level' not in names:
                row['_explicit']=True
                if oid and oid not in BLANK:id_lists[(scope,oid)].append(row)
            scoped_rows[scope].append(row);rows.append(row)
        tables.append(dict(number=table_id,section=path,scope=scope,rows=count,columns=names))
    if not rows or not any(r['tag'].casefold()==root_tag.casefold() for r in rows):raise ValueError('Raiz documental não encontrada: '+root_tag)
    for scope,rr in scoped_rows.items():
        root=next((r for r in rr if r['tag'].casefold()==root_tag.casefold()),None)
        for r in rr:
            if r.pop('_explicit',False):
                pp=r['sourceValues'].get('officialParent','')
                if pp.casefold()=='raiz' and root and root is not r:r['parent']=root['id']
                elif pp.casefold() not in BLANK:
                    options=id_lists.get((scope,pp),[])
                    if len(options)==1 and options[0] is not r:r['parent']=options[0]['id']
                    else:
                        # Complementary tables often identify parents by tag, not by ID.
                        # Prefer unique local matches, then unique document-wide matches.
                        candidates=[a for a in rr if a is not r and a['tag']==pp]
                        if not candidates:candidates=[a for a in rows if a is not r and a['tag']==pp]
                        if len(candidates)==1:r['parent']=candidates[0]['id']
                        else:r['hierarchyIssue']='Pai explícito ausente ou ambíguo: '+pp
    lookup={r['id']:r for r in rows}
    for r in rows:
        visited={r['id']};p=r['parent']
        while p:
            if p not in lookup or p in visited:raise ValueError('Ciclo ou pai inexistente: '+r['id'])
            visited.add(p);p=lookup[p]['parent']
        if r.get('hierarchyIssue'):warnings.append({'key':r['key'],'tag':r['tag'],'reason':r['hierarchyIssue']})
        # Do not fabricate an XPath for modal, complement or document wrapper absent from source.
        r['pathUnverified']=True
    # Stable identities from actual ancestry, document, section and source ID. An exact duplicate
    # is distinguished by its occurrence; a later update can flag those for manual review.
    identities=Counter();new_ids={}
    for r in rows:
        chain=[];cur=r
        while cur:
            chain.append(cur['tag']);cur=lookup.get(cur['parent'])
        path='/'.join(reversed(chain));r['sourceHierarchyPath']=path
        raw='|'.join([doc,r['sourceSection'],path,r['officialId']])
        identities[raw]+=1
        new_ids[r['id']]=doc+':'+hashlib.sha256(raw.encode()).hexdigest()[:24]+(':'+str(identities[raw]) if identities[raw]>1 else '')
    for r in rows:
        r['id']=r['key']=new_ids[r['id']];r['parent']=new_ids.get(r['parent'])
    for w in warnings:w['key']=new_ids[w['key']]
    # For one-table manuals, offer meaningful filters by structural branch rather than a
    # single enormous group. Keep modal and complementary sections separate.
    lookup={r['id']:r for r in rows}; original_groups={r['id']:r['mocGroup'] for r in rows};counts=Counter(original_groups.values()); group_labels={v:k for k,v in groups.items()};new_groups={}
    for r in rows:
        g=r['mocGroup'];label=group_labels[g];cur=r;chain=[r]
        while cur['parent'] in lookup and original_groups[cur['parent']]==g:
            cur=lookup[cur['parent']];chain.append(cur)
        if r['sourceLevel']!='' and counts[g]>50 and len(chain)>1:
            branch=chain[-2] if chain[-1]['tag'].lower()==root_tag.lower() and len(chain)>1 else chain[-1]
            label=label+' — '+branch['tag']
        if label not in new_groups:new_groups[label]=f'S{len(new_groups)+1:03}'
        r['mocGroup']=new_groups[label]
    groups=new_groups
    if recognized!=len(rows) or sum(t['rows'] for t in tables)!=len(rows):raise ValueError('Contagem de linhas divergente')
    # Check distinct source sections expected for families; fail rather than publish an empty variant.
    if doc=='mdfe' and not {'rodo','aereo','ferrov','aquav'}.issubset({r['tag'].casefold() for r in rows}):
        # Names vary by schema. Require the four headings, not guessed root tags.
        sec=' '.join(canon(t['section']) for t in tables)
        if not all(s in sec for s in ('rodoviario','aereo','ferroviario','aquaviario')):raise ValueError('Modais MDF-e ausentes')
    coverage='Tabelas reconhecidas da seção Leiaute extraídas; cobertura integral e XSD não certificados. Colunas Domínio/Exp. Reg. preservadas em Observação e JSON. '
    coverage+=f'{len(warnings)} vínculos requerem revisão; {len(skipped)} tabelas não estruturais ou não reconhecidas foram registradas para auditoria.'
    page_text=soup.get_text(' ',strip=True)
    note=re.search(r'Atualizado\s+até\s+a\s+(NT\s+[\d.]+\s*v\.?\s*[\d.]+)([^|]{0,100}?)\s*(?=☰|Leiaute|$)',page_text,re.I)
    meta=dict(documentId=doc,title='Leiaute '+label,source=url(doc),status='official-html-extracted-unverified-xsd',coverage=coverage,extractedAt=now_utc(),sourceHash=hashlib.sha256(html.encode()).hexdigest(),totalRows=len(rows),tableCount=len(tables),hierarchyIssues=len(warnings),tables=tables,unmappedTables=skipped,warnings=warnings,technicalNote=note[1] if note else None,manualReference=note[0] if note else title)
    return dict(metadata=meta,groups=[dict(id=v,description=k,order=i) for i,(k,v) in enumerate(groups.items(),1)],nodes=rows)

def validate_source_coverage(doc,cat):
    """Main manual section checks from observed table structure, not a generic row minimum.
    Supplemental/unknown tables still require review; this is not XSD validation.
    """
    rows=cat['nodes'];meta=cat['metadata'];tables=meta.get('tables',[])
    expected={'nf3e':('1',17),'nfgas':('1',14),'nfag':('1',14),'nfcom':('2',11)}
    if doc in expected:
        prefix,n=expected[doc];sections='\n'.join(t['section'] for t in tables)
        missing=[f'{prefix}.{i}' for i in range(1,n+1) if not re.search(r'(?<![\d.])'+re.escape(f'{prefix}.{i}')+r'(?=\.|\s|$)',sections)]
        if missing:raise ValueError('Seções principais ausentes: '+', '.join(missing))
    if doc=='abi':
        tags={r['tag'].casefold() for r in rows}
        for tag in ('nfeabi','ide','emit','total'):
            if tag not in tags:raise ValueError('Grupo principal ausente: '+tag)
    if doc in ('cte','cteos','gtve','bpe','bpetm','bpeta','mdfe'):
        tags={r['tag'].casefold() for r in rows}
        for tag in ('ide','emit'):
            if tag not in tags:raise ValueError('Grupo principal ausente: '+tag)
    meta['sourceCoverageCheck']='Seções principais e raiz reconhecidas; conferência de cobertura e XSD ainda pendentes.'
    return cat

def fetch(doc,html_dir):
    if html_dir:
        f=html_dir/(doc+'.html'); f=f if f.exists() else html_dir/(SOURCES[doc][1]+'.html');return f.read_text(encoding='utf-8-sig')
    req=Request(url(doc),headers={'User-Agent':'DF-e Data Explorer/2.3.21','Accept':'text/html'})
    with urlopen(req,timeout=25) as r:
        if r.geturl().split('?')[0]!=url(doc):raise ValueError('Redirecionamento inesperado')
        raw=r.read(25_000_001);return raw.decode(r.headers.get_content_charset() or 'utf-8',errors='strict')

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--document',choices=['all',*SOURCES],default='all');ap.add_argument('--html-dir',type=Path);args=ap.parse_args()
    report_path=ROOT/'public/data/importacao_documentos.json'
    report=json.loads(report_path.read_text()).get('documents',{}) if report_path.exists() else {}
    html_cache={}; ids=SOURCES if args.document=='all' else [args.document]
    for doc in ids:
        dest=ROOT/'public/data'/doc/'catalogo_atual.json';old=json.loads(dest.read_text()) if dest.exists() else None
        try:
            cache_key=SOURCES[doc][1] if not args.html_dir else doc
            if cache_key not in html_cache:html_cache[cache_key]=fetch(doc,args.html_dir)
            cat=validate_source_coverage(doc,extract(doc,html_cache[cache_key]));meta=cat['metadata']
            if old and len(cat['nodes'])<len(old['nodes']):raise ValueError('Redução de registros: revisão manual obrigatória')
            if old and old['metadata'].get('tableCount') and meta.get('tableCount',0)<old['metadata']['tableCount']:raise ValueError('Redução de tabelas: revisão manual obrigatória')
            if old and isinstance(old['metadata'].get('hierarchyIssues'),int) and (meta.get('hierarchyIssues') or 0)>old['metadata']['hierarchyIssues']:raise ValueError('Aumento de vínculos não resolvidos: revisão manual obrigatória')
            if old and old['metadata'].get('sourceHash')!=meta['sourceHash']:
                atomic_json(ROOT/'data/documents'/doc/'snapshots'/(digest(old)[:16]+'.json'),old)
            if not old or old['metadata'].get('sourceHash')!=meta['sourceHash']:atomic_json(dest,cat)
            report[doc]=dict(status='importado; XSD pendente',source=url(doc),found=len(cat['nodes']),imported=len(cat['nodes']),tables=meta.get('tableCount'),hierarchyIssues=meta.get('hierarchyIssues'))
        except Exception as e:
            report[doc]=dict(status='erro de importação; catálogo anterior preservado',source=url(doc),error=str(e),imported=len(old['nodes']) if old else 0)
        print(doc,report[doc],flush=True)
    atomic_json(ROOT/'public/data/importacao_documentos.json',{'checkedAt':now_utc(),'documents':report})
    subprocess.run([sys.executable,str(ROOT/'scripts/build_document_registry.py')],check=True)
    subprocess.run([sys.executable,str(ROOT/'scripts/build_offline.py')],check=True)
    if any(report[d]['status'].startswith('erro') for d in ids):return 1
    return 0
if __name__=='__main__':sys.exit(main())
