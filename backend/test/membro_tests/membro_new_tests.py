# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from base import GAETestCase
from datetime import datetime, date
from decimal import Decimal
from membro_app.membro_model import Membro
from routes.membros.new import index, save
from tekton.gae.middleware.redirect import RedirectResponse


class IndexTests(GAETestCase):
    def test_success(self):
        template_response = index()
        self.assert_can_render(template_response)


class SaveTests(GAETestCase):
    def test_success(self):
        self.assertIsNone(Membro.query().get())
        redirect_response = save(cargo='cargo_string', nome='nome_string', cpf='cpf_string', rg='rg_string', telefone='telefone_string', endereco='endereco_string', data='1/7/2014')
        self.assertIsInstance(redirect_response, RedirectResponse)
        saved_membro = Membro.query().get()
        self.assertIsNotNone(saved_membro)
        self.assertEquals('cargo_string', saved_membro.cargo)
        self.assertEquals('nome_string', saved_membro.nome)
        self.assertEquals('cpf_string', saved_membro.cpf)
        self.assertEquals('rg_string', saved_membro.rg)
        self.assertEquals('telefone_string', saved_membro.telefone)
        self.assertEquals('endereco_string', saved_membro.endereco)
        self.assertEquals(date(2014, 1, 7), saved_membro.data)

    def test_error(self):
        template_response = save()
        errors = template_response.context['errors']
        self.assertSetEqual(set(['cargo', 'nome', 'cpf', 'rg', 'telefone', 'endereco', 'data']), set(errors.keys()))
        self.assert_can_render(template_response)
