# -*- coding: utf-8 -*-
from odoo import api, fields, models

class CustomerProject(models.Model):
    _name = 'website.project.customer'
    _inherit = ['mail.thread']
    _description = 'Publish customer project details on the website'
   
    name = fields.Char(string="Project Name")
    sequence = fields.Integer(string="Sequence")
    short_description = fields.Html(string="Short Description")
    long_description = fields.Html(string="Long Description")
    project_image = fields.Binary(string="Image")
    tag_ids = fields.Many2many('website.project.tag', 'website_project_tag_rel', 'tag_id', 'project_id', 
                            string="Website Tags" )
    post_state = fields.Selection([('st_draft','Draft'),('st_publish','Published')],
                                    default='st_draft', track_visibility='onchange')
    post_layout = fields.Selection([('layout_default','Default'),('layout_1','Layout 1'),('layout_2','Layout 2'),('layout_3','Layout 3')],
                                    default='layout_default')
    image_ids = fields.One2many('website.project.customer.images', 'project_id', string="Images")

    def action_publish(self):
        result = self.write({'post_state': 'st_publish'})
        return result
    
    def action_unpublish(self):
        result = self.write({'post_state': 'st_draft'})
        return result
    
    ##relation with other module 
    buurt_id = fields.Many2one('res.buurt', string="Buurt", domain="[('wijk_id', '=?', wijk_id)]")
    wijk_id = fields.Many2one('res.wijk', string="Wijk", domain="[('gemeente_id', '=?', gemeente_id)]")
    gemeente_id = fields.Many2one('res.gemeente', string="Gemeente")

class ProjectTag(models.Model):
    _name = 'website.project.tag'
    _description = 'Project tags for website'

    name = fields.Char(string="Tag Name")
    sequence = fields.Integer(string="Sequence")
    project_ids = fields.Many2many('website.project.customer', 'website_project_tag_rel', 'project_id', 'tag_id', string="Projects")

class CustomerProjectImages(models.Model):
    _name = 'website.project.customer.images'
    _description = 'Project Customer Images'

    project_id = fields.Many2one ('website.project.customer', string="Project")
    photo = fields.Binary(string="Image")