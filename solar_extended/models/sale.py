#client_order_ref# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from PyPDF2 import PdfFileMerger, PdfFileReader
import tempfile
import os
import base64
import io
import math

class SaleOrderSolar(models.Model):
    _inherit = 'sale.order'

    order_type = fields.Selection([('default', 'Standaard Odoo'), ('default_no_price', 'Standaard Odoo - No Price Details'), ('b2c_solar', 'B2C Zonnepanelen report')], string='Type', default='default')

    #Attachment
    solar_pdf = fields.Binary(string="External Document", copy=False)
    solar_pdf_file = fields.Char(string="PDF File", copy=False)
    sale_condition_id = fields.Many2one("sale.template.conditions", "Verkoopvoorwaarden", copy=True)
    html_sale_conditions = fields.Html(compute='get_sale_condition_id', comodel_name='sale.template.conditions', store=True, copy=True)
    contact_person = fields.Many2one("res.partner", "Contact persoon")
    powercon = fields.Float('Verbruik in kWh', digits=(8,0))
    desireprod = fields.Float('Gewenst vermogen', digits=(8,0))
    energycost = fields.Monetary('Huidige elektra prijs per kWh', currency_field='currency_id', store=True)
    co2reduction = fields.Float(compute='getsum_total_elecprod', string='CO2 reductie', digits=(8,2), store=True)
    elecprod = fields.Float(compute='getsum_total_elecprod', string='Productie naar schatting', digits=(8,2), store=True)
    savings = fields.Monetary('Verwachtte besparing', currency_field='currency_id', store=True)
    forfair_vat = fields.Monetary(compute='get_net_investment', string='Forfair BTW bedrag', currency_field='currency_id', store=True)
    vat_reduction = fields.Monetary(compute='get_net_investment', string='BTW teruggave', currency_field='currency_id', store=True)
    net_investment = fields.Monetary(compute='get_net_investment', currency_field='currency_id', store=True)
    roi_years = fields.Float(compute='get_roi_in_years', string='ROI in jaren', store=True)
    roofdata_line_ids = fields.One2many('sale.roofdata.data', 'sale_id', string='Daken', copy=True)
    obstacles_line_ids = fields.One2many('sale.obstacles.data','sale_id', string ='Obstakels', copy=True)
    plan = fields.Image(string='Leg plan', readonly=False)
    client_order_ref = fields.Char(string='Customer Reference', copy=True)
    vat_reduction_type = fields.Selection([('yes', 'Ja'), ('no', 'Nee'), ('business', 'Zakelijk')], string='BTW terugvorderbaar', default='yes')
    vat_amount = fields.Monetary(compute='get_net_investment', currency_field='currency_id', readonly=False, store=True, string="BTW bedrag")


    @api.constrains('solar_pdf_file')
    def check_pdf_extension(self):
        if self.solar_pdf_file and not self.solar_pdf_file.endswith('.pdf'):
            raise ValidationError("File must be a .pdf file ")

    @api.onchange('sale_condition_id')
    def get_sale_condition_id(self):
        if self.sale_condition_id:
             self.html_sale_conditions = self.sale_condition_id.sale_condition

    def action_get_partner_roofdata(self):
        for rec in self:
            obs_lines = [(5,0,0)]
            roof_lines = [(5,0,0)]
            for obs_line in self.partner_id.obstacles_ids:
                obs_vals = {
                        'obstacles_id' : obs_line.id,
                        #'photo' : obs_line.photo
                }
                obs_lines.append((0,0, obs_vals))
            rec.obstacles_line_ids = obs_lines

            for roof_line in self.partner_id.roofdata_ids:
                roof_vals = {
                        'roofdata_id' : roof_line.id,
                        #'photo_1' : roof_line.photo_1,
                }
                roof_lines.append((0,0, roof_vals))
            rec.roofdata_line_ids = roof_lines

    @api.onchange('elecprod','energycost')   
    def getsum_total_elecprod(self):
        for rec in self:
            rec.co2reduction = rec.elecprod * 0.23314
            rec.savings = rec.elecprod * rec.energycost 

    @api.onchange('elecprod','amount_total', 'amount_tax', 'vat_reduction_type') 
    def get_net_investment(self):
        for rec in self:
            if rec.vat_reduction_type == "yes":
                #Calculate the forfair amount.
                forfair_rate = int(self.env['ir.config_parameter'].sudo().search([('key', '=', 'vat.forfair.amount.per.1000')]).value)
                max_amount = float(self.env['ir.config_parameter'].sudo().search([('key', '=', 'vat.forfair.max.order.amount')]).value)
 
                if rec.amount_untaxed > max_amount:
                    new_vat_amount = float(self.env['ir.config_parameter'].sudo().search([('key', '=', 'vat.forfair.max.vat.amount')]).value)
                else:
                    new_vat_amount = rec.amount_tax

                if not forfair_rate:
                    forfair_rate = 0.01

                total_wp = 0

                lines = self.order_line
                for line in lines:
                    if line.product_id.product_tmpl_id.wattpiek:
                        total_wp = total_wp + (line.product_id.product_tmpl_id.wattpiek * line.product_uom_qty)

                rounded_production = math.ceil(total_wp / 1000 )
                f_vat =  rounded_production * forfair_rate
                reduction = f_vat


                # Saving values in the fields
                rec.forfair_vat = f_vat
                rec.vat_amount = new_vat_amount
                rec.vat_reduction = new_vat_amount - f_vat

                rec.net_investment = rec.amount_total - new_vat_amount + f_vat 

            if rec.vat_reduction_type == "no":
                rec.vat_amount = rec.amount_tax
                rec.forfair_vat = 0
                rec.net_investment = rec.amount_total
                
            if rec.vat_reduction_type == "business":
                rec.vat_amount = rec.amount_tax
                rec.forfair_vat = 0
                rec.net_investment = rec.amount_untaxed

    @api.onchange('net_investment', 'energycost', 'elecprod', 'vat_reduction_type') 
    def get_roi_in_years(self):
        for rec in self:
            saving_year = rec.elecprod * rec.energycost 
            if saving_year > 0:
                raw_roi = rec.net_investment / saving_year
            else:
                raw_roi = 0
            rec.roi_years = round(raw_roi, 1)

