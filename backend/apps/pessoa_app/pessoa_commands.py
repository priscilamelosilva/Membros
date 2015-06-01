# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from gaebusiness.gaeutil import SaveCommand, ModelSearchCommand
from gaeforms.ndb.form import ModelForm
from gaegraph.business_base import UpdateNode, NodeSearch, DeleteNode
from pessoa_app.pessoa_model import Pessoa



class PessoaSaveForm(ModelForm):
    """
    Form used to save and update Pessoa
    """
    _model_class = Pessoa
    _include = [Pessoa.cargo, 
                Pessoa.nome, 
                Pessoa.cpf, 
                Pessoa.rg, 
                Pessoa.telefone, 
                Pessoa.endereco, 
                Pessoa.data]


class PessoaForm(ModelForm):
    """
    Form used to expose Pessoa's properties for list or json
    """
    _model_class = Pessoa


class GetPessoaCommand(NodeSearch):
    _model_class = Pessoa


class DeletePessoaCommand(DeleteNode):
    _model_class = Pessoa


class SavePessoaCommand(SaveCommand):
    _model_form_class = PessoaSaveForm


class UpdatePessoaCommand(UpdateNode):
    _model_form_class = PessoaSaveForm


class ListPessoaCommand(ModelSearchCommand):
    def __init__(self):
        super(ListPessoaCommand, self).__init__(Pessoa.query_by_creation())

