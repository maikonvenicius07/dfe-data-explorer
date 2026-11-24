import json
import sys
from pathlib import Path
from xsd_catalog import analyze_zip
from catalog_core import atomic_json,now_utc
ROOT=Path(__file__).resolve().parents[1]
if len(sys.argv)<2:raise SystemExit('Uso: python scripts/import_xsd.py pacote-xsd.zip')
result=analyze_zip(Path(sys.argv[1]).read_bytes());result['importedAt']=now_utc()
atomic_json(ROOT/'data'/'xsd_catalogo.json',result)
print(json.dumps({'xsdFiles':result['fileCount'],'saved':'data/xsd_catalogo.json'},ensure_ascii=False))
