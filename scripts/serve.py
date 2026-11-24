"""Servidor opcional para hospedagem; HTML/CSS/JS também funcionam sem servidor."""
import json
import os
import sys
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse
from monitor import synchronize,ROOT,DATA,load
from xlsx_export import build_xlsx

PUBLIC=ROOT/'public'
ENDPOINTS={
 '/api/catalogo':DATA/'catalogo_atual.json',
 '/api/status':DATA/'status.json',
 '/api/historico':DATA/'historico.json',
 '/api/diferencas':DATA/'ultima_diferenca.json',
 '/api/xsd':DATA/'xsd_catalogo.json',
 '/api/notificacoes':DATA/'notificacoes.json'
}
class Handler(SimpleHTTPRequestHandler):
 def __init__(self,*args,**kwargs):super().__init__(*args,directory=str(PUBLIC),**kwargs)
 def reply(self,body,code=200):
  blob=json.dumps(body,ensure_ascii=False).encode('utf8')
  self.send_response(code);self.send_header('Content-Type','application/json; charset=utf-8')
  self.send_header('Content-Length',str(len(blob)));self.send_header('Cache-Control','no-store');self.send_header('X-Content-Type-Options','nosniff');self.end_headers();self.wfile.write(blob)
 def do_GET(self):
  path=urlparse(self.path).path
  if path=='/api/exportar/xlsx':
   obj=load(DATA/'catalogo_atual.json')
   if not obj:return self.reply({'error':'Sincronize o MOC para gerar XLSX oficial'},404)
   blob=build_xlsx(obj['nodes']);self.send_response(200)
   self.send_header('Content-Type','application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
   self.send_header('Content-Disposition','attachment; filename="dicionario_moc_nfe.xlsx"')
   self.send_header('Content-Length',str(len(blob)));self.end_headers();self.wfile.write(blob);return
  if path in ENDPOINTS:
   obj=load(ENDPOINTS[path],None)
   if obj is None:return self.reply({'error':'Ainda não existe versão oficial sincronizada neste servidor'},404)
   return self.reply(obj)
  if path=='/health':return self.reply({'status':'ok','service':'xsd-schema-explorer'})
  return super().do_GET()
 def do_POST(self):
  path=urlparse(self.path).path
  if path!='/api/atualizar':return self.reply({'error':'Endpoint não encontrado'},404)
  token=os.environ.get('ADMIN_TOKEN','')
  if not token:return self.reply({'error':'Operação bloqueada: defina ADMIN_TOKEN no ambiente'},403)
  import hmac
  if not hmac.compare_digest(self.headers.get('Authorization',''), 'Bearer '+token):
   return self.reply({'error':'Não autorizado'},401)
  result=synchronize()
  return self.reply(result,500 if result.get('error') else 200)

if __name__=='__main__':
 port=int(os.environ.get('PORT','8000'))
 print(f'Explorador NF-e / NFC-e em 0.0.0.0:{port}',flush=True)
 ThreadingHTTPServer(('0.0.0.0',port),Handler).serve_forever()
