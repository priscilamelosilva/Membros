# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from gaegraph.business_base import NodeSearch, DeleteNode
from pessoa_app.pessoa_commands import ListPessoaCommand, SavePessoaCommand, UpdatePessoaCommand, PessoaForm,\
    GetPessoaCommand, DeletePessoaCommand


def save_pessoa_cmd(**pessoa_properties):
    """
    Command to save Pessoa entity
    :param pessoa_properties: a dict of properties to save on model
    :return: a Command that save Pessoa, validating and localizing properties received as strings
    """
    return SavePessoaCommand(**pessoa_properties)


def update_pessoa_cmd(pessoa_id, **pessoa_properties):
    """
    Command to update Pessoa entity with id equals 'pessoa_id'
    :param pessoa_properties: a dict of properties to update model
    :return: a Command that update Pessoa, validating and localizing properties received as strings
    """
    return UpdatePessoaCommand(pessoa_id, **pessoa_properties)


def list_pessoas_cmd():
    """
    Command to list Pessoa entities ordered by their creation dates
    :return: a Command proceed the db operations when executed
    """
    return ListPessoaCommand()


def pessoa_form(**kwargs):
    """
    Function to get Pessoa's detail form.
    :param kwargs: form properties
    :return: Form
    """
    return PessoaForm(**kwargs)


def get_pessoa_cmd(pessoa_id):
    """
    Find pessoa by her id
    :param pessoa_id: the pessoa id
    :return: Command
    """
    return GetPessoaCommand(pessoa_id)



def delete_pessoa_cmd(pessoa_id):
    """
    Construct a command to delete a Pessoa
    :param pessoa_id: pessoa's id
    :return: Command
    """
    return DeletePessoaCommand(pessoa_id)

