"""Testes sem rede: cópias dos catálogos reais em diretório temporário.
As alterações simuladas nunca são gravadas em public/data do projeto.
"""
from pathlib import Path
import copy,json,sys,shutil
import pytest
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'scripts'))
from monitor_documents import DOCUMENTS,baseline,run,gate,differences,path_for,load
from catalog_core import atomic_json
from test_import_dce import fixture,CAT
from import_documents import extract

@pytest.fixture
def sandbox(tmp_path):
    for doc in DOCUMENTS:
        p=path_for(tmp_path,doc);p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(path_for(R,doc),p)
    for name in ('status.json','historico.json','ultima_diferenca.json','notificacoes.json','catalogo_atual.json'):
        p=R/'data'/name
        if p.exists():
            dest=tmp_path/'data'/name;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,dest)
    return tmp_path

def test_baseline_does_not_claim_verification(sandbox):
    s=baseline(sandbox);assert len(s['documents'])==14;assert s['checkedAt'] is None
    assert all(d['lastCheckAt'] is None and not d['events'] for d in s['documents'].values())

def test_all_real_catalogs_unchanged_and_sources_cached(sandbox):
    calls=[];old={d:path_for(sandbox,d).read_bytes() for d in DOCUMENTS}
    def fetcher(d):calls.append(d);return 'fixture'
    def parser(d,h):
        cat=load(path_for(sandbox,d));cat['metadata']['sourceHash']='html mudou';cat['metadata']['extractedAt']='novo';return cat
    state,events,errors=run(sandbox,fetcher=fetcher,parser=parser)
    assert not errors and not events;assert len(calls)==10
    assert all(v['status']=='sem-alteracoes' for v in state['documents'].values())
    assert all(path_for(sandbox,d).read_bytes()==old[d] for d in DOCUMENTS)

def test_changes_isolated_snapshots_history_and_idempotence(sandbox):
    doc='nf3e';old=load(path_for(sandbox,doc));new=copy.deepcopy(old);new['nodes'][10]['description']+=' (teste)';new['metadata']['technicalNote']='NT teste'
    before=path_for(sandbox,'nfcom').read_bytes()
    def fetcher(d):
        if d=='nfcom':raise OSError('DNS simulado')
        return 'fixture'
    def parser(d,h):return copy.deepcopy(new) if d==doc else load(path_for(sandbox,d))
    st,events,errors=run(sandbox,[doc,'nfcom','mdfe'],fetcher,parser)
    assert errors==['nfcom'] and len(events)==1
    assert st['documents']['mdfe']['status']=='sem-alteracoes'
    assert path_for(sandbox,'nfcom').read_bytes()==before
    assert load(path_for(sandbox,doc))['nodes'][10]['description']==new['nodes'][10]['description']
    e=events[0];assert e['counts']['alterado']==2
    assert len(list((sandbox/'data/documents/nf3e/snapshots').glob('*.json')))==2
    st,events,errors=run(sandbox,[doc],lambda d:'fixture',parser)
    assert not events and not errors and len(st['documents'][doc]['events'])==1
    assert st['documents']['nfcom']['status']=='falha-preservado'

def test_partial_import_never_replaces_old_even_with_equal_count(sandbox):
    d='mdfe';p=path_for(sandbox,d);old=p.read_bytes();new=load(p);new['nodes'][10]['key']='new-key';new['nodes'][10]['id']='new-key'
    st,events,errors=run(sandbox,[d],lambda d:'fixture',lambda d,h:new)
    assert errors==[d] and not events and p.read_bytes()==old
    assert st['documents'][d]['status']=='revisao-necessaria'
    assert {x['status'] for x in st['documents'][d]['candidate']['changes']}=={'incluído','excluído'}

def test_reject_table_loss_and_hierarchy_regression(sandbox):
    doc='nfcom';old=load(path_for(sandbox,doc))
    for key,delta in [('tableCount',-1),('hierarchyIssues',1)]:
        new=copy.deepcopy(old);new['metadata'][key]+=delta
        with pytest.raises(ValueError):gate(doc,old,new,differences(old,new))

def test_new_field_and_nfe_legacy_history(sandbox):
    doc='nfe';p=path_for(sandbox,doc);old=load(p);new=copy.deepcopy(old);row=dict(new['nodes'][-1],key='TEST-NEW',id='TEST-NEW',officialId='TEST-NEW',tag='teste');new['nodes'].append(row);new['metadata']['totalRows']+=1
    before=len(load(sandbox/'data/historico.json',[]));st,events,errors=run(sandbox,[doc],lambda d:'fixture',lambda d,h:new)
    assert not errors and events[0]['counts']['incluído']==1
    assert len(load(sandbox/'data/historico.json'))==before+1
    assert load(sandbox/'data/catalogo_atual.json')==load(p)
    assert load(sandbox/'public/data/ultima_diferenca.json')['changes'][0]['status']=='incluído'

def test_real_importer_dce_fixture_updates_description(sandbox):
    d='dce';old=CAT;html=fixture(old['nodes']);new=extract(d,html)
    assert len(new['nodes'])==111
    # Fixture replaces all descriptions, not the published catalog.
    assert any(c['status']=='alterado' for c in differences(old,new))

def test_single_daily_workflow_and_explicit_pages():
    p=R/'.github/workflows';main=(p/'importar_documentos.yml').read_text();old=(p/'atualizar_moc.yml').read_text()
    assert "cron: '17 11 * * *'" in main and 'schedule:' not in old
    assert 'scripts/monitor_documents.py' in main and 'gh workflow run publicar_paginas.yml --ref main' in main
    assert 'pages/builds' in main and 'git push' in main
    assert 'steps.collect.outputs.partial' in main and 'exit "$code"' in main
    assert 'documento: nfe' in old

def test_pending_comparison_survives_followup_network_error(sandbox):
    d='mdfe';p=path_for(sandbox,d);original=p.read_bytes();new=load(p);new['nodes'].pop()
    state,_,errors=run(sandbox,[d],lambda doc:'fixture',lambda doc,h:new)
    assert errors==[d];pending=state['documents'][d]['candidate'];assert pending['hash']
    def failed(doc):raise OSError('DNS simulado')
    state,_,errors=run(sandbox,[d],failed)
    assert errors==[d] and state['documents'][d]['candidate']==pending and p.read_bytes()==original
