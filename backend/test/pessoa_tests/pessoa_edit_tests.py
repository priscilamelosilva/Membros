# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from base import GAETestCase
from datetime import datetime, date
from decimal import Decimal
from pessoa_app.pessoa_model import Pessoa
from routes.pessoas.edit import index, save
from mommygae import mommy
from tekton.gae.middleware.redirect import RedirectResponse


class IndexTests(GAETestCase):
    def test_success(self):
        pessoa = mommy.save_one(Pessoa)
        template_response = index(pessoa.key.id())
        self.assert_can_render(template_response)


class EditTests(GAETestCase):
    def test_success(self):
        pessoa = mommy.save_one(Pessoa)
        old_properties = pessoa.to_dict()
        redirect_response = save(pessoa.key.id(), cargo='cargo_string', nome='nome_string', cpf='cpf_string', rg='rg_string', telefone='telefone_string', endereco='endereco_string', data='data_string')
        self.assertIsInstance(redirect_response, RedirectResponse)
        edited_pessoa = pessoa.key.get()
        self.assertEquals('cargo_string', edited_pessoa.cargo)
        self.assertEquals('nome_string', edited_pessoa.nome)
        self.assertEquals('cpf_string', edited_pessoa.cpf)
        self.assertEquals('rg_string', edited_pessoa.rg)
        self.assertEquals('telefone_string', edited_pessoa.telefone)
        self.assertEquals('endereco_string', edited_pessoa.endereco)
        self.assertEquals('data_string', edited_pessoa.data)
        self.assertNotEqual(old_properties, edited_pessoa.to_dict())

    def test_error(self):
        pessoa = mommy.save_one(Pessoa)
        old_properties = pessoa.to_dict()
        template_response = save(pessoa.key.id())
        errors = template_response.context['errors']
        self.assertSetEqual(set(['cargo', 'nome', 'cpf', 'rg', 'telefone', 'endereco', 'data']), set(errors.keys()))
        self.assertEqual(old_properties, pessoa.key.get().to_dict())
        self.assert_can_render(template_response)
