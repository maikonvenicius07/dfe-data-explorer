from pathlib import Path
import sys,json,html
import pytest
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'scripts'))
from import_dce import extract,HEAD
CAT=json.loads((R/'public/data/dce/catalogo_atual.json').read_text())
def fixture(rows):
    def tr(cells,tag='td'):return '<tr>'+''.join(f'<{tag}>{html.escape(str(c or ""))}</{tag}>' for c in cells)+'</tr>'
    out=['<h1>Leiaute DC-e</h1><p>Atualizado até a NT 2024.001 v.1.21, publicada em junho de 2026</p>']
    for g in dict.fromkeys(x['mocGroup'] for x in rows):
        out.extend([f'<h2>Grupo {g}. Título de teste</h2>','<table>',tr(HEAD,'th')])
        for r in rows:
            if r['mocGroup']==g:out.append(tr([r['order'],r['officialId'],r['tag'],'Descrição teste',r['kind'],r['parent'],r['type'],r['occur'],r['length'],'Observação teste']))
        out.append('</table>')
    return ''.join(out)
def test_dce_import_preserves_collision_and_structure():
    data=extract(fixture(CAT['nodes']),CAT)
    assert len(data['nodes'])==111
    z=[r for r in data['nodes'] if r['id']=='Z06']
    assert {r['key'] for r in z}=={'Z06|Z05|xCampo','Z06|Z05|xTexto'}
    assert all(r['description']=='Descrição teste' and r['observation']=='Observação teste' for r in z)
    assert data['metadata']['documentId']=='dce'
    assert data['metadata']['status'].endswith('unverified-xsd')
def test_dce_rejects_partial_and_wrong_root():
    with pytest.raises(ValueError):extract(fixture(CAT['nodes'][:20]),CAT)
    wrong=[dict(r,tag='NFe') if r['id']=='ROOT' else r for r in CAT['nodes']]
    with pytest.raises(ValueError):extract(fixture(wrong),CAT)
