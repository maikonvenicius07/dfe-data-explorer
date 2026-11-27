"""Monitor diário dos 14 catálogos; usa os importadores existentes, sem validar XSD.
Exit 3 = uma ou mais fontes requerem atenção; demais fontes foram processadas.
Erros de gravação/construção são fatais e não devem ser publicados pelo workflow.
"""
from pathlib import Path
from collections import Counter
from urllib.request import Request, urlopen
import argparse, json, subprocess, sys
from catalog_core import OFFICIAL_URL, parse_moc, quality_gate, atomic_json, digest, now_utc
from import_documents import SOURCES, url, fetch, extract, validate_source_coverage

ROOT = Path(__file__).resolve().parents[1]
DOCUMENTS = {'nfe': ('NF-e e NFC-e', OFFICIAL_URL), **{k:(v[0],url(k)) for k,v in SOURCES.items()}}
FIELDS = ('order','officialId','tag','description','kind','parent','officialParent','type','occur','length','observation','mocGroup','sourceSection','sourceLevel','sourceHierarchyPath','sourceValues','original','hierarchyIssue','nonXmlMarker','sourceRootWrapper')
META = ('technicalNote','publicationDate','manualReference')

def load(path, default=None):
    return json.loads(path.read_text(encoding='utf8')) if path.exists() else default

def path_for(root, doc):
    return root/'public/data'/('catalogo_atual.json' if doc=='nfe' else doc+'/catalogo_atual.json')

def projection(cat):
    return {'nodes':[{k:n.get(k) for k in ('key',*FIELDS)} for n in cat['nodes']],
            'groups':cat.get('groups',[]), 'reference':{k:cat['metadata'].get(k) for k in META}}

def differences(old,new):
    a,b=projection(old),projection(new)
    def index(p):return {n['key']:n for n in p['nodes']}
    x,y=index(a),index(b); out=[]
    for key in sorted(x.keys()|y.keys()):
        if key not in x:out.append({'id':key,'field':y[key]['tag'],'officialId':y[key]['officialId'],'status':'incluído','new':y[key]})
        elif key not in y:out.append({'id':key,'field':x[key]['tag'],'officialId':x[key]['officialId'],'status':'excluído','old':x[key]})
        elif x[key]!=y[key]:
            out.append({'id':key,'field':y[key]['tag'],'officialId':y[key]['officialId'],'status':'alterado','changes':{k:{'before':x[key][k],'after':y[key][k]} for k in x[key] if x[key][k]!=y[key][k]}})
    for k in ('groups','reference'):
        if a[k]!=b[k]:out.append({'id':k,'field':'Grupos editoriais' if k=='groups' else 'Referência do manual','status':'alterado','changes':{k:{'before':a[k],'after':b[k]}}})
    # Preserve a reordering even if all individual nodes remain identical.
    if not out and a['nodes']!=b['nodes']:out.append({'id':'order','field':'Ordem dos registros','status':'alterado','changes':{'order':{'before':[n['key'] for n in a['nodes']],'after':[n['key'] for n in b['nodes']]}}})
    return out

def gate(doc,old,new,changes):
    nodes=new.get('nodes') or []; meta=new['metadata']
    if not nodes or meta.get('documentId',doc)!=doc or meta.get('source')!=DOCUMENTS[doc][1]:raise ValueError('Identidade ou fonte do catálogo incompatível')
    keys=[n.get('key') for n in nodes]
    if None in keys or '' in keys or len(set(keys))!=len(keys):raise ValueError('Chaves internas ausentes ou duplicadas')
    if doc=='nfe':quality_gate(new,old)
    else:validate_source_coverage(doc,new)
    om=old['metadata']
    if len(nodes)<len(old['nodes']) or any(c['status']=='excluído' for c in changes):raise ValueError('Registros removidos ou identidades alteradas: revisão manual obrigatória antes de substituir o catálogo')
    if meta.get('tableCount',0)<(om.get('tableCount') or 0):raise ValueError('Redução do número de tabelas')
    if meta.get('hierarchyIssues',0)>(om.get('hierarchyIssues') or 0):raise ValueError('Aumento de vínculos hierárquicos não resolvidos')
    old_sections={t['section'] for t in om.get('tables',[])};new_sections={t['section'] for t in meta.get('tables',[])}
    if old_sections-new_sections:raise ValueError('Seções anteriores ausentes: revisão manual obrigatória')
    if len(meta.get('unmappedTables',[]))>len(om.get('unmappedTables',[])):raise ValueError('Aumento de tabelas não reconhecidas')
    # Stable identities for duplicated tags may depend on their occurrence; a change in
    # such a family must be inspected rather than silently remapping saved selections.
    if doc not in ('nfe','dce'):
        def families(cat):return Counter((n.get('sourceSection'),n.get('sourceHierarchyPath'),n.get('officialId')) for n in cat['nodes'])
        a,b=families(old),families(new)
        if any(a[k]!=b[k] and max(a[k],b[k])>1 for k in a.keys()|b.keys()):raise ValueError('Quantidade de identidades ambíguas alterada')
    if om.get('technicalNote') and not meta.get('technicalNote'):raise ValueError('Referência de Nota Técnica anteriormente disponível não encontrada')
    return True

