# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import datetime

class CrmOrder(models.Model):
    _inherit = 'crm.lead'

    is_true = fields.Boolean(default=False)
    datum_aanvraag = fields.Date(string='Datum Aanvraag')
    datum_opname_verkoper = fields.Date(string='Datum Opname Verkoper')
    datum_eerste_offerte = fields.Date(string='Datum Eerste Offerte') 
    datum_conclusie = fields.Date(string='Datum conclusie (datum order, datum verloren)')
    order_datum = fields.Date(string='Order Datum')
    paneel_one = fields.Many2one('product.product', string='Paneel (1)')
    wattpiek_paneel_one = fields.Float(related='paneel_one.wattpiek', store=True,string='Wattpiek Paneel (1)', readonly=True)
    aantal_paneel_one = fields.Float(string='Aantal Panelen (1)')
    total_wattpiek_paneel_one = fields.Float(string='Total Wattpiek Paneel (1)',store=True, readonly=True)
    paneel_two = fields.Many2one('product.product', string='Paneel (2)')
    wattpiek_paneel_two = fields.Float(related='paneel_two.wattpiek', store=True,string='Wattpiek Paneel (2)', readonly=True)
    total_wattpiek_paneel_two = fields.Float(string='Total Wattpiek Paneel (2)',store=True, readonly=True)
    total_wattpiek_paneel = fields.Float(string='Total Wattpiek Paneel',store=True, readonly=True)
    aantal_paneel_two = fields.Float(string='Aantal Panelen (2)')
    hellend = fields.Boolean(string='Hellend', default=False)
    plat = fields.Boolean(string='Plat', default=False)
    veld = fields.Boolean(string='Veld', default=False)
    currency_id = fields.Many2one(
        'res.currency', 
        string='Currency',
        default=lambda self: self.env.user.company_id.currency_id, 
        readonly=True
    )
    omzet = fields.Float(string='Omzet')
    marge_voorcalculatie = fields.Float(string='Marge Voorcalculatie')
    aantal_dagen_installatie_voorcalculatie = fields.Float(string='Aantal Dagen Installatie Voorcalculatie')
    datum_ao = fields.Integer(string='Dagen tot opname', store=True, help="Het aantal dagen van binnenkomst lead tot opname")
    datum_ac = fields.Integer(string='Dagen tot conclusie', store=True, help="Het aantal dagen van binnenkomst lead tot conclusie")
    sales_order_id = fields.Many2one('sale.order', string="SO", store=True) 

    inverter_one = fields.Many2one('product.product', string='Omvormer 1')
    inverter_two = fields.Many2one('product.product', string='Omvormer 2')

    @api.onchange('wattpiek_paneel_one','aantal_paneel_one')   
    def getsum_total_wattpiek_paneel_one(self):
        self.total_wattpiek_paneel_one = self.wattpiek_paneel_one * self.aantal_paneel_one

    @api.onchange('wattpiek_paneel_two','aantal_paneel_two')   
    def getsum_total_wattpiek_paneel_two(self):
        self.total_wattpiek_paneel_two = self.wattpiek_paneel_two * self.aantal_paneel_two

    @api.onchange('total_wattpiek_paneel_one','total_wattpiek_paneel_two')   
    def getsum_total_wattpiek_paneel(self):
        self.total_wattpiek_paneel = self.total_wattpiek_paneel_one + self.total_wattpiek_paneel_two
 
    @api.onchange('datum_eerste_offerte', 'datum_aanvraag','datum_ao')
    def getsum_datum_ao(self):
        if self.datum_eerste_offerte and self.datum_aanvraag:
            d1=datetime.strptime(str(self.datum_eerste_offerte),'%Y-%m-%d') 
            d2=datetime.strptime(str(self.datum_aanvraag),'%Y-%m-%d')
            d3=d1-d2
            self.datum_ao=str(d3.days)

    @api.onchange('datum_conclusie', 'datum_aanvraag','datum_ac')
    def getsum_datum_ac(self):
        if self.datum_conclusie and self.datum_aanvraag:
            d1=datetime.strptime(str(self.datum_conclusie),'%Y-%m-%d') 
            d2=datetime.strptime(str(self.datum_aanvraag),'%Y-%m-%d')
            d3=d1-d2
            self.datum_ac=str(d3.days)

class CrmOrderProducts(models.Model):
    _inherit = 'product.template'

    wattpiek = fields.Float(string='Wattpiek', digits=(16, 0))
    st_zichtbaar_in_fieldservice = fields.Boolean(string='St.zichtbaar in fieldservice', default=False)