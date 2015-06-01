# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from datetime import datetime, date
from decimal import Decimal
from base import GAETestCase
from pessoa_app.pessoa_model import Pessoa
from routes.pessoas import rest
from gaegraph.model import Node
from mock import Mock
from mommygae import mommy


class IndexTests(GAETestCase):
    def test_success(self):
        mommy.save_one(Pessoa)
        mommy.save_one(Pessoa)
        json_response = rest.index()
        context = json_response.context
        self.assertEqual(2, len(context))
        pessoa_dct = context[0]
        self.assertSetEqual(set(['id', 'creation', 'cargo', 'nome', 'cpf', 'rg', 'telefone', 'endereco', 'data']), set(pessoa_dct.iterkeys()))
        self.assert_can_serialize_as_json(json_response)


class NewTests(GAETestCase):
    def test_success(self):
        self.assertIsNone(Pessoa.query().get())
        json_response = rest.new(None, cargo='cargo_string', nome='nome_string', cpf='cpf_string', rg='rg_string', telefone='telefone_string', endereco='endereco_string', data='data_string')
        db_pessoa = Pessoa.query().get()
        self.assertIsNotNone(db_pessoa)
        self.assertEquals('cargo_string', db_pessoa.cargo)
        self.assertEquals('nome_string', db_pessoa.nome)
        self.assertEquals('cpf_string', db_pessoa.cpf)
        self.assertEquals('rg_string', db_pessoa.rg)
        self.assertEquals('telefone_string', db_pessoa.telefone)
        self.assertEquals('endereco_string', db_pessoa.endereco)
        self.assertEquals('data_string', db_pessoa.data)
        self.assert_can_serialize_as_json(json_response)

    def test_error(self):
        resp = Mock()
        json_response = rest.new(resp)
        errors = json_response.context
        self.assertEqual(500, resp.status_code)
        self.assertSetEqual(set(['cargo', 'nome', 'cpf', 'rg', 'telefone', 'endereco', 'data']), set(errors.keys()))
        self.assert_can_serialize_as_json(json_response)


class EditTests(GAETestCase):
    def test_success(self):
        pessoa = mommy.save_one(Pessoa)
        old_properties = pessoa.to_dict()
        json_response = rest.edit(None, pessoa.key.id(), cargo='cargo_string', nome='nome_string', cpf='cpf_string', rg='rg_string', telefone='telefone_string', endereco='endereco_string', data='data_string')
        db_pessoa = pessoa.key.get()
        self.assertEquals('cargo_string', db_pessoa.cargo)
        self.assertEquals('nome_string', db_pessoa.nome)
        self.assertEquals('cpf_string', db_pessoa.cpf)
        self.assertEquals('rg_string', db_pessoa.rg)
        self.assertEquals('telefone_string', db_pessoa.telefone)
        self.assertEquals('endereco_string', db_pessoa.endereco)
        self.assertEquals('data_string', db_pessoa.data)
        self.assertNotEqual(old_properties, db_pessoa.to_dict())
        self.assert_can_serialize_as_json(json_response)

    def test_error(self):
        pessoa = mommy.save_one(Pessoa)
        old_properties = pessoa.to_dict()
        resp = Mock()
        json_response = rest.edit(resp, pessoa.key.id())
        errors = json_response.context
        self.assertEqual(500, resp.status_code)
        self.assertSetEqual(set(['cargo', 'nome', 'cpf', 'rg', 'telefone', 'endereco', 'data']), set(errors.keys()))
        self.assertEqual(old_properties, pessoa.key.get().to_dict())
        self.assert_can_serialize_as_json(json_response)


class DeleteTests(GAETestCase):
    def test_success(self):
        pessoa = mommy.save_one(Pessoa)
        rest.delete(None, pessoa.key.id())
        self.assertIsNone(pessoa.key.get())

    def test_non_pessoa_deletion(self):
        non_pessoa = mommy.save_one(Node)
        response = Mock()
        json_response = rest.delete(response, non_pessoa.key.id())
        self.assertIsNotNone(non_pessoa.key.get())
        self.assertEqual(500, response.status_code)
        self.assert_can_serialize_as_json(json_response)

