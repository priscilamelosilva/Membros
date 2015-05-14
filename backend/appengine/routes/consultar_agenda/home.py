from __future__ import absolute_import, unicode_literals

from google.appengine.ext import ndb
from config.template_middleware import TemplateResponse
from routes.nova_agenda.home import Criador, AgendaFormTable
from gaecookie.decorator import no_csrf
from gaepermission.decorator import login_required


__author__ = 'inspiron'

@login_required
@no_csrf
def index(_logged_user):
    chave_do_usuario=_logged_user.key
    query = Criador.query(Criador.origin==chave_do_usuario)
    criador_agenda=query.fetch()
    chaves_agenda=[arco.destination for arco in criador_agenda]
    agenda_lista=ndb.get_multi(chaves_agenda)
    form = AgendaFormTable()
    agenda_lista=[form.fill_with_model(agenda) for agenda in agenda_lista]
    contexto = {'agenda_lista':agenda_lista}
    return TemplateResponse(contexto, 'consulta_agenda/home.html')