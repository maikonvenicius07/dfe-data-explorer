"""Gera o HTML independente diretamente dos arquivos da mesma versão.
Garante que o HTML offline não fique defasado do JavaScript da implantação.
"""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];PUBLIC=ROOT/'public'
html=(PUBLIC/'index.html').read_text(encoding='utf8')
html=html.replace('<link rel="stylesheet" href="./styles.css">', '<style>'+ (PUBLIC/'styles.css').read_text(encoding='utf8')+'</style>')
for name in ('selection.js','app.js'):
    html=html.replace(f'<script src="./{name}"></script>', '<script>'+ (PUBLIC/name).read_text(encoding='utf8').replace('</script','<\\/script')+'</script>')
(PUBLIC/'EXPLORADOR_OFFLINE_COMPLETO.html').write_text(html,encoding='utf8')
print('HTML offline gerado:',len(html),'caracteres')
