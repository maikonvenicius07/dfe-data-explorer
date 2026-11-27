"""Fixtures sintéticas para testar o formato das tabelas observadas no portal.
Nenhum fixture é catálogo fiscal de produção."""
from pathlib import Path
import sys,html,json
import pytest
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'scripts'))
from import_documents import extract,SOURCES
HEAD=['#','Campo','Nível','Descrição','Ele','Tipo','Ocorr.','Tamanho','Domínio','Exp. Reg.','Observações']
HEAD_ID=['#','ID','Campo','Descrição','Ele','Pai','Tipo','Ocor.','Tam.','Observação']
def table(head,rows):
    def tr(row,t):return '<tr>'+''.join(f'<{t}>{html.escape(str(c))}</{t}>' for c in row)+'</tr>'
    return '<table>'+tr(head,'th')+''.join(tr(r,'td') for r in rows)+'</table>'
def row(num,tag,level,kind='G',obs=''):return [num,tag,level,'descrição teste',kind,'','1-1','','D1','ER1',obs]
def page(content):return '<html><title>Leiaute teste</title><h1>Leiaute teste</h1>'+content+'</html>'
def fixture(doc):
    if doc=='abi':return page('<h2>1. Leiaute</h2>'+table(HEAD_ID,[[0,'-','NFeABI','raiz','G','-','','1-1','',''],[1,'A01','infNFe','grupo','G','Raiz','','1-1','',''],[2,'A02','Id','teste','A','A01','C','1-1','47','']]))
    root=SOURCES[doc][2]
    h2={'cte':2,'cteos':4,'gtve':5,'bpe':2,'bpetm':3,'bpeta':4}.get(doc,1)
    body=f'<h2>{h2}. Leiaute</h2>'+table(HEAD,[row(1,root,0),row(2,'ide',1),row(3,'CNPJ',2,'E'),row(4,'emit',1),row(5,'CNPJ',2,'E')])
    if doc=='mdfe':
        for i,(tag,modal) in enumerate([('rodo','Rodoviário'),('aereo','Aéreo'),('ferrov','Ferroviário'),('aquav','Aquaviário')],3):body+=f'<h2>{i}. Modal {modal}</h2>'+table(HEAD,[row(1,tag,0),row(2,'campo',1,'E')])
    return page(body)
@pytest.mark.parametrize('doc',[d for d in SOURCES if d!='dce'])
def test_document_types(doc):
    c=extract(doc,fixture(doc));r=c['nodes'];m=c['metadata'];assert m['documentId']==doc and m['totalRows']==len(r)
    assert len({n['id'] for n in r})==len(r)
    assert sum(t['rows'] for t in m['tables'])==len(r)
    assert all(n['original'] for n in r)
    assert all(n['parent'] is None or n['parent'] in {a['id'] for a in r} for n in r)
    if doc!='abi':
        a,b=[n for n in r if n['tag']=='CNPJ'];assert a['parent']!=b['parent'];assert a['officialId']=='—';assert 'D1' in a['observation'] and 'ER1' in a['observation']
    else: assert r[1]['parent']==r[0]['id'] and r[2]['parent']==r[1]['id']
def test_variants_do_not_mix():
    p=page(''.join(f'<h2>{i}. Variante</h2>'+table(HEAD,[row(1,'infCte',0),row(2,t,1,'E')]) for i,t in [(2,'carga'),(4,'outros'),(5,'valores')]))
    for doc,tag in [('cte','carga'),('cteos','outros'),('gtve','valores')]:
        c=extract(doc,p);assert [n['tag'] for n in c['nodes']]==['infCte',tag]
def test_wrong_root_and_incomplete_modal():
    with pytest.raises(ValueError):extract('nf3e',fixture('nfag'))
    with pytest.raises(ValueError):extract('mdfe',page('<h2>2. Geral</h2>'+table(HEAD,[row(1,'infMDFe',0)])))
def test_source_parent_conflict_not_invented():
    h=HEAD[:3]+['Pai']+HEAD[3:];r=[row(1,'infNF3e',0),row(2,'ide',1),row(3,'CNPJ',2,'E')];r=[x[:3]+[p]+x[3:] for x,p in zip(r,['Raiz','infNF3e','emit'])]
    cat=extract('nf3e',page('<h2>1. Leiaute</h2>'+table(h,r)));assert cat['nodes'][2]['parent'] is None;assert cat['metadata']['hierarchyIssues']==1
def test_current_and_historical_values_preserved():
    t=fixture('nf3e').replace('descrição teste','<del>antiga</del>nova',1);n=extract('nf3e',t)['nodes'][0];assert n['description']=='nova' and 'antiga' in n['original']['description']
def test_production_registry_never_includes_missing_files():
    import re
    html=(R/'public/index.html').read_text();manifest=json.loads(re.search(r'<script id="documentRegistry" type="application/json">(.*?)</script>',html,re.S)[1]);
    for doc,item in manifest.items():
        cat=json.loads((R/'public/data'/doc/'catalogo_atual.json').read_text());assert item['rows']==len(cat['nodes']) and cat['metadata']['documentId']==doc
