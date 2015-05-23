# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from base import GAETestCase
from membro_app.membro_model import Membro
from routes.membros.home import index, delete
from gaebusiness.business import CommandExecutionException
from gaegraph.model import Node
from mommygae import mommy
from tekton.gae.middleware.redirect import RedirectResponse


class IndexTests(GAETestCase):
    def test_success(self):
        mommy.save_one(Membro)
        template_response = index()
        self.assert_can_render(template_response)


class DeleteTests(GAETestCase):
    def test_success(self):
        membro = mommy.save_one(Membro)
        redirect_response = delete(membro.key.id())
        self.assertIsInstance(redirect_response, RedirectResponse)
        self.assertIsNone(membro.key.get())

    def test_non_membro_deletion(self):
        non_membro = mommy.save_one(Node)
        self.assertRaises(CommandExecutionException, delete, non_membro.key.id())
        self.assertIsNotNone(non_membro.key.get())

