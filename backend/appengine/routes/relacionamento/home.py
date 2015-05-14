from __future__ import absolute_import, unicode_literals
from google.appengine.ext import ndb
from routes.novo_membro.home import Membro
from gaecookie.decorator import no_csrf
from gaegraph.model import Arc
from gaepermission.decorator import login_required

__author__ = 'inspiron'


@login_required
@no_csrf
class Criador(Arc):
    origin = ndb.KeyProperty(required=True)
    destination = ndb.KeyProperty(Membro, required=True)