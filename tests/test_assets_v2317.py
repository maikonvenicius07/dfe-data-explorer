"""Static packaging contract (independent of browser/network policy)."""
from pathlib import Path
from html.parser import HTMLParser
R=Path(__file__).resolve().parents[1]
class Assets(HTMLParser):
    def __init__(self):super().__init__();self.urls=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag=='script' and a.get('src'):self.urls.append(a['src'])
        if tag=='link' and a.get('rel')=='stylesheet':self.urls.append(a['href'])
def test_assets():
    parser=Assets();parser.feed((R/'public/index.html').read_text());assert len(parser.urls)==5
    offline=(R/'public/EXPLORADOR_OFFLINE_COMPLETO.html').read_text()
    for url in parser.urls:
        path,version=url.split('?');assert version=='v=2.3.17'
        src=R/'public'/path;assert src.is_file();assert src.read_text().replace('</script','<\\/script') in offline
    assert 'V2.3.17' in offline and 'id="printMap"' in offline
if __name__=='__main__':test_assets();print('PASS: referências versionadas e conteúdo offline idêntico aos módulos.')