class ProductSolar(models.Model):
    _inherit = 'product.template'

    html_product_details = fields.Html('Verk. omschr. deel 1')
    html_product_details_2 = fields.Html('Verk. omschr. deel 2')
    show_in_b2c = fields.Boolean(string="Zichtbaar in B2C raport")
    # wattpiek is pulled from module crm_order

class IrActionsReport(models.Model):
    _inherit = 'ir.actions.report'
    
    def _post_pdf(self, save_in_attachment, pdf_content=None, res_ids=None):
        res = super(IrActionsReport, self)._post_pdf(save_in_attachment, pdf_content, res_ids)
        
        if self.report_name in ('solar_extended.report_saleorder_document_solar', 'sale.report_saleorder'):
            streams = []
            
            for solar in self.env['sale.order'].browse(res_ids):
                if solar.solar_pdf:
                    print("Reading solar_pdf from record, ", solar.id)
                    streams.append(io.BytesIO(solar.solar_pdf))
            
            merger = PdfFileMerger(strict=False)
            
            for stream in streams:
                reader = PdfFileReader(stream)
                merger.append(reader, import_bookmarks=False)
            
            result_stream = io.BytesIO()
            merger.write(result_stream)
            result = result_stream.getvalue()
            
            return result
        
        return res

class solar_rooftype(models.Model):
    """A register class to create new menu"""
    _name = 'sale.rooftype'
    _description = "Basis tabel voor dak soorten"

    description = fields.Char('Daksoort', translate=True)
    
    def name_get(self):
        res = []
        for title in self:
            name = title.description
            res.append((title.id, name))
        return res

class solar_roofslope(models.Model):
    """A register class to create new menu"""
    _name = 'sale.roofslope'
    _description = "Basis tabel voor hellinggraden"

    degrees =  fields.Float('Hellingsgraad in graden', digits=(2,0))
    description = fields.Char('Hellingsgraad (omschr.)', translate=True)

    def name_get(self):
        res = []
        for title in self:
            name = title.description
            res.append((title.id, name))
        return res

class solar_roofcoverment(models.Model):
    """A register class to create new menu"""
    _name = 'sale.cover'
    _description = "Basis tabel voor dakbedekking"

    description = fields.Char('Dakbedekking', translate=True)

    def name_get(self):
        res = []
        for title in self:
            name = title.description
            res.append((title.id, name))
        return res

class solar_roofcolours(models.Model):
    """A register class to create new menu"""
    _name = 'sale.colour'
    _description = "Basis tabel voor dak kleuren"

    colour = fields.Char('Kleur', translate=True)

    def name_get(self):
        res = []
        for title in self:
            name = title.colour
            res.append((title.id, name))
        return res

