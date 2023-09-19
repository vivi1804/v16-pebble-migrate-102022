# -*- coding: utf-8 -*-
from odoo import api, fields, models

class SalesConfig(models.Model):
    _name = 'sales.configurator'
    _inherit = ['mail.thread','mail.activity.mixin']
    _description = 'Sales Configurator for website'
    _order = 'id desc'
    
    name = fields.Char(string="Name")
    postcode = fields.Char(string="Postcode")
    huisnummer = fields.Char(string="Huisnummer")
    legplan = fields.Binary(string="Legplan")
    type_id = fields.One2many('sales.configurator.type', 'sales_configurator_ids', string="Type" )
    verkoper = fields.Many2one('res.users', string="User" )
    opportunity_id = fields.One2many('crm.lead', 'sale_configuration_ids', string="Opportunity")
    opportunity  = fields.Many2one('crm.lead', string="Opportunity")
    sequence = fields.Integer(string="Sequence")
    state = fields.Selection([('draft','Draft'),('confirm','Confirmed'),('cancel','Cancelled')], default='draft')
    notes = fields.Text(string="Customer notes")

    type_paneel = fields.Many2one('sales.configurator.type_paneel', string="Type Paneel" )
    aantal_panelen = fields.Integer(string="Aantal Panelen")
    type_frame = fields.Many2one('sales.configurator.type_frame', string="Type Frame" )
    aansluiting = fields.Selection([('1-fase','1-fase'),('3-fase','3-fase')], default='1-fase')
    aantal_eindstoppen = fields.Integer(string="Aantal Eindstoppen")
    foto_materkast = fields.Binary(string="Foto's Materkast")
    enyoy = fields.Selection([('metered','Metered'),('standaard','Standaard')], default='metered')

    steiger = fields.Selection([('ja','Ja'),('nee','Nee')])
    steiger_aantal_dagen = fields.Integer(string='Aantal dagen')
    steiger_aantal_meter = fields.Integer(string='Aantal meter')
    ladderlift = fields.Selection([('ja','Ja'),('nee','Nee')])
    ladderlift_aantal_dagen = fields.Integer(string='Aantal dagen')
    dakrandbeveiliging = fields.Selection([('ja','Ja'),('nee','Nee')])
    dak_aantal_dagen = fields.Integer(string='Aantal dagen')
    dak_aantal_meter = fields.Integer(string='Aantal meter')
    klein_materiaal = fields.Selection([('ja','Ja'),('nee','Nee')])
    klein_aantal_dagen = fields.Integer(string='Aantal dagen')
    verrijker = fields.Selection([('ja','Ja'),('nee','Nee')])
    verrijker_aantal_dagen = fields.Integer(string='Aantal dagen')
    
    def action_confirm(self):
        result = self.write({'state': 'confirm'})
        return result

    def action_cancel(self):
        result = self.write({'state': 'cancel'})
        return result

    step_1 = fields.Boolean(string = 'STEP 1', default=False)
    step_2 = fields.Boolean(string = 'STEP 2', default=False)
    step_3 = fields.Boolean(string = 'STEP 3', default=False)
    step_4 = fields.Boolean(string = 'STEP 4', default=False)
    opportunity_page = fields.Boolean(string = 'Opportunity', default=False)
    copy_attachment = fields.Boolean(string = 'Copy Attachement', default=False)
    create_so = fields.Boolean(string = 'Create SO', default=False)
    sales_configurator_type = fields.Many2one('sales.configurator.type', string="Type" )

    #Energie informatie
    powercon = fields.Float(string = 'Verbruik in kWh', digits=(8,0))
    desireprod = fields.Float(string = 'Gewenst vermogen', digits=(8,0))
    energycost = fields.Float(string = 'Huidige elektra prijs per kWh')
    elecprod = fields.Float(string='Productie naar schatting', digits=(8,2))
    grondkabel = fields.Float(string = 'Grondkabel')
    co2reduction = fields.Float(string='CO2 reductie', digits=(8,2))
    savings = fields.Float(string='Verwachtte besparing')

    #sales information 
    sales_condition_id = fields.Many2one('sale.template.conditions', string="Sales Condition" )
    aansluitwaarde = fields.Char(string="Aansluitwaarde")
    kabeltrace = fields.Char(string="Kabeltrace")
    levertijd = fields.Char(string="Levertijd")
    condition_txt = fields.Html(string="Condition")

    extra_dakvlakken_eenvoudig = fields.Integer(string="Extra dakvlakken eenvoudige")
    extra_dakvlakken_complex = fields.Integer(string="Extra dakvlakken complex")
    dakdoorvoer = fields.Boolean(string="Dakdoorvoer", default=False)

    paneel_ids = fields.One2many ('sales.configurator.paneel','sale_configurator_id', string="Paneel Lines" )
    frame_ids = fields.One2many ('sales.configurator.frame','sale_configurator_id', string="Frame Lines" )
    roof_ids = fields.One2many ('sales.configurator.roof','sale_configurator_id', string="Roof Lines" )

