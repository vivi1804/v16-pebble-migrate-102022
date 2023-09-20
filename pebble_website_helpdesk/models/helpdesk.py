# -*- coding: utf-8 -*-
from odoo import api, fields, models

class HelpdeskExt(models.Model):
    _inherit = 'helpdesk.ticket'

    postcode = fields.Char(string='Postcode')
    huisnummer = fields.Char(string='Huisnummer')