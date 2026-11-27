"""Monitor independente de publicações XSD. Não modifica nenhum catálogo MOC.
Títulos oficiais são evidência de publicação; somente ZIPs realmente lidos geram diffs XSD.
"""
from __future__ import annotations
import argparse, copy, gzip, hashlib, io, json, re, sys, zipfile
from pathlib import Path, PurePosixPath
from collections import Counter
from urllib.parse import urljoin, urlsplit, parse_qs
from urllib.request import Request, build_opener, HTTPRedirectHandler
from bs4 import BeautifulSoup
from lxml import etree
from catalog_core import atomic_json, now_utc
ROOT=Path(__file__).resolve().parents[1]
SV='https://dfe-portal.svrs.rs.gov.br/'
NFE='https://www.nfe.fazenda.gov.br/portal/listaConteudo.aspx?tipoConteudo='
CTE='https://www.cte.fazenda.gov.br/portal/listaConteudo.aspx?tipoConteudo=0xlG1bdBass%3D'
# Portal SVRS (publicações) e, quando identificado, índice nacional de downloads.
FAMILIES={
 'nfe':(['nfe'],'NFe','BMPFMBoln3w%3D'), 'dce':(['dce'],'DCE',None),
 'cte':(['cte','cteos','gtve'],'CTe',CTE), 'abi':(['abi'],'Nfabi','sNOtscnJo6w%3D'),
 'nfgas':(['nfgas'],'Nfgas','rRDFjf1Ps7M%3D'), 'nfag':(['nfag'],'Nfag','2DuboicICSo%3D'),
 'nf3e':(['nf3e'],'Nf3e','hgMnsRcQa8I%3D'), 'nfcom':(['nfcom'],'Nfcom','7%2BcF7zwBrZ0%3D'),
 'bpe':(['bpe','bpetm','bpeta'],'Bpe',CTE), 'mdfe':(['mdfe'],'Mdfe',CTE)}
LABELS={'nfe':'NF-e/NFC-e','dce':'DC-e','cte':'CT-e / CT-e OS / GTVe','abi':'NF-e ABI','nfgas':'NFGAS','nfag':'NFAG','nf3e':'NF3-e','nfcom':'NFCom','bpe':'BP-e / TM / TA','mdfe':'MDF-e'}
HOSTS={'dfe-portal.svrs.rs.gov.br','www.nfe.fazenda.gov.br','www.cte.fazenda.gov.br','nfe.fazenda.gov.br','cte.fazenda.gov.br'}
XS='{http://www.w3.org/2001/XMLSchema}'
MAX=16*1024*1024; MAX_EXPANDED=64*1024*1024; MAX_FILES=400; MAX_NODES=100000
MAX_DOWNLOADS=4 # por família e rodada; não implica cobertura de todos os pacotes históricos

def sha(b): return hashlib.sha256(b).hexdigest()
def canonical(x): return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def allowed(u):
    p=urlsplit(u)
    return p.scheme=='https' and p.hostname in HOSTS and not p.username and not p.password and p.port in (None,443)
class SafeRedirect(HTTPRedirectHandler):
    def redirect_request(self,req,fp,code,msg,headers,newurl):
        if not allowed(newurl): raise ValueError('Redirecionamento fora das fontes autorizadas')
        return super().redirect_request(req,fp,code,msg,headers,newurl)
def fetch(u):
    if not allowed(u): raise ValueError('Fonte não autorizada')
    with build_opener(SafeRedirect()).open(Request(u,headers={'User-Agent':'DFE-Data-Explorer-XSD-monitor/1.0','Accept-Encoding':'identity'}),timeout=12) as r:
        if not allowed(r.geturl()): raise ValueError('Fonte final não autorizada')
        b=r.read(MAX+1)
    if len(b)>MAX: raise ValueError('Download acima do limite de 16 MiB')
    return b