class SalesConfigType(models.Model):
    _name = 'sales.configurator.type'
    _description = 'Sales Configurator type for website'

    name = fields.Char(string="Name")
    sequence = fields.Integer(string="Sequence")
    sales_configurator_ids = fields.Many2one('sales.configurator', string="Sales Configurator")

class SalesConfigTypePaneel(models.Model):
    _name = 'sales.configurator.type_paneel'
    _description = 'Sales Configurator Product - Type Paneel'

    name = fields.Char(string="Name")
    sequence = fields.Integer(string="Sequence")
    product_id = fields.Many2one('product.product', string="Product")
    sale_configuration_ids = fields.One2many ('sales.configurator','type_paneel', string="Sales Configurator" )
    paneel_ids = fields.One2many ('sales.configurator.paneel','type_paneel', string="Paneel Lines" )

class SalesConfigTypeFrame(models.Model):
    _name = 'sales.configurator.type_frame'
    _description = 'Sales Configurator Product - Type Frame'

    name = fields.Char(string="Name")
    sequence = fields.Integer(string="Sequence")
    product_id = fields.Many2one('product.product', string="Product")
    sale_configuration_ids = fields.One2many ('sales.configurator','type_frame', string="Sales Configurator" )
    frame_ids = fields.One2many ('sales.configurator.frame','type_frame', string="Frame Lines" )

class UserSalesConfig(models.Model):
    _inherit="res.users"

    sale_configuration_ids = fields.One2many ('sales.configurator','verkoper', string="Sales Configurator" )

class CrmSalesConfig(models.Model):
    _inherit="crm.lead"

    sale_configuration_ids = fields.Many2one ('sales.configurator', string="Sales Configurator" )
    sale_configuration = fields.One2many ('sales.configurator', 'opportunity', string="Sales Configurator" )

class ProductSalesConfig(models.Model):
    _inherit="product.product"

    sales_configuration_type_paneel_ids = fields.One2many ('sales.configurator.type_paneel','product_id', string="Sales Configurator Type Paneel" )
    sales_configuration_type_frame_ids = fields.One2many ('sales.configurator.type_frame','product_id', string="Sales Configurator Type Frame" )

class CompanySalesConfig(models.Model):
    _inherit="res.company"

    instruction_html = fields.Html(string="Instruction")
    instruction_html_1 = fields.Html(string="Instruction Step 1")
    instruction_html_2 = fields.Html(string="Instruction Step 2")
    instruction_html_3 = fields.Html(string="Instruction Step 3")
    instruction_html_4 = fields.Html(string="Instruction Step 4")

class SalesConfigCondition(models.Model):
    _inherit="sale.template.conditions"

    sales_configurator_ids = fields.One2many ('sales.configurator', 'sales_condition_id', string="Sales Condition" )


class SalesConfigPaneel(models.Model):
    _name="sales.configurator.paneel"
    _description = "sales configurator paneel"

    type_paneel = fields.Many2one('sales.configurator.type_paneel', string="Type Paneel" )
    aantal_panelen = fields.Integer(string="Aantal Panelen")
    sale_configurator_id = fields.Many2one('sales.configurator', string="Sale Configurator" )

class SalesConfigFrame(models.Model):
    _name="sales.configurator.frame"
    _description = "sales configurator frame"

    type_frame = fields.Many2one('sales.configurator.type_frame', string="Type Frame" )
    aantal_frame = fields.Integer(string="Aantal Frame")
    sale_configurator_id = fields.Many2one('sales.configurator', string="Sale Configurator" )

class SalesConfigRoof(models.Model):
    _name="sales.configurator.roof"
    _description = "sales configurator roof"

    name = fields.Char(string="name")
    type = fields.Selection([('hellend','Hellend'),('plat','plat')])
    sale_configurator_id = fields.Many2one('sales.configurator', string="Sale Configurator" )

class SalesConditionConfig(models.Model):
    _inherit="sale.template.conditions"

    is_sales_configurator = fields.Boolean(string="Zichtbaar in product configurator", default= False)