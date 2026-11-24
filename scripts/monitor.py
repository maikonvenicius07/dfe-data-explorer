"""Sincronização sob demanda/agendada; a primeira coleta requer internet no servidor."""
from __future__ import annotations
import argparse
import json
import os
from pathlib import Path
import sys
from urllib.request import Request,urlopen
from urllib.error import URLError
from catalog_core import OFFICIAL_URL,parse_moc,quality_gate,diff_catalogs,digest,atomic_json,now_utc

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data'
LAST=DATA/'catalogo_atual.json'; STATUS=DATA/'status.json'; HISTORY=DATA/'historico.json'

def load(path,fallback=None):
    try:return json.loads(Path(path).read_text(encoding='utf8'))
    except (FileNotFoundError,json.JSONDecodeError):return fallback

def notify_email(note,changes):
    """Envio opcional, configurado por SMTP_*; nunca envia sem credenciais."""
    import smtplib
    from email.message import EmailMessage
    host=os.environ.get('SMTP_HOST'); sender=os.environ.get('SMTP_FROM'); to=os.environ.get('SMTP_TO')
    password=os.environ.get('SMTP_PASSWORD'); user=os.environ.get('SMTP_USER')
    if not (host and sender and to and user and password):return False
    msg=EmailMessage();msg['Subject']='Atualização do leiaute MOC NF-e/NFC-e';msg['From']=sender;msg['To']=to
    msg.set_content(note['message']+'\n\nConsulte a Central de Atualizações do explorador.\nAlterações: '+str(len(changes)))
    with smtplib.SMTP_SSL(host,int(os.environ.get('SMTP_PORT','465')),timeout=20) as smtp:
        smtp.login(user,password);smtp.send_message(msg)
    return True

def synchronize(fetch=None):
    st=load(STATUS,{})
    st['lastCheckAt']=now_utc()
    try:
        if fetch is None:
            req=Request(OFFICIAL_URL,headers={'User-Agent':'NF-e-XSD-Explorer/2.0 contato: administrador', 'Accept':'text/html'})
            with urlopen(req,timeout=35) as resp:
                raw=resp.read(25_000_001)
                if len(raw)>25_000_000:raise ValueError('HTML excessivamente grande')
                encoding=resp.headers.get_content_charset() or 'utf-8'
                html_text=raw.decode(encoding,errors='replace')
        else:html_text=fetch()
        new=parse_moc(html_text); old=load(LAST)
        quality_gate(new,old)
        new_hash=digest([dict((k,v) for k,v in n.items() if k!='source') for n in new['nodes']])
        st['lastObservedHash']=new_hash
        if old and old.get('metadata',{}).get('sourceHash')==new_hash:
            st.update({'status':'sem-alteracoes','lastSuccessAt':now_utc(),'message':'Catálogo sem alterações técnicas'})
            atomic_json(STATUS,st);return {'changed':False,'message':st['message']}
        new['metadata']['sourceHash']=new_hash
        new['metadata']['snapshotId']=now_utc().replace(':','-')+'-'+new_hash[:10]
        changes=diff_catalogs(old or {'nodes':[]},new)
        # Persist snapshot before switching 'current'. Never replace current on failure.
        snap=DATA/'snapshots'/f"{new['metadata']['snapshotId']}.json"
        atomic_json(snap,new)
        history=load(HISTORY,[])
        history.append({'id':new['metadata']['snapshotId'],'capturedAt':now_utc(),
                        'hash':new_hash,'totalRows':len(new['nodes']),'note':new['metadata']['technicalNote'],
                        'changes':len(changes),'snapshot':snap.name})
        atomic_json(HISTORY,history)
        atomic_json(DATA/'ultima_diferenca.json',{'from':(old or {}).get('metadata',{}).get('snapshotId'),
                   'to':new['metadata']['snapshotId'],'changes':changes})
        atomic_json(LAST,new)
        note={'id':new_hash[:16], 'date':now_utc(), 'message':f'MOC atualizado: {len(changes)} diferença(s) em {len(new["nodes"])} registros; NT: {new["metadata"].get("technicalNote") or "não identificada"}', 'snapshotId':new['metadata']['snapshotId']}
        notes=load(DATA/'notificacoes.json',[])
        if not any(x.get('id')==note['id'] for x in notes):
            notes.append(note);atomic_json(DATA/'notificacoes.json',notes)
            try:notify_email(note,changes)
            except Exception as email_exc:st['emailWarning']=str(email_exc)[:180]
        st.update({'status':'atualizado','lastSuccessAt':now_utc(),'message':f'{len(changes)} alterações detectadas',
                   'currentHash':new_hash,'version':new['metadata']['snapshotId'],'count':len(new['nodes'])})
        atomic_json(STATUS,st)
        return {'changed':True,'count':len(new['nodes']),'changes':len(changes)}
    except Exception as exc:
        st.update({'status':'falha-preservado','message':str(exc)[:500],'lastErrorAt':now_utc()})
        atomic_json(STATUS,st)
        return {'changed':False,'error':str(exc),'preserved':True}

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--file',help='HTML MOC salvo localmente (importação offline)')
    args=parser.parse_args();res=synchronize(fetch=(lambda:Path(args.file).read_text(encoding='utf8')) if args.file else None)
    print(json.dumps(res,ensure_ascii=False,indent=2));sys.exit(1 if 'error' in res else 0)
