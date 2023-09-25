# -*- coding: utf-8 -*-

import base64
from odoo import http
import werkzeug
from odoo.http import request
from odoo.addons.website.controllers import form

class ImageSalesWebsiteForm(form.WebsiteForm):

    @http.route(['/images'], type='http', auth="public", website=True)
    def website_sales_images_upload(self, **post):
        default_values = {}
        values = {}
        if request.env.user:
            default_values['user_id'] = request.env.user.id

        types = request.env['sales.configurator.type'].search([('name','=',"Images Upload")])

        values = {
            'default_values': default_values,
            'types': types}

        return request.render("pebble_sales_configurator.enphase_images_form", values )