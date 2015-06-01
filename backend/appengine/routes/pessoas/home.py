# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from json import dumps
from config.template_middleware import TemplateResponse
from tekton import router
from gaecookie.decorator import no_csrf
from pessoa_app import pessoa_facade
from routes.pessoas import new, edit
from tekton.gae.middleware.redirect import RedirectResponse
from gaepermission.decorator import login_not_required


@login_not_required
@no_csrf
def index():
    cmd = pessoa_facade.list_pessoas_cmd()
    pessoas = cmd()
    edit_path = router.to_path(edit)
    delete_path = router.to_path(delete)
    pessoa_form = pessoa_facade.pessoa_form()

    def localize_pessoa(pessoa):
        pessoa_dct = pessoa_form.fill_with_model(pessoa)
        pessoa_dct['edit_path'] = router.to_path(edit_path, pessoa_dct['id'])
        pessoa_dct['delete_path'] = router.to_path(delete_path, pessoa_dct['id'])
        return pessoa_dct

    localized_pessoas = [localize_pessoa(pessoa) for pessoa in pessoas]
    context = {'pessoas': dumps(localized_pessoas),
               'new_path': router.to_path(new)}
    return TemplateResponse(context, 'pessoas/pessoa_home.html')


def delete(pessoa_id):
    pessoa_facade.delete_pessoa_cmd(pessoa_id)()
    return RedirectResponse(router.to_path(index))