def baseline(root):
    result={'schemaVersion':1,'checkedAt':None,'documents':{}}
    for doc,(label,source) in DOCUMENTS.items():
        cat=load(path_for(root,doc)); m=cat['metadata'] if cat else {}
        result['documents'][doc]={'label':label,'source':source,'status':'aguardando-primeira-verificacao','lastCheckAt':None,'lastSuccessAt':None,'rows':len(cat['nodes']) if cat else 0,'technicalNote':m.get('technicalNote'),'catalogExtractedAt':m.get('extractedAt'),'events':[]}
    return result

def collect_html(doc,html_dir=None):
    if doc!='nfe':return fetch(doc,html_dir)
    if html_dir:return (html_dir/'nfe.html').read_text(encoding='utf-8-sig')
    req=Request(OFFICIAL_URL,headers={'User-Agent':'DF-e Data Explorer/2.3.25','Accept':'text/html'})
    with urlopen(req,timeout=35) as response:
        if response.geturl().split('?')[0]!=OFFICIAL_URL:raise ValueError('Redirecionamento inesperado')
        raw=response.read(25_000_001)
        if len(raw)>25_000_000:raise ValueError('HTML excede 25 MB')
        return raw.decode(response.headers.get_content_charset() or 'utf8',errors='strict')

def parse(doc,html):
    return parse_moc(html) if doc=='nfe' else extract(doc,html)

def legacy_nfe(root,cat,entry,event=None):
    """Compatibilidade com histórico da NF-e e backend existente."""
    data=root/'data'; st=load(data/'status.json',{})
    st.update(status=entry['status'],lastCheckAt=entry['lastCheckAt'],message=entry.get('message',''),lastSuccessAt=entry.get('lastSuccessAt'))
    if entry['status'] in ('falha-preservado','revisao-necessaria'):st['lastErrorAt']=entry['lastCheckAt']
    if event:
        m=cat['metadata']; st.update(currentHash=m['sourceHash'],version=m['snapshotId'],count=len(cat['nodes']))
        snap=data/'snapshots'/(m['snapshotId']+'.json');atomic_json(snap,cat)
        h=load(data/'historico.json',[]);h.append({'id':m['snapshotId'],'capturedAt':event['date'],'hash':m['sourceHash'],'totalRows':len(cat['nodes']),'note':m.get('technicalNote'),'changes':len(event['changes']),'snapshot':snap.name});atomic_json(data/'historico.json',h)
        atomic_json(data/'ultima_diferenca.json',{'from':event['previousSnapshot'],'to':m['snapshotId'],'changes':event['changes']})
        notes=load(data/'notificacoes.json',[]);notes.append({'id':event['id'],'date':event['date'],'message':event['message'],'snapshotId':m['snapshotId']});atomic_json(data/'notificacoes.json',notes)
        atomic_json(data/'catalogo_atual.json',cat)
    atomic_json(data/'status.json',st)
    for name in ('status.json','historico.json','ultima_diferenca.json','notificacoes.json'):
        p=data/name
        if p.exists():atomic_json(root/'public/data'/name,load(p))