class solar_compassdirection(models.Model):
    """A register class to create new menu"""
    _name = 'sale.compass'
    _description = "Basis tabel voor kompas richtingen"

    degrees = fields.Float('Kompas richting in graden', digits=(3,0))
    description = fields.Char('Kompas richting (omschr.)', translate=True)

    def name_get(self):
        res = []
        for title in self:
            name = title.description
            res.append((title.id, name))
        return res

class solar_tablehespul(models.Model):
    """A register class to create new menu"""
    _name = 'sale.tablehespul'
    _description = "Basis tabel voor tabel van Hespul"

    compass_degrees = fields.Float('Kompas richting in graden')
    roof_slope = fields.Float('Hellingsgraad')
    value = fields.Float('Waarde')

    def name_get(self):
        res = []
        for title in self:
            name = title.compass_degrees
            res.append((title.id, name))
        return res

class solar_obstacles(models.Model):
    """A register class to create new menu"""
    _name = 'sale.obstacles'
    _description = "Informatie van obstakels"

    description = fields.Char('Omschrijving')
    photo = fields.Image('Foto')
    partner_id = fields.Many2one('res.partner','Partner')

class solar_obstaclesdata(models.Model):
    """A register class to create new menu"""
    _name = 'sale.obstacles.data'
    _description = "Informatie van obstakels op het dak op een verkooporder"

    obstacles_id = fields.Many2one('sale.obstacles','Obstakel')
    description = fields.Char(related='obstacles_id.description', string='Omschrijving')
    photo = fields.Image(related='obstacles_id.photo', string='Foto')
    sale_id = fields.Many2one('sale.order','Sale')
    is_printed = fields.Boolean ('Afdrukken?', default=False)

class solar_roofdata(models.Model):
    _name = "sale.roofdata"
    _description = "Roof data"

    description = fields.Char('Omschrijving')
    compass_id = fields.Many2one('sale.compass','Kompas richting')
    roof_length = fields.Float('Lengte')
    roof_width = fields.Float('Breedte')
    rooftype = fields.Many2one('sale.rooftype','Type')
    roofcolour = fields.Many2one('sale.colour','Kleur')
    roofslope_id = fields.Many2one('sale.roofslope','Hellingsgraad')
    roofcover = fields.Many2one('sale.cover','Dakbedekking')
    roofheight = fields.Float('Goothoogte')
    sale_id = fields.Many2one('sale.order','Sale')
    partner_id = fields.Many2one('res.partner','Partner')

    #make the number of photo's irrelevant to the sales order?
    photo_1 = fields.Image('Foto')

    def name_get(self):
        res = []
        for title in self:
            name = title.partner_id.name
            res.append((title.id, name))
        return res

class solar_roofdatadata(models.Model):
    _name = "sale.roofdata.data"
    _description = "Collectie van dak informatie in verkooporder"

    roofdata_id = fields.Many2one('sale.roofdata','Dak informatie')
    description = fields.Char(related='roofdata_id.description', string='Omschrijving')
    compass_id = fields.Many2one(related='roofdata_id.compass_id', string='Kompas richting')
    roof_length = fields.Float(related='roofdata_id.roof_length', string='Lengte')
    roof_width = fields.Float(related='roofdata_id.roof_width', string='Breedte')
    rooftype = fields.Many2one(related ='roofdata_id.rooftype', string='Type')
    roofcolour = fields.Many2one(related='roofdata_id.roofcolour', spring='Kleur')
    roofslope_id = fields.Many2one(related='roofdata_id.roofslope_id', string='Hellingsgraad')
    roofcover = fields.Many2one(related='roofdata_id.roofcover', string='Dakbedekking')
    roofheight = fields.Float(related='roofdata_id.roofheight', string='Goothoogte')
    photo_1 = fields.Image(related='roofdata_id.photo_1', string='Foto')
    #photo_1 = fields.Image(string='Foto', readonly=False)

    sale_id = fields.Many2one('sale.order','Sale')
    is_printed = fields.Boolean ('Afdrukken?', default=False)

class solar_partner(models.Model):
    _inherit = "res.partner"

    roofdata_ids = fields.One2many('sale.roofdata', 'partner_id', 'Dak informatie')
    obstacles_ids = fields.One2many('sale.obstacles','partner_id', 'Obstakels')

    powercon = fields.Float('Energie verbruik', digits=(8,0))
    desireprod = fields.Float('Gewenst vermogen', digits=(8,0))