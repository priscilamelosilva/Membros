# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
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
    cmd = membro_facade.list_membros_cmd()
    membros = cmd()
    edit_path = router.to_path(edit)
    delete_path = router.to_path(delete)
    membro_form = membro_facade.membro_form()

    def localize_membro(membro):
        membro_dct = membro_form.fill_with_model(membro)
        membro_dct['edit_path'] = router.to_path(edit_path, membro_dct['id'])
        membro_dct['delete_path'] = router.to_path(delete_path, membro_dct['id'])
        return membro_dct

    localized_membros = [localize_membro(membro) for membro in membros]
    context = {'membros': localized_membros,
               'rest_new_path': router.to_path(rest.new)}
    return TemplateResponse(context, 'membros/membro_home.html')

@login_required
@no_csrf
def delete(membro_id):
    membro_facade.delete_membro_cmd(membro_id)()
    return RedirectResponse(router.to_path(index))

