# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from datetime import datetime, timedelta

class InvoiceFactuurType(models.Model):
    _inherit = 'account.move'

    factuur_type_id = fields.Many2one('account.move.factuur', 'Factuur Type')
    versturen_op =  fields.Date('Versturen OP', compute="getsum_calc_date", readonly=True, store=True)
    auto_versturen = fields.Boolean('Automatisch Versturen?', related='factuur_type_id.auto_versturen')
    install_datum =  fields.Date('Installatie datum')

    @api.depends('invoice_date', 'factuur_type_id.aantal_dagen','versturen_op')
    def getsum_calc_date(self):
        for rec in self:
            if rec.invoice_date:
                daysz = rec.factuur_type_id.aantal_dagen
                inv_date = fields.Date.from_string(rec.invoice_date) - timedelta(days=daysz)
                rec._origin.versturen_op = inv_date
            
class FactuurType(models.Model):
    _name = 'account.move.factuur'

    factuur_type = fields.Char('Name', required=True)
    aantal_dagen = fields.Float('Aantal Dagen')
    auto_versturen = fields.Boolean('Automatisch Versturen?')

    def name_get(self):
        res = []
        for title in self:
            name = title.factuur_type
            res.append((title.id, name))
        return res

