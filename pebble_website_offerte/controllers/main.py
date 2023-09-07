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
        postcode = request.params.get('x_studio_postcode')
        huisnummer = request.params.get('x_studio_huisnummer')
        name = "-".join([postcode, huisnummer])

        if name:
            kwargs['name'] = name

        #     request.env['crm.lead'].sudo().create({
        #         'name': name,
        #         'x_studio_titel': request.params.get('x_studio_titel'),
        #         'x_studio_voornaam': request.params.get('x_studio_voornaam'),
        #         'x_studio_achternaam': request.params.get('x_studio_achternaam'),
        #         'x_studio_postcode': postcode,
        #         'x_studio_huisnummer': huisnummer,
        #         'x_studio_dak_orientatie': request.params.get('x_studio_dak_orientatie'),
        #         'x_studio_investeringsredenen': request.params.get('x_studio_investeringsredenen'),
        #         'x_studio_energie_verbruik_per_jaar': request.params.get('x_studio_energie_verbruik_per_jaar'),
        #         'x_studio_zonnepanelen_': request.params.get('x_studio_zonnepanelen_'),
        #         'x_studio_infraroodverwarming_': request.params.get('x_studio_infraroodverwarming_'),
        #         'x_studio_laadpaal_': request.params.get('x_studio_laadpaal_'),
        #         'medium_id': request.params.get('medium_id'),
        #     })

            return super(WebsiteForm, self)._handle_website_form(model_name, **kwargs)