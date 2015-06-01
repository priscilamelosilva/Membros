# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from base import GAETestCase
from pessoa_app.pessoa_model import Pessoa
from routes.pessoas.home import index, delete
from gaebusiness.business import CommandExecutionException
from gaegraph.model import Node
from mommygae import mommy
from tekton.gae.middleware.redirect import RedirectResponse


class IndexTests(GAETestCase):
    def test_success(self):
        mommy.save_one(Pessoa)
        template_response = index()
        self.assert_can_render(template_response)


class DeleteTests(GAETestCase):
    def test_success(self):
        pessoa = mommy.save_one(Pessoa)
        redirect_response = delete(pessoa.key.id())
        self.assertIsInstance(redirect_response, RedirectResponse)
        self.assertIsNone(pessoa.key.get())

    def test_non_pessoa_deletion(self):
        non_pessoa = mommy.save_one(Node)
        self.assertRaises(CommandExecutionException, delete, non_pessoa.key.id())
        self.assertIsNotNone(non_pessoa.key.get())

