# -*- coding: utf-8 -*-
import json
from odoo import http
from odoo.http import request
from odoo.tools.translate import _
from odoo.addons.http_routing.models.ir_http import unslug, slug
from bs4 import BeautifulSoup

class WebReferencesSnippet(http.Controller):
    @http.route(['/get_references'], type='json', auth='public', website=True)
    def get_references(self):
        domain = [('post_state','=','st_publish')]
        references = http.request.env['website.project.customer'].sudo().search(domain, limit=1, order='create_date desc')
        r = []

        for reference in references:

            ## CONVERT HTML TO TEXT
            soup = BeautifulSoup(reference.short_description, features='html.parser')
            txt_short_description = soup.get_text()
            post_cover = '/web/image?' + 'model=website.project.customer&id=' + str(reference.id) + '&field=project_image'
            post_url = slug(reference)

            refs = {
                "name": reference.name,
                "short_description": txt_short_description, 
                "cover": post_cover,
                "post_url": post_url,
            }
            r.append(refs)
        return r