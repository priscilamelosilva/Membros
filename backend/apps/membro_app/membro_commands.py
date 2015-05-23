# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from gaebusiness.gaeutil import SaveCommand, ModelSearchCommand
from gaeforms.ndb.form import ModelForm
from gaegraph.business_base import UpdateNode, NodeSearch, DeleteNode
from membro_app.membro_model import Membro



class MembroSaveForm(ModelForm):
    """
    Form used to save and update Membro
    """
    _model_class = Membro
    _include = [Membro.cargo, 
                Membro.nome, 
                Membro.cpf, 
                Membro.rg, 
                Membro.telefone, 
                Membro.endereco, 
                Membro.data]


class MembroForm(ModelForm):
    """
    Form used to expose Membro's properties for list or json
    """
    _model_class = Membro


class GetMembroCommand(NodeSearch):
    _model_class = Membro


class DeleteMembroCommand(DeleteNode):
    _model_class = Membro


class SaveMembroCommand(SaveCommand):
    _model_form_class = MembroSaveForm


class UpdateMembroCommand(UpdateNode):
    _model_form_class = MembroSaveForm


class ListMembroCommand(ModelSearchCommand):
    def __init__(self):
        super(ListMembroCommand, self).__init__(Membro.query_by_creation())

