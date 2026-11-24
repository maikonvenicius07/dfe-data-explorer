"""Gerador XLSX mínimo, sem instalação de bibliotecas de planilhas no servidor.
Exportação de texto: preserva zeros à esquerda, IDs e códigos fiscais como texto.
"""
from io import BytesIO
from zipfile import ZipFile,ZIP_DEFLATED
from xml.sax.saxutils import escape
import re

HEADERS=['#','ID','Campo','Descrição','Ele','Pai','Tipo','Ocor.','Tam.','Observação','Grupo MOC']

def cell_addr(row,col):
    s='';col+=1
    while col: col,mod=divmod(col-1,26);s=chr(65+mod)+s
    return f'{s}{row}'

def sheet_xml(rows):
    parts=['<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
           '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"><sheetViews><sheetView workbookViewId="0"><pane ySplit="1" topLeftCell="A2" activePane="bottomLeft" state="frozen"/></sheetView></sheetViews>',
           '<cols><col min="1" max="3" width="13" customWidth="1"/><col min="4" max="4" width="55" customWidth="1"/><col min="5" max="9" width="13" customWidth="1"/><col min="10" max="10" width="65" customWidth="1"/><col min="11" max="11" width="17" customWidth="1"/></cols><sheetData>']
    for i,row in enumerate(rows,1):
        parts.append(f'<row r="{i}" ht="{25 if i==1 else 18}" customHeight="1">')
        for j,value in enumerate(row):
            val=str(value if value is not None else '')
            # Inline strings avoid implicit numeric conversion in Excel.
            val=escape(''.join(ch for ch in val if ord(ch)>=32 or ch in '\t\n\r'))
            parts.append(f'<c r="{cell_addr(i,j)}" t="inlineStr" s="{1 if i==1 else 0}"><is><t xml:space="preserve">{val}</t></is></c>')
        parts.append('</row>')
    parts.append('</sheetData><autoFilter ref="A1:K'+str(len(rows))+'"/></worksheet>')
    return ''.join(parts)

def build_xlsx(nodes):
    rows=[HEADERS]+[[n.get(k,'') for k in ('order','officialId','tag','description','kind','parent','type','occur','length','observation','mocGroup')] for n in nodes]
    content_types='''<?xml version="1.0" encoding="UTF-8"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/><Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/><Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/></Types>'''
    styles='''<?xml version="1.0" encoding="UTF-8"?><styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"><fonts count="2"><font><sz val="10"/><name val="Calibri"/></font><font><b/><sz val="10"/><color rgb="FFFFFFFF"/><name val="Calibri"/></font></fonts><fills count="3"><fill><patternFill patternType="none"/></fill><fill><patternFill patternType="gray125"/></fill><fill><patternFill patternType="solid"><fgColor rgb="FF245A7B"/><bgColor indexed="64"/></patternFill></fill></fills><borders count="1"><border><left/><right/><top/><bottom/><diagonal/></border></borders><cellStyleXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0"/></cellStyleXfs><cellXfs count="2"><xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0"/><xf numFmtId="0" fontId="1" fillId="2" borderId="0" xfId="0" applyFill="1" applyFont="1"/></cellXfs></styleSheet>'''
    buf=BytesIO()
    with ZipFile(buf,'w',ZIP_DEFLATED) as z:
        z.writestr('[Content_Types].xml',content_types)
        z.writestr('_rels/.rels','''<?xml version="1.0" encoding="UTF-8"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/></Relationships>''')
        z.writestr('xl/workbook.xml','''<?xml version="1.0" encoding="UTF-8"?><workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"><sheets><sheet name="Dicionario MOC" sheetId="1" r:id="rId1"/></sheets></workbook>''')
        z.writestr('xl/_rels/workbook.xml.rels','''<?xml version="1.0" encoding="UTF-8"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/><Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/></Relationships>''')
        z.writestr('xl/worksheets/sheet1.xml',sheet_xml(rows))
        z.writestr('xl/styles.xml',styles)
    return buf.getvalue()
