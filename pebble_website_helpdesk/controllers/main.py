# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from werkzeug.exceptions import NotFound
from werkzeug.utils import redirect

import json
import base64
from psycopg2 import IntegrityError

from odoo import http, _
from odoo.http import request
from odoo.osv import expression
from odoo.exceptions import ValidationError
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
        
        types =  request.env['helpdesk.ticket.type'].sudo().search([])

        result = self.get_helpdesk_team_data(team or teams[0], search=search)
        result['multiple_teams'] = len(teams) > 1
        result['types'] = types
        return request.render("website_helpdesk.team", result)

class CustomWebsiteForm(WebsiteForm):

    @http.route(['/website/form/<model_name>'], type='http', auth="public", website=True, sitemap=True)
    def _handle_website_form(self, model_name, **kwargs):
        if model_name == "helpdesk.ticket":
            if kwargs.get('postcode') and kwargs.get('huisnummer'):
                postcode = kwargs.get('postcode').replace(" ", "")
                huisnummer = kwargs.get('huisnummer').replace(" ", "")
                partner_name = "-".join([postcode, huisnummer])

                Partner = request.env['res.partner'].sudo().search([('name','=', partner_name)], limit=1)
                if not Partner:
                    Partner = request.env['res.partner'].sudo().create({
                        'name': partner_name,
                        'email': kwargs.get('partner_email'),
                        'zip': postcode,
                        'street_number': huisnummer,
                    })

            # Create the helpdesk ticket
            ticket = request.env['helpdesk.ticket'].sudo().create({
                'name': kwargs.get('name'),
                'partner_id': Partner.id,
                'postcode': postcode,
                'huisnummer': huisnummer,
                'partner_name': kwargs.get('partner_name'),
                'partner_email': kwargs.get('partner_email'),
                'description': kwargs.get('description'),
                'ticket_type_id': kwargs.get('ticket_type_id'),
            })

            model_record = request.env['ir.model'].sudo().search([('model', '=', model_name)]) 
            data = self.extract_data(model_record, request.params)
            attached_files = data.get('attachments')
            for attachment in attached_files:
                attached_file = attachment.read()
                request.env['ir.attachment'].sudo().create({
                    'name': attachment.filename,
                    'res_model': 'helpdesk.ticket',
                    'res_id': ticket.id,
                    'type': 'binary',
                    'datas': base64.encodebytes(attached_file),
                })

            # Send an email message using an email template
            template_id = request.env.ref('helpdesk.new_ticket_request_email_template').id  # Replace with the actual template ID
            template = request.env['mail.template'].sudo().browse(template_id)
            template.send_mail(ticket.id, force_send=True)

            request.session['form_builder_model_model'] = model_record.model
            request.session['form_builder_model'] = model_record.name
            request.session['form_builder_id'] = ticket.id
            return json.dumps({'id': ticket.id})
        else:
            model_record = request.env['ir.model'].sudo().search(
                [('model', '=', model_name)])
            if not model_record:
                return json.dumps({
                    'error': _("The form's specified model does not exist")
                })
            try:
                data = self.extract_data(model_record, request.params)
            # If we encounter an issue while extracting data
            except ValidationError as e:
                return json.dumps({'error_fields': e.args[0]})
            try:
                id_record = self.insert_record(request, model_record,
                                               data['record'], data['custom'],
                                               data.get('meta'))
                if id_record:
                    self.insert_attachment(model_record, id_record,
                                           data['attachments'])
                    # in case of an email, we want to send it immediately instead of waiting
                    # for the email queue to process
                    if model_name == 'mail.mail':
                        request.env[model_name].sudo().browse(id_record).send()

            # Some fields have additional SQL constraints that we can't check generically
            # Ex: crm.lead.probability which is a float between 0 and 1
            # TODO: How to get the name of the erroneous field ?
            except IntegrityError:
                return json.dumps(False)

            request.session['form_builder_model_model'] = model_record.model
            request.session['form_builder_model'] = model_record.name
            request.session['form_builder_id'] = id_record

            return json.dumps({'id': id_record})
