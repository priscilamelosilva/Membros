# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from gaegraph.business_base import NodeSearch, DeleteNode
from membro_app.membro_commands import ListMembroCommand, SaveMembroCommand, UpdateMembroCommand, MembroForm,\
    GetMembroCommand, DeleteMembroCommand


def save_membro_cmd(**membro_properties):
    """
    Command to save Membro entity
    :param membro_properties: a dict of properties to save on model
    :return: a Command that save Membro, validating and localizing properties received as strings
    """
    return SaveMembroCommand(**membro_properties)


def update_membro_cmd(membro_id, **membro_properties):
    """
    Command to update Membro entity with id equals 'membro_id'
    :param membro_properties: a dict of properties to update model
    :return: a Command that update Membro, validating and localizing properties received as strings
    """
    return UpdateMembroCommand(membro_id, **membro_properties)


def list_membros_cmd():
    """
    Command to list Membro entities ordered by their creation dates
    :return: a Command proceed the db operations when executed
    """
    return ListMembroCommand()


def membro_form(**kwargs):
    """
    Function to get Membro's detail form.
    :param kwargs: form properties
    :return: Form
    """
    return MembroForm(**kwargs)


def get_membro_cmd(membro_id):
    """
    Find membro by her id
    :param membro_id: the membro id
    :return: Command
    """
    return GetMembroCommand(membro_id)



def delete_membro_cmd(membro_id):
    """
    Construct a command to delete a Membro
    :param membro_id: membro's id
    :return: Command
    """
    return DeleteMembroCommand(membro_id)

