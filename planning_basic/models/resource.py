# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

class ServiceDetailedResource(models.Model):
    _name = 'detailed.resources'
    _description = "Field Service Detailed Resources"

    name = fields.Char(string='Name', store=True, readonly=False, force_save=True)
    res_type = fields.Selection([('employee', 'Employee')], string='Type of Resource')
    employee_id = fields.Many2one('hr.employee', string='Employee')
    x_color = fields.Integer('Color')

    @api.onchange('employee_id')
    def get_employee_name(self):
        if self.res_type == 'employee':
            if self.employee_id:
                self.name = self.employee_id.display_name

class ServiceDetailedPlanning(models.Model):
    _name = 'detailed.planning'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Field Service Detailed Planning"

    name = fields.Char(string='Name')
    start_datetime = fields.Datetime(string='Start Date/Time')
    end_datetime = fields.Datetime(string='End Date/Time')
    klant_id = fields.Many2one('res.partner', related='task_id.partner_id', string='Klant', store=True)
    contact_id = fields.Many2one('res.partner', related='task_id.sale_order_id.contact_person', string='Contact Person', store=True)
    verkooporder_id = fields.Many2one('sale.order', related='task_id.sale_order_id', string='Verkooporder', store=True)
    closed_project = fields.Boolean(related='task_id.sale_order_id.closed_project', string='Closed Project', store=True)
    resource_id = fields.Many2one('detailed.resources',string='Resources', store=True)
    task_id = fields.Many2one('project.task', string='Task', store=True)
    free_text = fields.Char(string='Free Text', store=True)
    res_type_id = fields.Selection(related='resource_id.res_type', string='Type of Resource', store=True)
    partner_address = fields.Text('Address', compute="get_full_address", store=True)

    @api.depends('klant_id')
    def get_full_address(self):
        for rec in self:
            if rec.klant_id:
                x_street_name = rec.klant_id.street_name or ""
                x_street_number = rec.klant_id.street_number or ""
                x_street_number2 = rec.klant_id.street_number2 or ""
                x_street2 = rec.klant_id.street2 or ""
                x_zip = rec.klant_id.zip or ""
                x_city = rec.klant_id.city or ""
                x_country_name = rec.klant_id.country_id.name or ""

                line_1 = x_street_name + " " +  x_street_number + " " + x_street_number2
                line_3 = x_zip + " " + x_city
                rec.partner_address = line_1 + "\n" + x_street2 + "\n" +  line_3 + "\n" + x_country_name
            else:
                rec.partner_address = ""

    #When saving automatically set free_text
    #@api.depends('task_id')
    #def get_task_free_text(self):
    #    for rec in self:
    #        if rec.task_id:
    #            if rec._origin.task_id.free_text:
    #                rec.free_text = rec._origin.task_id.free_text
    #            else:
    #                rec.free_text = ""

