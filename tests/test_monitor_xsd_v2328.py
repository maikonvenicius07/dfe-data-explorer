from pathlib import Path
import io,sys,zipfile,json,copy
import pytest
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from monitor_xsd import *

def package(n='10',occ='0',add=False,second=True,prefix='xs',comment=''):
    body=f'<{prefix}:schema xmlns:{prefix}="http://www.w3.org/2001/XMLSchema" targetNamespace="urn:example"><{prefix}:element name="campo" minOccurs="{occ}"><{prefix}:simpleType><{prefix}:restriction base="{prefix}:string"><{prefix}:maxLength value="{n}"/></{prefix}:restriction></{prefix}:simpleType></{prefix}:element>{comment}'+(f'<{prefix}:element name="novo" type="{prefix}:string"/>' if add else '')+f'</{prefix}:schema>'
    b=io.BytesIO()
    with zipfile.ZipFile(b,'w') as z:
        z.writestr('main.xsd',body)
        if second:z.writestr('aux.xsd',f'<{prefix}:schema xmlns:{prefix}="http://www.w3.org/2001/XMLSchema"/>')
    return b.getvalue()

def pages(title='Pacote Schemas NT 2026.001 v1.00',name='a.zip'):
    return f'<h2><a href="/{name}">{title}</a></h2>'.encode()
def fake(raw,html=None):return lambda u:raw if u.endswith('.zip') else (html or pages())

def test_14_documents_10_families():
    assert len(FAMILIES)==10 and len(set(x for v in FAMILIES.values() for x in v[0]))==14

def test_safe_links_and_national_mixed():
    h=b'<a href="/portal/exibirArquivo.aspx?conteudo=123">Schemas XML CT-e NT 2026.001</a><a href="/b.zip">Schemas XML BP-e NT 2026.001</a><a href="https://example.com/z.zip">Schemas XML CT-e NT 2026.002</a>'
    r=extract_publications('cte',CTE,h);assert len(r)==2 and r[0]['url'].startswith('https://www.cte') and not r[1]['url']
    assert len(extract_publications('bpe',CTE,h))==1

def test_title_only_not_download():
    r=extract_publications('nf3e',sources('nf3e')[0],b'<h2><a href="#" onclick="openDocument(7)">Schemas NT 2026.004 v1.01</a></h2>');assert not r[0]['url']

def test_wrong_html_fails():
    with pytest.raises(ValueError):extract_publications('nfe',sources('nfe')[0],b'<html>captcha</html>')

def test_xsd_diff_and_prefix():
    a=analyze(package());b=analyze(package(prefix='x',comment='<!-- cosmetic -->'));assert a['hash']==b['hash']
    c=compare(a,analyze(package(n='20',occ='1',add=True)));assert any(x['status']=='incluído' and 'novo' in x['path'] for x in c);assert any(x['before'] and x['after'] and x['before'].get('attributes',{}).get('minOccurs')=='0' and x['after']['attributes']['minOccurs']=='1' for x in c);assert any('maxLength' in x['path'] for x in c)

def test_decl_removal():
    assert any(x['status']=='excluído' and 'novo' in x['path'] for x in compare(analyze(package(add=True)),analyze(package())))

@pytest.mark.parametrize('name,body',[('../a.xsd','<bad/>'),('a.xsd','<!DOCTYPE schema [<!ENTITY a SYSTEM "file:///etc/passwd">]><schema/>'),('a.xsd','<notSchema/>')])
def test_unsafe_or_invalid_zip(name,body):
    b=io.BytesIO()
    with zipfile.ZipFile(b,'w') as z:z.writestr(name,body)
    with pytest.raises(ValueError):analyze(b.getvalue())

def test_baseline_change_and_history(tmp_path):
    start=initial()['families']['dce'];a=monitor_family('dce',start,tmp_path,fake(package()),'2026-11-27T00:00:00Z');assert a['status']=='verificado' and not a['events'];assert len(list(tmp_path.rglob('*.zip')))==1
    b=monitor_family('dce',a,tmp_path,fake(package(n='20')),'2026-11-28T00:00:00Z');assert b['events'][0]['kind']=='conteudo-alterado';assert len(list(tmp_path.rglob('*.json.gz')))==2
    c=monitor_family('dce',b,tmp_path,fake(package(n='20')),'2026-11-29T00:00:00Z');assert len(c['events'])==1
    d=monitor_family('dce',c,tmp_path,fake(b'not zip'),'2026-11-30T00:00:00Z');assert d['status']=='parcial' and d['packages']==c['packages']

def test_suspicious_removal_preserved(tmp_path):
    a=monitor_family('dce',initial()['families']['dce'],tmp_path,fake(package()),'1');b=monitor_family('dce',a,tmp_path,fake(package(second=False)),'2');assert b['status']=='parcial' and b['packages']==a['packages'];assert any(x['status']=='excluído' for x in b['events'][0]['changes'])
    c=monitor_family('dce',b,tmp_path,fake(package(second=False)),'3');assert len(c['events'])==len(b['events'])

def test_failure_isolated_and_moc_not_changed(tmp_path):
    f=tmp_path/'public/data/catalogo_atual.json';f.parent.mkdir(parents=True);f.write_text('preservar')
    def fetcher(u):
        if 'Nfcom' in u or '7%2Bc' in u:raise OSError('DNS')
        return fake(package())(u)
    s=run(tmp_path,fetcher=fetcher);assert s['families']['nfcom']['status']=='falha-preservado' and s['families']['dce']['status']=='verificado';assert f.read_text()=='preservar'

def test_new_release_candidate_not_confirmed_replacement(tmp_path):
    a=monitor_family('dce',initial()['families']['dce'],tmp_path,fake(package()),'1');b=monitor_family('dce',a,tmp_path,fake(package(n='20'),pages('Schemas NT 2026.002 v1.01','b.zip')),'2');assert {x['kind'] for x in b['events']}=={'publicacao-identificada','comparacao-candidata'} and len(b['packages'])==2

def test_listing_without_zip_not_claimed(tmp_path):
    a=monitor_family('dce',initial()['families']['dce'],tmp_path,lambda u:b'<a href="#">Pacote Schemas NT 2026.001</a>','1');assert a['status']=='parcial' and a['lastSuccessAt']=='1' and not a['packages']
