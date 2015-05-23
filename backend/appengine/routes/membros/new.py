# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from config.template_middleware import TemplateResponse
from gaebusiness.business import CommandExecutionException
from tekton import router
from gaecookie.decorator import no_csrf
from gaepermission.decorator import login_required
from membro_app import membro_facade
from routes import membros
from tekton.gae.middleware.redirect import RedirectResponse

@login_required
@no_csrf
def index():
    return TemplateResponse({'save_path': router.to_path(save)}, 'membros/membro_form.html')


@login_required
@no_csrf
def save(**membro_properties):
    cmd = membro_facade.save_membro_cmd(**membro_properties)
    try:
        cmd()
    except CommandExecutionException:
        context = {'errors': cmd.errors,
                   'membro': membro_properties}

        return TemplateResponse(context, 'membros/membro_form.html')
    return RedirectResponse(router.to_path(membros))

