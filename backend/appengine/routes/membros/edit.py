# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from config.template_middleware import TemplateResponse
from gaebusiness.business import CommandExecutionException
from tekton import router
from gaepermission.decorator import login_required
from gaecookie.decorator import no_csrf
from membro_app import membro_facade
from routes import membros
from tekton.gae.middleware.redirect import RedirectResponse

@login_required
@no_csrf
def index(membro_id):
    membro = membro_facade.get_membro_cmd(membro_id)()
    membro_form = membro_facade.membro_form()
    context = {'save_path': router.to_path(save, membro_id), 'membro': membro_form.fill_with_model(membro)}
    return TemplateResponse(context, 'membros/membro_form.html')


@login_required
@no_csrf
def save(membro_id, **membro_properties):
    cmd = membro_facade.update_membro_cmd(membro_id, **membro_properties)
    try:
        cmd()
    except CommandExecutionException:
        context = {'errors': cmd.errors, 'membro': membro_properties}

        return TemplateResponse(context, 'membros/membro_form.html')
    return RedirectResponse(router.to_path(membros))

