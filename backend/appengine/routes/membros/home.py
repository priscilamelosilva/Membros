# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import json
from config.template_middleware import TemplateResponse
from tekton import router
from gaecookie.decorator import no_csrf
from gaepermission.decorator import login_required
from membro_app import membro_facade
from routes.membros import edit, rest
from tekton.gae.middleware.redirect import RedirectResponse

@login_required
@no_csrf
def index():
    context = {'rest_list_path': router.to_path(rest.index),
               'rest_delete_path': router.to_path(rest.delete),
               'rest_edit_path': router.to_path(rest.edit),
               'rest_new_path': router.to_path(rest.new)}
    return TemplateResponse(context, 'membros/membro_home.html')

@login_required
@no_csrf
def delete(membro_id):
    membro_facade.delete_membro_cmd(membro_id)()
    return RedirectResponse(router.to_path(index))

