from __future__ import absolute_import, unicode_literals
from config.template_middleware import TemplateResponse
from google.appengine.ext import ndb
from gaecookie.decorator import no_csrf
from gaeforms.ndb.form import ModelForm
from gaegraph.model import Node
from gaepermission.decorator import login_required
from tekton import router

__author__ = 'inspiron'


@login_required
@no_csrf
def index():
    contexto={'salvar_path':router.to_path(salvar)}
    return TemplateResponse(contexto)


class Membro(Node):
    nome = ndb.StringProperty(required=True)
    cpf = ndb.StringProperty(required=True)
    rg = ndb.StringProperty(required=True)
    data = ndb.DateProperty(required=True)
    endereco = ndb.StringProperty(required=True)
    telefone = ndb.StringProperty(required=True)
    cargo = ndb.StringProperty(required=True)

class MembroFormTable(ModelForm):
    _model_class = Membro
    _include = [Membro.nome, Membro.cpf, Membro.rg, Membro.data, Membro.endereco, Membro.telefone, Membro.cargo]


class MembroForm(ModelForm):
    _model_class = Membro
    _include = [Membro.nome, Membro.cpf, Membro.rg, Membro.data, Membro.endereco, Membro.telefone, Membro.cargo]


@login_required
@no_csrf
def salvar(_resp,**propriedades):
    membro_form = MembroForm(**propriedades)
    erros = membro_form.validate()
    if erros:
        contexto={'salvar_path':router.to_path(salvar),
                  'erros':erros,
                  'membro':membro_form}
        return TemplateResponse(contexto,'novo_membro/home.html')
    else:
        membro = membro_form.fill_model()
        membro.put()
        _resp.write('<html><body><font color = "green">Salvo com Sucesso!</font></body></html>')