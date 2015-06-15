# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from base import GAETestCase
from datetime import datetime, date
from decimal import Decimal
from config.template_middleware import TemplateResponse
from mock import Mock
from pessoa_app.pessoa_model import Pessoa
from routes.pessoas import new, rest
from routes.pessoas.new import index, save
from tekton.gae.middleware.redirect import RedirectResponse


class IndexTests(GAETestCase):
    def test_success(self):
        template_response = index()
        self.assert_can_render(template_response)


class SaveTests(GAETestCase):
    def test_success(self):
        resposta = new.save(cargo='cargo', nome='nome', cpf='cpf', rg='rg', telefone='telefone', endereco='endereco', data='data')
        self.assertIsInstance(resposta, RedirectResponse)
        self.assertEqual('/pessoas', resposta.context)
        saved_pessoa = Pessoa.query().fetch()
        self.assertEqual(1, len(saved_pessoa))
        pes = saved_pessoa[0]
        self.assertIsNotNone(saved_pessoa)
        self.assertEqual('cargo', pes.cargo)
        self.assertEqual('nome', pes.nome)
        self.assertEqual('cpf', pes.cpf)
        self.assertEqual('rg', pes.rg)
        self.assertEqual('telefone', pes.telefone)
        self.assertEqual('endereco', pes.endereco)
        self.assertEqual('data', pes.data)


    def test_validacao(self):
        resposta = new.save()
        self.assertIsInstance(resposta, TemplateResponse)
        self.assert_can_render(resposta)
        self.assertIsNone(Pessoa.query().get())
        self.maxDiff = None
        self.assertDictEqual({u'pessoa': {}, u'errors': {'cargo': u'Required field',
                            'cpf': u'Required field',
                            'data': u'Required field',
                            'endereco': u'Required field',
                            'nome': u'Required field',
                            'rg': u'Required field',
                            'telefone': u'Required field'}}, resposta.context)


    def test_json_error(self):
        resposta_mock = Mock()
        resposta = rest.salvar(resposta_mock)
        resposta_mock.set_status.assert_called_once_with(400)
        self.assert_can_serialize_as_json(resposta)
