"""Leitor offline de XSD (sem rede, DTD ou entidades externas)."""
from __future__ import annotations
import hashlib
import io
import json
from pathlib import Path
import zipfile
from defusedxml import ElementTree as ET
XS='{http://www.w3.org/2001/XMLSchema}'
FACETS=['enumeration','pattern','minLength','maxLength','length','minInclusive','maxInclusive','minExclusive','maxExclusive','totalDigits','fractionDigits','whiteSpace']
MAX_ZIP=100*1024*1024

def analyze_zip(data: bytes):
    if len(data)>MAX_ZIP:raise ValueError('ZIP excede 100 MB')
    with zipfile.ZipFile(io.BytesIO(data)) as z:
        entries=[e for e in z.infolist() if e.filename.lower().endswith('.xsd')]
        if len(entries)>400:raise ValueError('Excesso de arquivos XSD')
        if sum(e.file_size for e in entries)>MAX_ZIP:raise ValueError('Possível ZIP bomb')
        out=[]
        for ent in entries:
            if ent.file_size>10*1024*1024:raise ValueError('Arquivo XSD acima de 10 MB')
            src=z.read(ent)
            root=ET.fromstring(src)
            if root.tag!=XS+'schema':continue
            target=root.get('targetNamespace','')
            includes=[];elements=[];types=[]
            for rel in root.findall(XS+'include')+root.findall(XS+'import')+root.findall(XS+'redefine'):
                includes.append({'kind':rel.tag.split('}')[-1],'schemaLocation':rel.get('schemaLocation'),
                                 'namespace':rel.get('namespace')})
            def walk(t, ancestors=(), structure=()):
                local=t.tag.split('}')[-1]
                current=ancestors+((t.get('name') or t.get('ref') or ''),) if local in ('element','attribute') else ancestors
                structures=structure+((local,) if local in ('sequence','choice','all') else ())
                if local in ('element','attribute','simpleType','complexType'):
                    restrictions=[]
                    for x in t.iter():
                        if x.tag.startswith(XS) and x.tag.split('}')[-1] in FACETS:
                            restrictions.append({'facet':x.tag.split('}')[-1],'value':x.get('value')})
                    item={'tag':local,'name':t.get('name'),'ref':t.get('ref'),'type':t.get('type'),
                          'minOccurs':t.get('minOccurs'),'maxOccurs':t.get('maxOccurs'),
                          'use':t.get('use'),'restrictions':restrictions,'file':ent.filename,
                          'declarationPath':'/'.join(x for x in current if x),
                          'enclosingElement':ancestors[-1] if ancestors else None,
                          'structure':list(structures)}
                    if local in ('element','attribute'):elements.append(item)
                    else:types.append(item)
                for ch in t:
                    walk(ch,current,structures)
            walk(root)
            out.append({'file':ent.filename,'namespace':target,'sha256':hashlib.sha256(src).hexdigest(),
                        'relations':includes,'elements':elements,'types':types})
        if not out:raise ValueError('Nenhum arquivo XSD válido foi encontrado no pacote')
        known={e['file'] for e in out}
        # relative include paths (ZIP directory aware) are resolved only within the ZIP
        for f in out:
            for rel in f['relations']:
                target=rel['schemaLocation']
                if not target:rel['status']='sem local';continue
                from posixpath import normpath,dirname,join
                path=normpath(join(dirname(f['file']),target))
                rel['status']='resolvido localmente' if path in known else 'não encontrado no pacote'
        return {'source':'user-provided-xsd','files':out,'fileCount':len(out),
                'coverage':'XSD importados; junção MOC/XSD exige correspondência validada',
                'warning':'Includes externos não são buscados automaticamente'}
