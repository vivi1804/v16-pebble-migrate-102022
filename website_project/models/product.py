# -*- coding: utf-8 -*-
from email.policy import default
from odoo import api, fields, models

class ProductWebsite(models.Model):
    _inherit = ['product.template']
    
    website_category_ids = fields.Many2many('website.product.category', 'website_product_category_rel', 'category_id', 'product_id', 
                                            string="Website Product Category" )
    short_description = fields.Html(string="Short Description")
    long_description = fields.Html(string="Long Description")
    published = fields.Boolean(string="Published", default=False, track_visibility='onchange')

class ProductWebsiteCategory(models.Model):
    _name = 'website.product.category'
    _description = 'Product category for website'

    name = fields.Char(string="Tag Name")
    sequence = fields.Integer(string="Sequence")
    product_ids = fields.Many2many('product.template', 'website_product_category_rel', 'product_id', 'category_id', 
                                    string="Product")