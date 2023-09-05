# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

class ServiceDetailedResource2(models.Model):
    _inherit = 'detailed.resources'

    res_type = fields.Selection(selection_add=[('vehicle', 'Vehicle')])
    vehicle_id = fields.Many2one('fleet.vehicle', string='Vehicle')

    @api.onchange('vehicle_id')
    def get_vehicle_name(self):
    	if self.res_type == 'vehicle':
    		if self.vehicle_id:
    			self.name = self.vehicle_id.display_name

class TaskDetailedResource2(models.Model):
    _inherit = 'project.task'

    res_vehicle_ids = fields.Many2many('detailed.resources','detailed_resources_rel_2','resource_vehicle_id','x_resource_vehicle_id', string='Vehicle(s)')

    @api.onchange("res_vehicle_ids")
    def _onchange_res_vehicle_ids(self):
        ## start add function
            plan_lines = []
            for plan_line in self.res_vehicle_ids:
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

            rsc_lines = []
            for plan_ids_line in self.detailed_planning_ids:
                for rsc_line in self.res_vehicle_ids:
                    rsc_lines.append(rsc_line._origin.id)

                if not plan_ids_line.resource_id.id in rsc_lines:
                    if plan_ids_line.resource_id.res_type == 'vehicle':
                        plan_lines.append((2,plan_ids_line.id))
                        self.detailed_planning_ids = plan_lines

    @api.onchange("planned_date_begin")
    def _onchange_planned_date_begin_2(self):
        for rec in self:
            plan_lines = []
            for plan_line in self.res_vehicle_ids:
                dp_rec = self.env['detailed.planning'].search([('resource_id','=',plan_line._origin.id),('task_id','=',self._origin.id)])
                if dp_rec:
                    for line in dp_rec:
                        plan_lines.append((1,line.id, {'start_datetime' : self.planned_date_begin}))
                    self.detailed_planning_ids = plan_lines

    @api.onchange("planned_date_end")
    def _onchange_planned_date_end_2(self):
        for rec in self:
            plan_lines = []
            for plan_line in self.res_vehicle_ids:
                dp_rec = self.env['detailed.planning'].search([('resource_id','=',plan_line._origin.id),('task_id','=',self._origin.id)])
                if dp_rec:
                    for line in dp_rec:
                        plan_lines.append((1,line.id, {'end_datetime' : self.planned_date_end}))
                    self.detailed_planning_ids = plan_lines

    @api.onchange("free_text")
    def _onchange_free_tex_2(self):
        for rec in self:
            plan_lines = []
            for plan_line in self.res_vehicle_ids:
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