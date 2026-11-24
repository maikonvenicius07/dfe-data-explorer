import json
import io
from pathlib import Path
import sys
import tempfile
import unittest
import zipfile
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from catalog_core import parse_moc,diff_catalogs,quality_gate
from xsd_catalog import analyze_zip
import monitor

def mock_doc(extra='',second=False):
    def tr(items):return '<tr>' + ''.join(f'<td>{c}</td>' for c in items) + '</tr>'
    head=tr(['#','ID','Campo','Descrição','Ele','Pai','Tipo','Ocor.','Tam.','Observação'])
    rows=[['0','-','NFe','Raiz oficial','G','-','-','1-1','-','Nota fiscal'],
          ['1','A01','infNFe','Informações da NF-e','G','Raiz','-','1-1','-','Observação 1<br>linha 2'],
          ['2','A02','versao','Versão do leiaute','A','A01','C','1-1','4','Versão 4.00']]
    if second:rows[2][3]='Versão e estrutura atualizadas'
    if extra: rows.append(['3','A03','Id','Identificador','ID','A01','C','1-1','47',extra])
    return '<html><body><p>Atualizado até a NT 2026.008 v.1.01 publicada em 30/10/2026</p><h2>Grupo A. Dados da Nota Fiscal eletrônica</h2><table>'+head+''.join(tr(r) for r in rows)+'</table></body></html>'

class ImportTests(unittest.TestCase):
    def test_read_10_columns_group_and_observations(self):
        d=parse_moc(mock_doc()); self.assertEqual(len(d['nodes']),3)
        self.assertEqual(d['nodes'][1]['mocGroup'],'A')
        self.assertIn('linha 2',d['nodes'][1]['observation'])
        self.assertEqual(d['metadata']['technicalNote'],'NT 2026.008 v.1.01')
        self.assertEqual(d['nodes'][2]['order'],'2')
    def test_difference_includes_changes_without_reordering(self):
        a=parse_moc(mock_doc());b=parse_moc(mock_doc('nova regra',True))
        d=diff_catalogs(a,b)
        self.assertEqual(len(d),2)
        self.assertTrue(any(x['status']=='incluído' for x in d))
        self.assertTrue(any(x['status']=='alterado' for x in d))
    def test_quality_gate_prevents_deletion(self):
        old=parse_moc(mock_doc('novo'))
        new=parse_moc(mock_doc())
        with self.assertRaisesRegex(ValueError,'Redução inesperada'):
            quality_gate(new,old,min_rows=1,min_ratio=.80)
    def test_failed_fetch_preserves_current(self):
        with tempfile.TemporaryDirectory() as temp:
            fake=Path(temp);cur=fake/'catalogo_atual.json';cur.write_text('{"nodes":[{"id":"A01"}]}')
            with patch.object(monitor,'DATA',fake),patch.object(monitor,'LAST',cur),patch.object(monitor,'STATUS',fake/'status.json'),patch.object(monitor,'HISTORY',fake/'historico.json'):
                result=monitor.synchronize(lambda:'<html>site em manutenção</html>')
            self.assertTrue(result['preserved']);self.assertEqual(json.loads(cur.read_text())['nodes'][0]['id'],'A01')
    def test_xsd_import_and_local_include(self):
        main=b'''<?xml version="1.0"?><xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema"><xs:include schemaLocation="base.xsd"/><xs:element name="NFe" type="xs:string" minOccurs="1"/></xs:schema>'''
        sec=b'''<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema"><xs:simpleType name="Tipo"><xs:restriction base="xs:string"><xs:enumeration value="A"/></xs:restriction></xs:simpleType></xs:schema>'''
        out=io.BytesIO()
        with zipfile.ZipFile(out,'w') as z:z.writestr('main.xsd',main);z.writestr('base.xsd',sec)
        d=analyze_zip(out.getvalue());self.assertEqual(d['fileCount'],2)
        self.assertIn('resolvido',d['files'][0]['relations'][0]['status'])
        self.assertEqual(d['files'][1]['types'][0]['restrictions'][0]['value'],'A')
    def test_xsd_blocks_entity_expansion(self):
        payload=b'<!DOCTYPE a [<!ENTITY x SYSTEM "file:///etc/passwd">]><schema>&x;</schema>'
        buf=io.BytesIO()
        with zipfile.ZipFile(buf,'w') as z:z.writestr('malicioso.xsd',payload)
        with self.assertRaises(Exception):analyze_zip(buf.getvalue())

if __name__=='__main__':unittest.main(verbosity=2)
