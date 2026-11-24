"""Copia snapshots validados ao site estático. Nunca inventa dados oficiais.
Use após monitor.py para preparar public/ para GitHub Pages.
"""
from pathlib import Path
import json, shutil
ROOT=Path(__file__).resolve().parents[1]
PUBLIC=ROOT/'public'/'data';DATA=ROOT/'data';PUBLIC.mkdir(parents=True,exist_ok=True)
for name in ('catalogo_atual.json','status.json','historico.json','ultima_diferenca.json','xsd_catalogo.json','notificacoes.json'):
    src=DATA/name
    if src.is_file():
        try: json.loads(src.read_text(encoding='utf8'))
        except (ValueError,UnicodeDecodeError) as exc: raise SystemExit(f'JSON inválido ({name}): {exc}')
        shutil.copyfile(src,PUBLIC/name)
        print('Exportado:',name)
print('Site estático preparado; sem base oficial validada, a interface permanece demonstrativa.')
