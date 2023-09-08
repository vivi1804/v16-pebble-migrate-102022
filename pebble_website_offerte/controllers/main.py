# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
from odoo.addons.website.controllers import form

class WebsiteOfferte(http.Controller):
    
    @http.route('/offerte', auth='public', website=True)
    def pebble_offerte(self, **kw):

        return request.render('pebble_website_offerte.offerte', {'str': "test"})
    
class WebsiteForm(form.WebsiteForm):

    def _handle_website_form(self, model_name, **kwargs):
            
            return super(WebsiteForm, self)._handle_website_form(model_name, **kwargs)