# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from gaebusiness.business import CommandExecutionException
from gaepermission.decorator import login_required
from tekton.gae.middleware.json_middleware import JsonResponse
from membro_app import membro_facade


@login_required
def index():
    cmd = membro_facade.list_membros_cmd()
    membro_list = cmd()
    membro_form = membro_facade.membro_form()
    membro_dcts = [membro_form.fill_with_model(m) for m in membro_list]
    return JsonResponse(membro_dcts)

@login_required
def new(_resp, **membro_properties):
    cmd = membro_facade.save_membro_cmd(**membro_properties)
    return _save_or_update_json_response(cmd, _resp)

@login_required
def edit(_resp, id, **membro_properties):
    cmd = membro_facade.update_membro_cmd(id, **membro_properties)
    return _save_or_update_json_response(cmd, _resp)

@login_required
def delete(_resp, id):
    cmd = membro_facade.delete_membro_cmd(id)
    try:
        cmd()
    except CommandExecutionException:
        _resp.status_code = 500
        return JsonResponse(cmd.errors)

@login_required
def _save_or_update_json_response(cmd, _resp):
    try:
        membro = cmd()
    except CommandExecutionException:
        _resp.status_code = 500
        return JsonResponse(cmd.errors)
    membro_form = membro_facade.membro_form()
    return JsonResponse(membro_form.fill_with_model(membro))