class TaskDetailedResource(models.Model):
    _inherit = 'project.task'

    res_employee_ids = fields.Many2many('detailed.resources','detailed_resources_rel','resource_employee_id','x_resource_employee_id', string='Employee(s)')
    detailed_planning_ids = fields.One2many('detailed.planning','task_id', string='Detailed Planning')
    free_text = fields.Char(string='Free Text', compute='_get_free_text', store=True)

    @api.depends("sale_line_id")
    def _get_free_text(self):
        for rec in self:
            if rec.sale_line_id:
                if rec.sale_line_id.order_id.order_type == 'b2c_solar':
                    rec.free_text = rec.sale_line_id.order_id.contact_person.display_name

    @api.onchange("res_employee_ids")
    def _onchange_res_employee_ids(self): 
        for rec in self:
            ## start add function
            plan_lines = []
            for plan_line in self.res_employee_ids:
                dp_lines = []
                for dp_line in self.detailed_planning_ids:
                    dp_lines.append(dp_line.resource_id.id)

                if not dp_lines:
                    if self.sale_line_id:
                        if self.sale_line_id.order_id.order_type == 'b2c_solar':
                            partner_name = self.sale_line_id.order_id.contact_person.name
                        else:
                            partner_name = self.sale_line_id.order_id.partner_id.name
                    else:
                        partner_name = ""
                    
                    if self.free_text:
                        text_name = self.free_text
                    else:
                        text_name = ""

                    plan_line_name = plan_line.name
                    plan_name = text_name + " - " + partner_name + " - "  + plan_line_name
                    
                    plan_vals = {
                            'name': plan_name,
                            'resource_id' : plan_line._origin.id,
                            'free_text' : self.free_text,
                            'start_datetime' : self.planned_date_begin,
                            'end_datetime' : self.planned_date_end
                    }
                    plan_lines.append((0,0, plan_vals))
                    self.detailed_planning_ids = plan_lines

                if dp_lines:
                    if self.sale_line_id:
                        if self.sale_line_id.order_id.order_type == 'b2c_solar':
                            partner_name = self.sale_line_id.order_id.contact_person.name
                        else:
                            partner_name = self.sale_line_id.order_id.partner_id.name
                    else:
                        partner_name = ""
                    
                    if self.free_text:
                        text_name = self.free_text 
                    else:
                        text_name = ""

                    plan_line_name = plan_line.name
                    plan_name = text_name + " - " + partner_name + " - "  + plan_line_name
                    
                    if not plan_line._origin.id in dp_lines:
                        plan_vals = {
                                'name': plan_name,
                                'resource_id' : plan_line._origin.id,
                                'free_text' : self.free_text,
                                'start_datetime' : self.planned_date_begin,
                                'end_datetime' : self.planned_date_end
                        }
                        plan_lines.append((0,0, plan_vals))
                        self.detailed_planning_ids = plan_lines
            ##end add function

            ##start remove function 
            rsc_lines = []
            for plan_ids_line in self.detailed_planning_ids:
                for rsc_line in self.res_employee_ids:
                    rsc_lines.append(rsc_line._origin.id)

                if not plan_ids_line.resource_id.id in rsc_lines:
                    if plan_ids_line.resource_id.res_type == 'employee':
                        plan_lines.append((2,plan_ids_line.id))
                        self.detailed_planning_ids = plan_lines
            ##end remove function

    ## edit start date and end date 
    @api.onchange("planned_date_begin")
    def _onchange_planned_date_begin(self):
        for rec in self:
            plan_lines = []
            for plan_line in self.res_employee_ids:
                dp_rec = self.env['detailed.planning'].search([('resource_id','=',plan_line._origin.id),('task_id','=',self._origin.id)])
                if dp_rec:
                    for line in dp_rec:
                        plan_lines.append((1,line.id, {'start_datetime' : self.planned_date_begin}))
                    self.detailed_planning_ids = plan_lines

    @api.onchange("planned_date_end")
    def _onchange_planned_date_end(self):
        for rec in self:
            plan_lines = []
            for plan_line in self.res_employee_ids:
                dp_rec = self.env['detailed.planning'].search([('resource_id','=',plan_line._origin.id),('task_id','=',self._origin.id)])
                if dp_rec:
                    for line in dp_rec:
                        plan_lines.append((1,line.id, {'end_datetime' : self.planned_date_end}))
                    self.detailed_planning_ids = plan_lines

    @api.onchange("free_text")
    def _onchange_free_text(self):
        for rec in self:
            plan_lines = []
            for plan_line in self.res_employee_ids:
                dp_rec = self.env['detailed.planning'].search([('resource_id','=',plan_line._origin.id),('task_id','=',self._origin.id)])
                if dp_rec:
                    for line in dp_rec:
                        if self.sale_line_id:
                            if self.sale_line_id.order_id.order_type == 'b2c_solar':
                                partner_name = self.sale_line_id.order_id.contact_person.name 
                            else:
                                partner_name = self.sale_line_id.order_id.partner_id.name 
                        else:
                            partner_name = ""
                        
                        if self.free_text:
                            text_name = self.free_text 
                        else:
                            text_name = ""

                        plan_line_name = plan_line.name
                        plan_name = text_name + " - " + partner_name + " - "  + plan_line_name

                        plan_lines.append((1,line.id, {'name': plan_name, 'free_text': self.free_text}))
                    self.detailed_planning_ids = plan_lines

class ProjectSaleOrder(models.Model):
    _inherit = 'sale.order'

    closed_project = fields.Boolean(default=False, string='Closed Project')