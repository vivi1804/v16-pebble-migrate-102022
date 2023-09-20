# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import http
from odoo.http import request
from odoo.addons.website.controllers import form

class WebsiteForm(form.WebsiteForm):

    @http.route('''/helpdesk/<model("helpdesk.team", "[('use_website_helpdesk_form','=',True)]"):team>/submit''', type='http', auth="public", website=True)
    def website_helpdesk_form(self, team, **kwargs):
        if not team.active or not team.website_published:
            return request.render("website_helpdesk.not_published_any_team")
        default_values = {}
        types = request.env['helpdesk.ticket.type'].sudo().search([])
        if request.env.user.partner_id != request.env.ref('base.public_partner'):
            default_values['name'] = request.env.user.partner_id.name
            default_values['email'] = request.env.user.partner_id.email
        return request.render("website_helpdesk_form.ticket_submit", {'team': team, 'default_values': default_values, 'types': types})

    @http.route('/website_form/<string:model_name>', type='http', auth="public", methods=['POST'], website=True)
    def website_form(self, model_name, **kwargs):
        if request.params.get('partner_email'):
            pass

        if request.params.get('postcode') and request.params.get('huisnummer'):
            postcode = request.params.get('postcode') 
            huisnummer = request.params.get('huisnummer')
            customer = "-".join([postcode.replace(" ",""), huisnummer.replace(" ","")])

            Partner = request.env['res.partner'].sudo().search([('name', '=', customer)])
            if Partner:
                request.params['partner_id'] = Partner.id
        return super(WebsiteForm, self).website_form(model_name, **kwargs)