def run(root=ROOT, docs=None, fetcher=collect_html, parser=parse):
    ids=list(docs or DOCUMENTS); state_path=root/'public/data/monitoramento.json'
    state=load(state_path) or baseline(root)
    state['checkedAt']=now_utc(); report_path=root/'public/data/importacao_documentos.json';report=load(report_path,{}).get('documents',{})
    cache={}; fresh=[]; failures=[]
    for doc in ids:
        label,source=DOCUMENTS[doc]; dest=path_for(root,doc);old=load(dest);e=state['documents'][doc];e['lastCheckAt']=now_utc();e.pop('error',None)
        e.update(rows=len(old['nodes']) if old else 0,technicalNote=old['metadata'].get('technicalNote') if old else None)
        new=None; changes=None; event=None
        try:
            if source not in cache:
                try:cache[source]=(fetcher(doc),None)
                except Exception as exc:cache[source]=(None,exc)
            html,err=cache[source]
            if err:raise err
            new=parser(doc,html)
            if not old:raise ValueError('Catálogo inicial ausente; execute importação inicial validada')
            changes=differences(old,new)
            gate(doc,old,new,changes)
        except Exception as exc:
            e.update(status='revisao-necessaria' if changes is not None else 'falha-preservado',error=str(exc)[:500],message='Catálogo anterior preservado')
            if changes is not None:
                e['candidate']={'date':e['lastCheckAt'],'technicalNote':new['metadata'].get('technicalNote'),'rows':len(new['nodes']),'changes':changes,'hash':digest(projection(new))}
            failures.append(doc)
        else:
            e['lastSuccessAt']=now_utc();e.pop('candidate',None)
            if changes:
                oldhash=digest(projection(old));newhash=digest(projection(new));stamp=now_utc();eventid=digest([doc,oldhash,newhash,stamp])[:24]
                folder=root/'data/documents'/doc/'snapshots';atomic_json(folder/(oldhash+'.json'),old)
                m=new['metadata'];m['snapshotId']=stamp.replace(':','-')+'-'+newhash[:12];m['technicalHash']=newhash
                if doc=='nfe':m['sourceHash']=digest([{k:v for k,v in n.items() if k!='source'} for n in new['nodes']])
                atomic_json(folder/(newhash+'.json'),new)
                counts=Counter(c['status'] for c in changes)
                event={'id':eventid,'date':stamp,'technicalNote':m.get('technicalNote'),'previousNote':old['metadata'].get('technicalNote'),'previousSnapshot':old['metadata'].get('snapshotId'),'beforeHash':oldhash,'afterHash':newhash,'counts':dict(counts),'changes':changes,'message':f'{label}: {len(changes)} diferença(s) de documentação; NT: {m.get("technicalNote") or "não identificada"}'}
                atomic_json(dest,new);e['events'].append(event);fresh.append(event)
                e.update(status='atualizado',message=event['message'],rows=len(new['nodes']),technicalNote=m.get('technicalNote'),catalogExtractedAt=m.get('extractedAt'))
            else:e.update(status='sem-alteracoes',message='Nenhuma alteração técnica identificada')
        if doc=='nfe':legacy_nfe(root,new if event else old,e,event)
        else:report[doc]={'status':e['status'],'source':source,'imported':e['rows'],'checkedAt':e['lastCheckAt'],'error':e.get('error')}
        print(doc,e['status'],e.get('error',''),flush=True)
    atomic_json(state_path,state);atomic_json(report_path,{'checkedAt':state['checkedAt'],'documents':report})
    return state, fresh, failures

def notify_email(events):
    import os,smtplib
    from email.message import EmailMessage
    keys=('SMTP_HOST','SMTP_FROM','SMTP_TO','SMTP_USER','SMTP_PASSWORD');cfg={k:os.environ.get(k) for k in keys}
    if not events or not all(cfg.values()):return
    msg=EmailMessage();msg['Subject']='DF-e Data Explorer — alterações nos leiautes';msg['From']=cfg['SMTP_FROM'];msg['To']=cfg['SMTP_TO'];msg.set_content('\n'.join(e['message'] for e in events)+'\nConsulte Atualizações e histórico no aplicativo.')
    with smtplib.SMTP_SSL(cfg['SMTP_HOST'],int(os.environ.get('SMTP_PORT','465')),timeout=20) as smtp:smtp.login(cfg['SMTP_USER'],cfg['SMTP_PASSWORD']);smtp.send_message(msg)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--document',choices=['all',*DOCUMENTS],default='all');ap.add_argument('--html-dir',type=Path);ap.add_argument('--init',action='store_true');ap.add_argument('--email-events',type=Path);ap.add_argument('--send-email',type=Path);a=ap.parse_args()
    if a.send_email:
        try:notify_email(load(a.send_email,[]))
        except Exception as exc:print('Aviso: envio SMTP falhou:',type(exc).__name__,file=sys.stderr);return 1
        return 0
    if a.init:
        p=ROOT/'public/data/monitoramento.json'
        if not p.exists():atomic_json(p,baseline(ROOT))
        return 0
    _,events,failed=run(docs=None if a.document=='all' else [a.document],fetcher=lambda doc:collect_html(doc,a.html_dir))
    # Build both embedded and offline files before the workflow is allowed to commit.
    subprocess.run([sys.executable,str(ROOT/'scripts/prepare_release.py')],check=True)
    if a.email_events:atomic_json(a.email_events,events)
    return 3 if failed else 0
if __name__=='__main__':sys.exit(main())
