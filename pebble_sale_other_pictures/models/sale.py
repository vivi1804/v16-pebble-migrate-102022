# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

class SaleOtherPictures(models.Model):
    _inherit = 'sale.order'

    other_pictures_line_ids = fields.One2many('sale.other.pictures.data','sale_id', string ='Other Pictures')

    def action_get_partner_roofdata(self):
        for rec in self:
            pict_lines = [(5,0,0)]
            for pict_line in self.partner_id.other_pictures_ids:
                pict_vals = {
                        'other_pictures_id' : pict_line.id,
                        #'photo' : pict_line.photo
                }
                pict_lines.append((0,0, pict_vals))
            rec.other_pictures_line_ids = pict_lines

class solar_other(models.Model):
    """A register class to create new menu"""
    _name = 'sale.other.pictures'
    _description = "Other Pictures"

    description = fields.Char('Omschrijving')
    photo = fields.Image('Foto')
    partner_id = fields.Many2one('res.partner','Partner')

class solar_otherdata(models.Model):
    """A register class to create new menu"""
    _name = 'sale.other.pictures.data'
    _description = "Sales Other Pictures"

    other_pictures_id = fields.Many2one('sale.other.pictures','Other Pictures')
    description = fields.Char(related='other_pictures_id.description', string='Omschrijving')
    photo = fields.Image(related='other_pictures_id.photo', string='Foto')
    sale_id = fields.Many2one('sale.order','Sale')
    is_printed = fields.Boolean ('Afdrukken?', default=False)

class solar_other_partner(models.Model):
    _inherit = "res.partner"

    other_pictures_ids = fields.One2many('sale.other.pictures', 'partner_id', 'Other Pictures')