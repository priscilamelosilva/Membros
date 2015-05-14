from __future__ import absolute_import, unicode_literals
from google.appengine.ext import ndb
from routes.novo_membro.home import Membro
from gaecookie.decorator import no_csrf
from gaepermission.decorator import login_required
from tekton.gae.middleware.redirect import RedirectResponse
from tekton.router import to_path


__author__ = 'inspiron'

@login_required
@no_csrf
def delete_form(membro_id):
    chave = ndb.Key(Membro, int(membro_id))
    chave.delete()
    return RedirectResponse(to_path(index))

@login_required
@no_csrf
def index(_resp):
    _resp.write('<html><body><font color = "red">Excluido com Sucesso!</font></body></html>')
