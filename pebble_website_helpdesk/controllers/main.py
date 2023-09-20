# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from operator import truediv
from werkzeug.exceptions import NotFound
from werkzeug.utils import redirect

import json

from odoo import http, _
from odoo.http import request
from odoo.osv import expression
from odoo.addons.website.controllers.form import WebsiteForm


class WebsiteHelpdesk(http.Controller):

    def get_helpdesk_team_data(self, team, search=None):
        return {'team': team}

    @http.route(['/helpdesk', '/helpdesk/<model("helpdesk.team"):team>'], type='http', auth="public", website=True, sitemap=True)
    def website_helpdesk_teams(self, team=None, **kwargs):
        search = kwargs.get('search')

        teams_domain = [('use_website_helpdesk_form', '=', True)]
        if not request.env.user.has_group('helpdesk.group_helpdesk_manager'):
            if team and not team.is_published:
                raise NotFound()
            teams_domain = expression.AND([teams_domain, [('website_published', '=', True)]])

        if team and team.show_knowledge_base and not kwargs.get('contact_form'):
            return redirect(team.website_url + '/knowledgebase')

        teams = request.env['helpdesk.team'].search(teams_domain, order="id asc")
        if not teams:
            raise NotFound()
        
        types =  request.env['helpdesk.ticket.type'].search([])

        result = self.get_helpdesk_team_data(team or teams[0], search=search)
        result['multiple_teams'] = len(teams) > 1
        result['types'] = types
        return request.render("website_helpdesk.team", result)


    @http.route(['/create/ticket/<model_name>'], type='http', auth="public", website=True)
    def create_helpdesk_ticket(self, **kwargs):
        if kwargs.get('postcode') and kwargs.get('huisnummer'):
            postcode = kwargs.get('postcode') 
            huisnummer = kwargs.get('huisnummer')
            customer = "-".join([postcode.replace(" ",""), huisnummer.replace(" ","")])

            Partner = request.env['res.partner'].sudo().search([('name', '=', customer)])
            
            vals = {
                'postcode': postcode,
                'huisnummer': huisnummer,
                'name': "Website aanvrag",
            }

            request.env['helpdesk.ticket'].sudo().create(vals)
        return request.render("pebble_website_helpdesk.website_helpdesk_ticket_form_extended_team_1", {})


