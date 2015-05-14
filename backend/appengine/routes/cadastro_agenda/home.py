from __future__ import absolute_import, unicode_literals
from config.template_middleware import TemplateResponse
from gaecookie.decorator import no_csrf
from gaepermission.decorator import login_required

__author__ = 'inspiron'

@login_required
@no_csrf
def index():
    return TemplateResponse(template_path='/nova_agenda/home.html')