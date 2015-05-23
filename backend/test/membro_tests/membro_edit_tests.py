# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from base import GAETestCase
from datetime import datetime, date
from decimal import Decimal
from membro_app.membro_model import Membro
from routes.membros.edit import index, save
from mommygae import mommy
from tekton.gae.middleware.redirect import RedirectResponse


class IndexTests(GAETestCase):
    def test_success(self):
        membro = mommy.save_one(Membro)
        template_response = index(membro.key.id())
        self.assert_can_render(template_response)


class EditTests(GAETestCase):
    def test_success(self):
        membro = mommy.save_one(Membro)
        old_properties = membro.to_dict()
        redirect_response = save(membro.key.id(), cargo='cargo_string', nome='nome_string', cpf='cpf_string', rg='rg_string', telefone='telefone_string', endereco='endereco_string', data='1/7/2014')
        self.assertIsInstance(redirect_response, RedirectResponse)
        edited_membro = membro.key.get()
        self.assertEquals('cargo_string', edited_membro.cargo)
        self.assertEquals('nome_string', edited_membro.nome)
        self.assertEquals('cpf_string', edited_membro.cpf)
        self.assertEquals('rg_string', edited_membro.rg)
        self.assertEquals('telefone_string', edited_membro.telefone)
        self.assertEquals('endereco_string', edited_membro.endereco)
        self.assertEquals(date(2014, 1, 7), edited_membro.data)
        self.assertNotEqual(old_properties, edited_membro.to_dict())

    def test_error(self):
        membro = mommy.save_one(Membro)
        old_properties = membro.to_dict()
        template_response = save(membro.key.id())
        errors = template_response.context['errors']
        self.assertSetEqual(set(['cargo', 'nome', 'cpf', 'rg', 'telefone', 'endereco', 'data']), set(errors.keys()))
        self.assertEqual(old_properties, membro.key.get().to_dict())
        self.assert_can_render(template_response)
