# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from gaebusiness.business import CommandExecutionException
from pessoa_app.pessoa_commands import PessoaForm
from tekton.gae.middleware.json_middleware import JsonResponse, JsonUnsecureResponse
from pessoa_app import pessoa_facade
from gaepermission.decorator import login_not_required

@login_not_required
def index():
    cmd = pessoa_facade.list_pessoas_cmd()
    pessoa_list = cmd()
    pessoa_form = pessoa_facade.pessoa_form()
    pessoa_dcts = [pessoa_form.fill_with_model(m) for m in pessoa_list]
    return JsonResponse(pessoa_dcts)


@login_not_required
def new(_resp, **pessoa_properties):
    cmd = pessoa_facade.save_pessoa_cmd(**pessoa_properties)
    return _save_or_update_json_response(cmd, _resp)


@login_not_required
def salvar(_resp, **propriedades):
    form = PessoaForm(**propriedades)
    erros = form.validate()
    if erros:
        _resp.set_status(400)
        return JsonUnsecureResponse(erros)
    pessoa = form.fill_model()
    pessoa.put()
    dct = form.fill_with_model(pessoa)
    log.info(dct)
    return JsonUnsecureResponse(dct)


@login_not_required
def edit(_resp, id, **pessoa_properties):
    cmd = pessoa_facade.update_pessoa_cmd(id, **pessoa_properties)
    return _save_or_update_json_response(cmd, _resp)


@login_not_required
def delete(_resp, id):
    cmd = pessoa_facade.delete_pessoa_cmd(id)
    try:
        cmd()
    except CommandExecutionException:
        _resp.status_code = 500
        return JsonResponse(cmd.errors)


@login_not_required
def _save_or_update_json_response(cmd, _resp):
    try:
        pessoa = cmd()
    except CommandExecutionException:
        _resp.status_code = 500
        return JsonResponse(cmd.errors)
    pessoa_form = pessoa_facade.pessoa_form()
    return JsonResponse(pessoa_form.fill_with_model(pessoa))

