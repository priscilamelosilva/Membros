# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from config.template_middleware import TemplateResponse
from gaebusiness.business import CommandExecutionException
from tekton import router
from gaecookie.decorator import no_csrf
from pessoa_app import pessoa_facade
from routes import pessoas
from tekton.gae.middleware.redirect import RedirectResponse


@no_csrf
def index():
    return TemplateResponse({'save_path': router.to_path(save)}, 'pessoas/pessoa_form.html')


def save(**pessoa_properties):
    cmd = pessoa_facade.save_pessoa_cmd(**pessoa_properties)
    try:
        cmd()
    except CommandExecutionException:
        context = {'errors': cmd.errors,
                   'pessoa': pessoa_properties}

        return TemplateResponse(context, 'pessoas/pessoa_form.html')
    return RedirectResponse(router.to_path(pessoas))