def sources(family):
    _,folder,extra=FAMILIES[family]; out=[SV+folder+'/Documentos']
    if extra: out.append(extra if extra.startswith('https:') else NFE+extra)
    return out

def clean(s): return ' '.join(s.split())
def extract_publications(family, source, raw):
    soup=BeautifulSoup(raw,'html.parser'); result=[]; seen=set()
    # No JS execution, captcha bypass or guessed endpoint. Only direct download links.
    for a in soup.find_all('a'):
        title=clean(a.get_text(' ',strip=True))
        if not re.search(r'\b(?:schemas?|esquemas?|xsd)\b',title,re.I): continue
        if not (re.search(r'\d|pacote|evento',title,re.I) and len(title)>12): continue
        if re.match(r'nota t[eé]cnica',title,re.I) and not re.search(r'\b(?:zip|pacote)\b',title,re.I): continue
        # The CT-e national list includes BP-e and MDF-e. Do not mix them.
        if source==CTE:
            patterns={'cte':r'\bCT\s*-?\s*e\b','bpe':r'\bBP\s*-?\s*e\b','mdfe':r'\bMDF\s*-?\s*e\b'}
            if not re.search(patterns[family],title,re.I):continue
        href=a.get('href','').strip(); link=urljoin(source,href) if href and not href.startswith(('#','javascript:')) else ''
        if link and (not allowed(link) or not (urlsplit(link).path.lower().endswith('.zip') or ('exibirarquivo.aspx' in urlsplit(link).path.lower() and 'conteudo' in {k.lower() for k in parse_qs(urlsplit(link).query)}))):link=''
        # Some SVRS download controls have a direct data-href or data-url.
        if not link:
            for attr in ('data-url','data-href','data-download-url'):
                v=a.get(attr,''); u=urljoin(source,v) if v else ''
                if u and allowed(u) and urlsplit(u).path.lower().endswith('.zip'):link=u;break
        key=(title,link)
        if key in seen:continue
        seen.add(key);result.append({'title':title,'url':link,'source':source,'id':sha(canonical([title,link]))[:24]})
    if not result:raise ValueError('Nenhuma publicação de schema reconhecida; possível mudança na página ou acesso bloqueado')
    return result

def qname(el,v):
    if ':' in v:
        p,n=v.split(':',1);ns=el.nsmap.get(p)
        return '{'+ns+'}'+n if ns else v
    ns=el.nsmap.get(None);return '{'+ns+'}'+v if ns else v

def analyze(raw):
    if len(raw)>MAX:raise ValueError('ZIP excede limite')
    files={}; count=0
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        entries=[e for e in z.infolist() if not e.is_dir() and e.filename.lower().endswith('.xsd')]
        if not entries or len(entries)>MAX_FILES or sum(e.file_size for e in entries)>MAX_EXPANDED:raise ValueError('Pacote sem XSD ou acima dos limites')
        for e in entries:
            path=PurePosixPath(e.filename.replace('\\','/'))
            if path.is_absolute() or '..' in path.parts or ':' in str(path) or str(path) in files:raise ValueError('Caminho XSD inválido ou duplicado')
            if e.file_size>10*1024*1024:raise ValueError('XSD acima de 10 MiB')
            root=etree.fromstring(z.read(e),parser=etree.XMLParser(resolve_entities=False,load_dtd=False,no_network=True,huge_tree=False,remove_comments=True))
            if root.getroottree().docinfo.doctype or root.tag!=XS+'schema':raise ValueError('XSD inválido ou DTD proibido')
            # Chaves de declaração: arquivo, namespace, caminho estrutural e ocorrência.
            # Não confundir com XPath de instância; tipos referenciados não são expandidos.
            nodes={}
            def walk(el,parent=''):
                nonlocal count
                if not isinstance(el.tag,str):return
                count+=1
                if count>MAX_NODES:raise ValueError('Limite de declarações excedido')
                attrs={k:(qname(el,v) if k in ('type','ref','base','itemType','substitutionGroup','refer') else ' '.join(qname(el,w) for w in v.split()) if k=='memberTypes' else v) for k,v in el.attrib.items()}
                value={'kind':el.tag,'attributes':attrs}
                if el.text and el.text.strip():value['text']=clean(el.text)
                nodes[parent or '/schema']=value
                seen=Counter();order=[]
                for ch in el:
                    if not isinstance(ch.tag,str):continue
                    name=ch.get('name') or (qname(ch,ch.get('ref')) if ch.get('ref') else '') or (ch.get('value') if ch.tag in (XS+'enumeration',XS+'pattern') else '') or ''
                    seg=ch.tag+'['+name+']';seen[seg]+=1;key=(parent or '/schema')+'/'+seg+'#'+str(seen[seg]);order.append(key);walk(ch,key)
                if order:value['children']=order
            walk(root);files[str(path)]={'namespace':root.get('targetNamespace',''),'nodes':nodes}
    return {'files':files,'fileCount':len(files),'declarations':count,'hash':sha(canonical(files))}

