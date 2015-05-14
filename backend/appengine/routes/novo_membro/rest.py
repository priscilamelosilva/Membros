# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from google.appengine.ext import ndb
from routes.novo_membro.home import MembroForm, Membro
from distutils import log
from gaecookie.decorator import no_csrf
from gaepermission.decorator import login_required, login_not_required
from tekton.gae.middleware.json_middleware import JsonUnsecureResponse


@login_not_required
@no_csrf
def salvar(_resp, **propriedades):
    membro_form = MembroForm(**propriedades)
    erros = membro_form.validate()
    if erros:
        _resp.set_status(400)
        return JsonUnsecureResponse(erros)
    membro = membro_form.fill_model()
    membro.put()
    dct = membro_form.fill_with_model(membro)
    log.info(dct)
    return JsonUnsecureResponse(dct)


@login_not_required
@no_csrf
def listar():
    query = Membro.query()
    membro = query.fetch()
    form = MembroForm()
    membros = [form.fill_with_model(m) for m in membro]
    return JsonUnsecureResponse(membros)


@login_not_required
@no_csrf
def deletar(membro_id):
    key = ndb.Key(Membro, int(membro_id))
    key.delete()




