# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from google.appengine.ext import ndb
from gaegraph.model import Node
from gaeforms.ndb import property


class Membro(Node):
    nome = ndb.StringProperty(required=True)
    cpf = ndb.StringProperty(required=True)
    rg = ndb.StringProperty(required=True)
    data = ndb.DateProperty(required=True)
    endereco = ndb.StringProperty(required=True)
    telefone = ndb.StringProperty(required=True)
    cargo = ndb.StringProperty(required=True)