def compare(before,after):
    changes=[]
    for f in sorted(set(before['files'])|set(after['files'])):
        b=before['files'].get(f);a=after['files'].get(f)
        if b is None or a is None:
            changes.append({'file':f,'path':'/','status':'incluído' if b is None else 'excluído','before':None if b is None else {'declarations':len(b['nodes'])},'after':None if a is None else {'declarations':len(a['nodes'])}});continue
        for key in sorted(set(b['nodes'])|set(a['nodes'])):
            old=b['nodes'].get(key);new=a['nodes'].get(key)
            if old!=new:changes.append({'file':f,'path':key,'status':'incluído' if old is None else 'excluído' if new is None else 'alterado','before':old,'after':new})
    return changes

def initial():return {'schemaVersion':1,'checkedAt':None,'families':{k:{'label':LABELS[k],'documents':v[0],'status':'aguardando','lastCheckAt':None,'lastSuccessAt':None,'publications':[],'packages':{},'events':[]} for k,v in FAMILIES.items()}}

def monitor_family(family, previous, storage, fetcher, stamp):
    d=copy.deepcopy(previous);baseline_packages=copy.deepcopy(previous['packages']);d['lastCheckAt']=stamp;errors=[];pubs=[];ok_sources=[]
    for source in sources(family):
        try:pubs.extend(extract_publications(family,source,fetcher(source)));ok_sources.append(source)
        except Exception as e:errors.append(source+': '+str(e)[:300])
    if not ok_sources:
        d.update(status='falha-preservado',errors=errors);return d
    # Never interpret disappearance in a failed or incomplete index as deletion of a schema.
    seen={p['id']:p for p in d['publications']};new={p['id']:p for p in pubs}
    for p in new.values():
        if p['id'] not in seen and d.get('lastSuccessAt'):
            d['events'].append({'id':sha(canonical([family,'publication',p['id']]))[:24],'date':stamp,'kind':'publicacao-identificada','title':p['title'],'source':p['source'],'url':p['url'],'changes':[]})
    d['publications']=list({**seen,**new}.values());d['lastSuccessAt']=stamp
    candidates={}
    for p in pubs:
        if p['url']:candidates.setdefault(p['url'],p)
    # Fetch recent direct links from each source, not arbitrary historical files.
    ordered=list(candidates.values());recent=ordered[:2]
    remaining=sorted(ordered[2:],key=lambda p:baseline_packages.get(sha(p['url'].encode())[:24],{}).get('lastCheckAt',''))
    chosen=(recent+remaining)[:MAX_DOWNLOADS];checked=0
    for p in chosen:
        k=sha(p['url'].encode())[:24];prior=d['packages'].get(k)
        try:
            raw=fetcher(p['url']);a=analyze(raw);h=a['hash'];store=storage/family;store.mkdir(parents=True,exist_ok=True)
            snapshot=store/(h+'.json.gz')
            if not snapshot.exists():
                tmp=snapshot.with_suffix('.tmp');tmp.write_bytes(gzip.compress(canonical(a),mtime=0));tmp.replace(snapshot)
            archive=store/(h+'.zip')
            if not archive.exists():
                tmp=archive.with_suffix('.tmp');tmp.write_bytes(raw);tmp.replace(archive)
            suspicious=bool(prior and (set(prior['fileNames'])-set(a['files']) or a['declarations']<prior['declarations']*0.8))
            if prior and prior['hash']!=h:
                old=json.loads(gzip.decompress((store/(prior['hash']+'.json.gz')).read_bytes()));changes=compare(old,a)
                event={'id':sha(canonical([family,k,prior['hash'],h]))[:24],'date':stamp,'kind':'revisao-necessaria' if suspicious else 'conteudo-alterado','title':p['title'],'source':p['source'],'url':p['url'],'beforeHash':prior['hash'],'afterHash':h,'changeCount':len(changes),'changes':changes[:100]}
                atomic_json(store/(event['id']+'.json'),{**event,'changes':changes});
                if not any(x['id']==event['id'] for x in d['events']):d['events'].append(event)
            elif not prior and baseline_packages:
                # Different URLs are distinct releases; only compare as a candidate when an identical file set exists.
                prevs=list(baseline_packages.values());matches=[x for x in prevs if x.get('fileNames')==sorted(a['files']) and x['hash']!=h]
                if matches:
                    oldref=max(matches,key=lambda x:x['lastCheckAt']);old=json.loads(gzip.decompress((store/(oldref['hash']+'.json.gz')).read_bytes()));changes=compare(old,a)
                    event={'id':sha(canonical([family,k,oldref['hash'],h]))[:24],'date':stamp,'kind':'comparacao-candidata','title':p['title'],'source':p['source'],'url':p['url'],'beforeHash':oldref['hash'],'afterHash':h,'changeCount':len(changes),'changes':changes[:100]}
                    atomic_json(store/(event['id']+'.json'),{**event,'changes':changes});d['events'].append(event)
            if suspicious:
                errors.append(p['title']+': redução suspeita de arquivos ou declarações; referência anterior preservada para revisão');continue
            d['packages'][k]={**p,'hash':h,'fileCount':a['fileCount'],'fileNames':sorted(a['files']),'declarations':a['declarations'],'lastCheckAt':stamp};checked+=1
        except Exception as e:errors.append(p['title']+': '+str(e)[:300])
    d.update(status='parcial' if errors or not chosen or len(chosen)<len(candidates) or any(not p['url'] for p in pubs) else 'verificado',errors=errors,listedThisCheck=len(pubs),directLinks=len(candidates),packagesChecked=checked,lastPackageCheckAt=stamp if checked else d.get('lastPackageCheckAt'))
    return d

def run(root=ROOT,family='all',fetcher=fetch):
    file=root/'public/data/xsd_monitoramento.json';state=json.loads(file.read_bytes()) if file.exists() else initial();stamp=now_utc();storage=root/'data/xsd_monitor';ids=FAMILIES if family=='all' else [family]
    for k in ids:
        state['families'][k]=monitor_family(k,state['families'][k],storage,fetcher,stamp)
        print(k,state['families'][k]['status'],state['families'][k].get('packagesChecked',0),'pacotes nesta rodada',flush=True)
    state['checkedAt']=stamp;atomic_json(file,state)
    return state

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--family',choices=['all',*FAMILIES],default='all');args=p.parse_args();state=run(family=args.family)
    # Separate from MOC; partial coverage is reported but does not prevent MOC publication.
    sys.exit(3 if any(d['status'] in ('parcial','falha-preservado') for k,d in state['families'].items() if args.family=='all' or k==args.family) else 0)
