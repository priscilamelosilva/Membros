from __future__ import absolute_import, unicode_literals
from config.template_middleware import TemplateResponse
from routes.novo_membro.home import MembroForm, Membro
from gaecookie.decorator import no_csrf
from gaepermission.decorator import login_required
from tekton import router

__author__ = 'inspiron'

@login_required
@no_csrf
def editar_form(membro_id):
    membro_id = int(membro_id)
    membro = Membro.get_by_id(membro_id)
    membro_form = MembroForm()
    membro_form.fill_with_model(membro)
    contexto= {'salvar_path':router.to_path(salvar, membro_id),
               'membro':membro_form}
    return TemplateResponse(contexto,'editar/home.html')


@login_required
@no_csrf
def salvar( _resp, membro_id, **propriedades):
    membro_id = int(membro_id)
    membro = Membro.get_by_id(membro_id)
    membro_form = MembroForm(**propriedades)
    erros = membro_form.validate()
    if erros:
        contexto = {'salvar_path':router.to_path(salvar),
                    'erros':erros,
                    'membro':membro_form}
        return TemplateResponse(contexto,'editar/home.html')
    else:
        membro_form.fill_model(membro)
        membro.put()
        _resp.write('<html><body><font color = "green">Atualizado com Sucesso!</font></body></html>')