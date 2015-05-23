# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from datetime import datetime, date
from decimal import Decimal
from base import GAETestCase
from membro_app.membro_model import Membro
from routes.membros import rest
from gaegraph.model import Node
from mock import Mock
from mommygae import mommy


class IndexTests(GAETestCase):
    def test_success(self):
        mommy.save_one(Membro)
        mommy.save_one(Membro)
        json_response = rest.index()
        context = json_response.context
        self.assertEqual(2, len(context))
        membro_dct = context[0]
        self.assertSetEqual(set(['id', 'creation', 'cargo', 'nome', 'cpf', 'rg', 'telefone', 'endereco', 'data']), set(membro_dct.iterkeys()))
        self.assert_can_serialize_as_json(json_response)


class NewTests(GAETestCase):
    def test_success(self):
        self.assertIsNone(Membro.query().get())
        json_response = rest.new(None, cargo='cargo_string', nome='nome_string', cpf='cpf_string', rg='rg_string', telefone='telefone_string', endereco='endereco_string', data='1/7/2014')
        db_membro = Membro.query().get()
        self.assertIsNotNone(db_membro)
        self.assertEquals('cargo_string', db_membro.cargo)
        self.assertEquals('nome_string', db_membro.nome)
        self.assertEquals('cpf_string', db_membro.cpf)
        self.assertEquals('rg_string', db_membro.rg)
        self.assertEquals('telefone_string', db_membro.telefone)
        self.assertEquals('endereco_string', db_membro.endereco)
        self.assertEquals(date(2014, 1, 7), db_membro.data)
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
        membro = mommy.save_one(Membro)
        old_properties = membro.to_dict()
        json_response = rest.edit(None, membro.key.id(), cargo='cargo_string', nome='nome_string', cpf='cpf_string', rg='rg_string', telefone='telefone_string', endereco='endereco_string', data='1/7/2014')
        db_membro = membro.key.get()
        self.assertEquals('cargo_string', db_membro.cargo)
        self.assertEquals('nome_string', db_membro.nome)
        self.assertEquals('cpf_string', db_membro.cpf)
        self.assertEquals('rg_string', db_membro.rg)
        self.assertEquals('telefone_string', db_membro.telefone)
        self.assertEquals('endereco_string', db_membro.endereco)
        self.assertEquals(date(2014, 1, 7), db_membro.data)
        self.assertNotEqual(old_properties, db_membro.to_dict())
        self.assert_can_serialize_as_json(json_response)

    def test_error(self):
        membro = mommy.save_one(Membro)
        old_properties = membro.to_dict()
        resp = Mock()
        json_response = rest.edit(resp, membro.key.id())
        errors = json_response.context
        self.assertEqual(500, resp.status_code)
        self.assertSetEqual(set(['cargo', 'nome', 'cpf', 'rg', 'telefone', 'endereco', 'data']), set(errors.keys()))
        self.assertEqual(old_properties, membro.key.get().to_dict())
        self.assert_can_serialize_as_json(json_response)


class DeleteTests(GAETestCase):
    def test_success(self):
        membro = mommy.save_one(Membro)
        rest.delete(None, membro.key.id())
        self.assertIsNone(membro.key.get())

    def test_non_membro_deletion(self):
        non_membro = mommy.save_one(Node)
        response = Mock()
        json_response = rest.delete(response, non_membro.key.id())
        self.assertIsNotNone(non_membro.key.get())
        self.assertEqual(500, response.status_code)
        self.assert_can_serialize_as_json(json_response)

