from __future__ import absolute_import, unicode_literals

from google.appengine.ext import ndb
from config.template_middleware import TemplateResponse
from gaecookie.decorator import no_csrf
from gaeforms.ndb.form import ModelForm
from gaegraph.model import Node, Arc
from gaepermission.decorator import login_required
from tekton import router


__author__ = 'inspiron'


@login_required
@no_csrf
def index():
    contexto={'salvar_path_agenda':router.to_path(salvar)}
    return TemplateResponse(contexto)


class Agenda(Node):
    nome = ndb.StringProperty(required=True)
    data = ndb.DateProperty(required=True)
    hora = ndb.StringProperty(required=True)
    telefone = ndb.StringProperty(required=True)
    igreja = ndb.StringProperty(required=True)
    assunto = ndb.StringProperty(required=True)

class AgendaFormTable(ModelForm):
    _model_class = Agenda
    _include = [Agenda.nome, Agenda.data, Agenda.hora, Agenda.telefone, Agenda.igreja, Agenda.assunto]


class AgendaForm(ModelForm):
    _model_class = Agenda
    _include = [Agenda.nome, Agenda.data, Agenda.hora, Agenda.telefone, Agenda.igreja, Agenda.assunto]



@login_required
@no_csrf
class Criador(Arc):
    origin = ndb.KeyProperty(required=True)
    destination = ndb.KeyProperty(Agenda, required=True)


@login_required
@no_csrf
def salvar(_resp, _logged_user, **propriedades):
    agenda_form = AgendaForm(**propriedades)
    erros = agenda_form.validate()
    if erros:
        contexto={'salvar_path_agenda':router.to_path(salvar),
                  'erros':erros,
                  'agenda':agenda_form}
        return TemplateResponse(contexto,'nova_agenda/home.html')
    else:
        agenda = agenda_form.fill_model()
        chave_de_membro = agenda.put()
        chave_de_usuario = _logged_user.key
        criador = Criador(origin=chave_de_usuario, destination=chave_de_membro)
        criador.put()
        _resp.write('<html><body><font color = "green">Salvo com Sucesso!</font></body></html>')