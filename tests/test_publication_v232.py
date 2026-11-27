"""Regressão: o Pages deve abrir o aplicativo, com quatro telas acessíveis e quatro módulos internos."""
from pathlib import Path
from html.parser import HTMLParser

R = Path(__file__).resolve().parents[1]
VIEWS = {'oracle', 'atualizacoes', 'impressao'}
DOCUMENT_VIEWS = {'moc', 'pending'}
INTERNAL = {'arvore', 'dicionario', 'diagrama', 'xsd'}

class Tags(HTMLParser):
    def __init__(self):
        super().__init__()
        self.menu = []
        self.documents = []
        self.context = []
        self.sections = []
        self.active_menu = []
        self.active_sections = []
        self.hidden_sections = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'button' and 'data-document' in a:
            self.documents.append(a['data-document'])
        if tag == 'button' and 'data-goto' in a:
            self.context.append(a['data-goto'])
        if tag == 'button' and 'data-view' in a:
            self.menu.append(a['data-view'])
            if 'active' in a.get('class', '').split():
                self.active_menu.append(a['data-view'])
        if tag == 'section' and a.get('id', '').startswith('view-'):
            view = a['id'][5:]
            self.sections.append(view)
            if 'hidden' in a and 'inert' in a:
                self.hidden_sections.append(view)
            if 'active' in a.get('class', '').split():
                self.active_sections.append(view)


def test_entrada_pages_modo_branch():
    # Branch main /root: precisa abrir o aplicativo e NÃO o README.
    content = (R / 'index.html').read_text(encoding='utf-8')
    assert 'url=./public/' in content
    assert 'href="./public/"' in content
    assert (R / 'public/index.html').is_file()
    assert (R / '.nojekyll').is_file()


def test_quatro_telas_publicas_e_modulos_internos():
    for name in ('index.html', 'EXPLORADOR_OFFLINE_COMPLETO.html'):
        t = Tags()
        t.feed((R / 'public' / name).read_text(encoding='utf-8'))
        assert set(t.menu) == VIEWS, (name, t.menu)
        assert len(t.menu) == len(VIEWS)
        assert set(t.sections) == VIEWS | INTERNAL | DOCUMENT_VIEWS, (name, t.sections)
        assert len(t.sections) == len(VIEWS | INTERNAL | DOCUMENT_VIEWS)
        assert set(t.hidden_sections) == INTERNAL | {'pending'}
        assert t.active_menu == []
        assert t.documents == ['nfe']
        assert INTERNAL.issubset(t.context)
        assert t.active_sections == ['moc']
        assert 'resumo' not in t.menu
        assert 'resumo' not in t.sections


def test_workflow_github_pages_e_validacao():
    workflow = (R / '.github/workflows/publicar_paginas.yml').read_text(encoding='utf-8')
    assert "      - 'public/**'" in workflow
    assert "      - 'index.html'" in workflow
    assert 'actions/upload-pages-artifact@v4' in workflow
    assert 'actions/deploy-pages@v4' in workflow
    assert 'path: _site' in workflow
    assert 'cp -a public _site/public' in workflow
