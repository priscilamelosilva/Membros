# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from base import GAETestCase
from datetime import datetime, date
from decimal import Decimal
from pessoa_app.pessoa_model import Pessoa
from routes.pessoas.new import index, save
from tekton.gae.middleware.redirect import RedirectResponse


class IndexTests(GAETestCase):
    def test_success(self):
        template_response = index()
        self.assert_can_render(template_response)


class SaveTests(GAETestCase):
    def test_success(self):
        self.assertIsNone(Pessoa.query().get())
        redirect_response = save(cargo='cargo_string', nome='nome_string', cpf='cpf_string', rg='rg_string', telefone='telefone_string', endereco='endereco_string', data='data_string')
        self.assertIsInstance(redirect_response, RedirectResponse)
        saved_pessoa = Pessoa.query().get()
        self.assertIsNotNone(saved_pessoa)
        self.assertEquals('cargo_string', saved_pessoa.cargo)
        self.assertEquals('nome_string', saved_pessoa.nome)
        self.assertEquals('cpf_string', saved_pessoa.cpf)
        self.assertEquals('rg_string', saved_pessoa.rg)
        self.assertEquals('telefone_string', saved_pessoa.telefone)
        self.assertEquals('endereco_string', saved_pessoa.endereco)
        self.assertEquals('data_string', saved_pessoa.data)

    def test_error(self):
        template_response = save()
        errors = template_response.context['errors']
        self.assertSetEqual(set(['cargo', 'nome', 'cpf', 'rg', 'telefone', 'endereco', 'data']), set(errors.keys()))
        self.assert_can_render(template_response)
