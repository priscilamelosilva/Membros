from __future__ import absolute_import, unicode_literals
from config.template_middleware import TemplateResponse
from routes.novo_membro.home import MembroFormTable, Membro
from gaecookie.decorator import no_csrf
from gaepermission.decorator import login_required

__author__ = 'inspiron'


@login_required
@no_csrf
def index():
    query = Membro.query()
    membro_lista = query.fetch()
    form = MembroFormTable()
    membro_lista = [form.fill_with_model(membro) for membro in membro_lista]
    contexto = {'membro_lista':membro_lista}
    return TemplateResponse(contexto)