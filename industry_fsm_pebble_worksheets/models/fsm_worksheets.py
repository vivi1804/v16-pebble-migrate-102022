# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from ast import literal_eval

class WorksheetsOpname(models.Model):
	_name = 'worksheets.opname'

	x_task_id = fields.Many2one('project.task', string='Task')
	x_partner_id = fields.Many2one('res.partner', string='Partner')
	x_name = fields.Char(related='x_task_id.name',string='Name')
	x_sale_comments = fields.Text(string='Verkoopopmerkingen')

	extra_photo_ids = fields.One2many('sale.other.pictures','worksheet_id', string='Extra Fotos')
	roofdata_ids = fields.One2many('sale.roofdata','worksheet_id', string='Roof data')
	obstacles_ids = fields.One2many('sale.obstacles','worksheet_id', string='Obstacles')

	x_comments = fields.Text(string='Comments')
	x_comments_b = fields.Text(string='Comments')
	bool_x_comments = fields.Boolean('Adjusted?', default=False)

	@api.onchange('x_comments')
	def push_x_comments(self):
		if self.x_comments:
			self.x_comments_b = self.x_comments
			self.bool_x_comments = False

	@api.onchange('x_comments_b')
	def check_x_comments(self):
		if self.x_task_id:
			if self.x_comments_b != self.x_comments:
				self.bool_x_comments = True
			else:
				self.bool_x_comments = False
	
	x_hoofdschakelaar_aanwezig = fields.Selection([('yes','Ja'),('no','Nee')], string='Hoofdschakelaar aanwezig')
	x_hoofdschakelaar_aanwezig_b = fields.Selection([('yes','Ja'),('no','Nee')], string='Hoofdschakelaar aanwezig')
	bool_x_hoofdschakelaar_aanwezig = fields.Boolean('Adjusted?', default=False)

	@api.onchange('x_hoofdschakelaar_aanwezig')
	def push_x_hoofdschakelaar_aanwezig(self):
		if self.x_hoofdschakelaar_aanwezig:
			self.x_hoofdschakelaar_aanwezig_b = self.x_hoofdschakelaar_aanwezig
			self.bool_x_hoofdschakelaar_aanwezig = False

	@api.onchange('x_hoofdschakelaar_aanwezig_b')
	def check_x_hoofdschakelaar_aanwezig(self):
		if self.x_task_id:
			if self.x_hoofdschakelaar_aanwezig_b != self.x_hoofdschakelaar_aanwezig:
				self.bool_x_hoofdschakelaar_aanwezig = True
			else:
				self.bool_x_hoofdschakelaar_aanwezig = False

	x_teruglevering_geschikt = fields.Selection([('yes','Ja'),('no','Nee')], string='Teruglevering geschikt')
	x_teruglevering_geschikt_b = fields.Selection([('yes','Ja'),('no','Nee')], string='Teruglevering geschikt')
	bool_x_teruglevering_geschikt = fields.Boolean('Adjusted?', default=False)

	@api.onchange('x_teruglevering_geschikt')
	def push_x_teruglevering_geschikt(self):
		if self.x_teruglevering_geschikt:
			self.x_teruglevering_geschikt_b = self.x_teruglevering_geschikt
			self.bool_x_teruglevering_geschikt = False

	@api.onchange('x_teruglevering_geschikt_b')
	def check_x_teruglevering_geschikt(self):
		if self.x_task_id:
			if self.x_teruglevering_geschikt_b != self.x_teruglevering_geschikt:
				self.bool_x_teruglevering_geschikt = True
			else:
				self.bool_x_teruglevering_geschikt = False

	x_aansluitwaarde = fields.Char(string='Aansluitwaarde')
	x_aansluitwaarde_b = fields.Char(string='Aansluitwaarde')
	bool_x_aansluitwaarde = fields.Boolean('Adjusted?', default=False)

	@api.onchange('x_aansluitwaarde')
	def push_x_aansluitwaarde(self):
		if self.x_aansluitwaarde:
			self.x_aansluitwaarde_b = self.x_aansluitwaarde
			self.bool_x_aansluitwaarde = False

	@api.onchange('x_aansluitwaarde_b')
	def check_x_aansluitwaarde(self):
		if self.x_task_id:
			if self.x_aansluitwaarde_b != self.x_aansluitwaarde:
				self.bool_x_aansluitwaarde = True
			else:
				self.bool_x_aansluitwaarde = False

	x_internet = fields.Char(string='Internet')
	x_internet_b = fields.Char(string='Internet')
	bool_x_internet = fields.Boolean('Adjusted?', default=False)

	@api.onchange('x_internet')
	def push_x_internet(self):
		if self.x_internet:
			self.x_internet_b = self.x_internet
			self.bool_x_internet = False

	@api.onchange('x_internet_b')
	def check_x_internet(self):
		if self.x_task_id:
			if self.x_internet_b != self.x_internet:
				self.bool_x_internet = True
			else:
				self.bool_x_internet = False

	x_rs_1 = fields.Many2one('product.product', string='RS 1')
	x_rs_1_b = fields.Many2one('product.product', string='RS 1')
	bool_x_rs_1 = fields.Boolean('Adjusted?', default=False)

	@api.onchange('x_rs_1')
	def push_x_rs_1(self):
		if self.x_rs_1:
			self.x_rs_1_b = self.x_rs_1
			self.bool_x_rs_1 = False

	@api.onchange('x_rs_1_b')
	def check_x_rs_1(self):
		if self.x_task_id:
			if self.x_rs_1_b != self.x_rs_1:
				self.bool_x_rs_1 = True
			else:
				self.bool_x_rs_1 = False

	x_rs_2 = fields.Many2one('product.product', string='RS 2')
	x_rs_2_b = fields.Many2one('product.product', string='RS 2')
	bool_x_rs_2 = fields.Boolean('Adjusted?', default=False)

	@api.onchange('x_rs_2')
	def push_x_rs_2(self):
		if self.x_rs_2:
			self.x_rs_2_b = self.x_rs_2
			self.bool_x_rs_2 = False

	@api.onchange('x_rs_2_b')
	def check_x_rs_2(self):
		if self.x_task_id:
			if self.x_rs_2_b != self.x_rs_2:
				self.bool_x_rs_2 = True
			else:
				self.bool_x_rs_2 = False

	x_rs_3 = fields.Many2one('product.product', string='RS 3')
	x_rs_3_b = fields.Many2one('product.product', string='RS 3')
	bool_x_rs_3 = fields.Boolean('Adjusted?', default=False)

	@api.onchange('x_rs_3')
	def push_x_rs_3(self):
		if self.x_rs_3:
			self.x_rs_3_b = self.x_rs_3
			self.bool_x_rs_3 = False

	@api.onchange('x_rs_3_b')
	def check_x_rs_3(self):
		if self.x_task_id:
			if self.x_rs_3_b != self.x_rs_3:
				self.bool_x_rs_3 = True
			else:
				self.bool_x_rs_3 = False

	x_afmetingen_rs_steiger_1 = fields.Text(string='Afmetingen rs steiger 1')
	x_afmetingen_rs_steiger_1_b = fields.Text(string='Afmetingen rs steiger 1')
	bool_x_afmetingen_rs_steiger_1 = fields.Boolean('Adjusted?', default=False)

	@api.onchange('x_afmetingen_rs_steiger_1')
	def push_x_afmetingen_rs_steiger_1(self):
		if self.x_afmetingen_rs_steiger_1:
			self.x_afmetingen_rs_steiger_1_b = self.x_afmetingen_rs_steiger_1
			self.bool_x_afmetingen_rs_steiger_1 = False

	@api.onchange('x_afmetingen_rs_steiger_1_b')
	def check_x_afmetingen_rs_steiger_1(self):
		if self.x_task_id:
			if self.x_afmetingen_rs_steiger_1_b != self.x_afmetingen_rs_steiger_1:
				self.bool_x_afmetingen_rs_steiger_1 = True
			else:
				self.bool_x_afmetingen_rs_steiger_1 = False

	x_bereikbaarheid = fields.Text(string='Bereikbaarheid')
	x_bereikbaarheid_b = fields.Text(string='Bereikbaarheid')
	bool_x_bereikbaarheid = fields.Boolean('Adjusted?', default=False)

	@api.onchange('x_bereikbaarheid')
	def push_x_bereikbaarheid(self):
		if self.x_bereikbaarheid:
			self.x_bereikbaarheid_b = self.x_bereikbaarheid
			self.bool_x_bereikbaarheid = False

	@api.onchange('x_bereikbaarheid_b')
	def check_x_bereikbaarheid(self):
		if self.x_task_id:
			if self.x_bereikbaarheid_b != self.x_bereikbaarheid:
				self.bool_x_bereikbaarheid = True
			else:
				self.bool_x_bereikbaarheid = False

	x_aantal_monteurs = fields.Integer(string='Aantal monteurs')
	x_aantal_monteurs_b = fields.Integer(string='Aantal monteurs')
	bool_x_aantal_monteurs = fields.Boolean('Adjusted?', default=False)

	@api.onchange('x_aantal_monteurs')
	def push_aantal_monteurs(self):
		if self.x_aantal_monteurs:
			self.x_aantal_monteurs_b = self.x_aantal_monteurs
			self.bool_x_aantal_monteurs = False

	@api.onchange('x_aantal_monteurs_b')
	def check_aantal_monteurs(self):
		if self.x_task_id:
			if self.x_aantal_monteurs_b != self.x_aantal_monteurs:
				self.bool_x_aantal_monteurs = True
			else:
				self.bool_x_aantal_monteurs = False

	x_aantal_dagen = fields.Float(string='Aantal dagen')
	x_aantal_dagen_b = fields.Float(string='Aantal dagen')	
	bool_x_aantal_dagen = fields.Boolean('Adjusted?', default=False)

	@api.onchange('x_aantal_dagen')
	def push_aantal_dagen(self):
		if self.x_aantal_dagen:
			self.x_aantal_dagen_b = self.x_aantal_dagen
			self.bool_x_aantal_dagen = False

	@api.onchange('x_aantal_dagen_b')
	def check_aantal_dagen(self):
		if self.x_task_id:
			if self.x_aantal_dagen_b != self.x_aantal_dagen:
				self.bool_x_aantal_dagen = True
			else:
				self.bool_x_aantal_dagen = False

	x_dak_doorvoer_nodig = fields.Selection([('yes','Ja'),('no','Nee')], string='Dak doorvoer nodig')
	x_dak_doorvoer_nodig_b = fields.Selection([('yes','Ja'),('no','Nee')], string='Dak doorvoer nodig')
	bool_x_dak_doorvoer_nodig = fields.Boolean('Adjusted?', default=False)

	@api.onchange('x_dak_doorvoer_nodig')
	def push_x_dak_doorvoer_nodig(self):
		if self.x_dak_doorvoer_nodig:
			self.x_dak_doorvoer_nodig_b = self.x_dak_doorvoer_nodig
			self.bool_x_dak_doorvoer_nodig = False

	@api.onchange('x_dak_doorvoer_nodig_b')
	def check_x_dak_doorvoer_nodig(self):
		if self.x_task_id:
			if self.x_dak_doorvoer_nodig_b != self.x_dak_doorvoer_nodig:
				self.bool_x_dak_doorvoer_nodig = True
			else:
				self.bool_x_dak_doorvoer_nodig = False

	x_ac_route = fields.Text(string='AC route')
	x_ac_route_b = fields.Text(string='AC route')
	bool_x_ac_route = fields.Boolean('Adjusted?', default=False)

	@api.onchange('x_ac_route')
	def push_x_ac_route(self):
		if self.x_ac_route:
			self.x_ac_route_b = self.x_ac_route
			self.bool_x_ac_route = False

	@api.onchange('x_ac_route_b')
	def check_x_ac_route(self):
		if self.x_task_id:
			if self.x_ac_route_b != self.x_ac_route:
				self.bool_x_ac_route = True
			else:
				self.bool_x_ac_route = False

	x_ac_kabel = fields.Many2one('product.product', string='AC kabel')
	x_ac_kabel_b = fields.Many2one('product.product', string='AC kabel')
	bool_x_ac_kabel = fields.Boolean('Adjusted?', default=False)

	@api.onchange('x_ac_kabel')
	def push_x_ac_kabel(self):
		if self.x_ac_kabel:
			self.x_ac_kabel_b = self.x_ac_kabel
			self.bool_x_ac_kabel = False

	@api.onchange('x_ac_kabel_b')
	def check_x_ac_kabel(self):
		if self.x_task_id:
			if self.x_ac_kabel_b != self.x_ac_kabel:
				self.bool_x_ac_kabel = True
			else:
				self.bool_x_ac_kabel = False
	
	x_lengte_in_mtr_ac = fields.Float(string='Lengte in mtr 1')
	x_lengte_in_mtr_ac_b = fields.Float(string='Lengte in mtr 1')
	bool_x_lengte_in_mtr_ac = fields.Boolean('Adjusted?', default=False)

	@api.onchange('x_lengte_in_mtr_ac')
	def push_def_lengte_ac(self):
		if self.x_lengte_in_mtr_ac:
			self.x_lengte_in_mtr_ac_b = self.x_lengte_in_mtr_ac
			self.bool_x_lengte_in_mtr_ac = False

	@api.onchange('x_lengte_in_mtr_ac_b')
	def check_def_lengte_ac(self):
		if self.x_task_id:
			if self.x_lengte_in_mtr_ac_b != self.x_lengte_in_mtr_ac:
				self.bool_x_lengte_in_mtr_ac = True
			else:
				self.bool_x_lengte_in_mtr_ac = False

	x_dc_route = fields.Text(string='DC route')
	x_dc_route_b = fields.Text(string='DC route')
	bool_x_dc_route = fields.Boolean('Adjusted?', default=False)

	@api.onchange('x_dc_route')
	def push_x_dc_route(self):
		if self.x_dc_route:
			self.x_dc_route_b = self.x_dc_route
			self.bool_x_dc_route = False

	@api.onchange('x_dc_route_b')
	def check_x_dc_route(self):
		if self.x_task_id:
			if self.x_dc_route_b != self.x_dc_route:
				self.bool_x_dc_route = True
			else:
				self.bool_x_dc_route = False

	x_dc_dikte = fields.Selection([('4','4 mm'),('6','6 mm')], string='DC dikte')
	x_dc_dikte_b = fields.Selection([('4','4 mm'),('6','6 mm')], string='DC dikte')	
	bool_x_dc_dikte = fields.Boolean('Adjusted?', default=False)

	@api.onchange('x_dc_dikte')
	def push_x_dc_dikte(self):
		if self.x_dc_dikte:
			self.x_dc_dikte_b = self.x_dc_dikte
			self.bool_x_dc_dikte = False

	@api.onchange('x_dc_dikte_b')
	def check_x_dc_dikte(self):
		if self.x_task_id:
			if self.x_dc_dikte_b != self.x_dc_dikte:
				self.bool_x_dc_dikte = True
			else:
				self.bool_x_dc_dikte = False

	x_lengte_in_mtr_dc = fields.Float(string='Lengte in mtr 2')
	x_lengte_in_mtr_dc_b = fields.Float(string='Lengte in mtr 2')
	bool_x_lengte_in_mtr_dc = fields.Boolean('Adjusted?', default=False)
	
	@api.onchange('x_lengte_in_mtr_dc')
	def push_def_lengte_dc(self):
		if self.x_lengte_in_mtr_dc:
			self.x_lengte_in_mtr_dc_b = self.x_lengte_in_mtr_dc
			self.bool_x_lengte_in_mtr_dc = False

	@api.onchange('x_lengte_in_mtr_dc_b')
	def check_def_lengte_dc(self):
		if self.x_task_id:
			if self.x_lengte_in_mtr_dc_b != self.x_lengte_in_mtr_dc:
				self.bool_x_lengte_in_mtr_dc = True
			else:
				self.bool_x_lengte_in_mtr_dc = False

class WorksheetsOpnamePartner(models.Model):
	_inherit = 'res.partner'

	# Give value False when installment the data file will be loaded as last part therefore XML is not there yet
	def _get_default_opname(self):
		return self.env.ref('industry_fsm_pebble_worksheets.fsm_worksheet_template_opname', False)

	worksheet_template_id = fields.Many2one('worksheet.template', string="Worksheet Template", default=_get_default_opname)

	def action_fsm_worksheet_partner(self):
		action = self.worksheet_template_id.action_id.read()[0]
		worksheet = self.env[self.worksheet_template_id.model_id.model].search([('x_task_id','=',False),('x_partner_id', '=', self.id)])
		context = literal_eval(action.get('context', '{}'))
		action.update({
		    'res_id': worksheet.id if worksheet else False,
		    'views': [(False, 'form')],
		    'context': {
		        **context,
		        'edit': True,
		        'default_x_partner_id': self.id,
		        'form_view_initial_mode': 'edit',
		    },
		})
		return action

class SaleOrderLineOpname(models.Model):
	_inherit = "sale.order.line"

	def _timesheet_create_task(self, project):
		values = self._timesheet_create_task_prepare_values(project)
		task = self.env['project.task'].sudo().create(values)
		self.write({'task_id': task.id})
		# post message on task
		task_msg = _("This task has been created from: <a href=# data-oe-model=sale.order data-oe-id=%d>%s</a> (%s)") % (self.order_id.id, self.order_id.name, self.product_id.name)
		task.message_post(body=task_msg)

		#update worksheet, add task 
		worksheet_ids = self.env['worksheets.opname'].search([('x_task_id','=',False),('x_partner_id','=',self.order_id.partner_id.id)])
		for worksheet_record in worksheet_ids:
			worksheet_record.write({'x_task_id': self.task_id.id})
			if self.task_id.type_of_service == 'schouw':
				worksheet_record.write({'x_task_id': self.task_id.id})
			else:
				worksheet_record.write({'x_task_id': False})
		
		#update task, change worksheet based on partner 
		task_ids = self.env['project.task'].search([('id','=',self.task_id.id)])
		for task_record in task_ids:
			if self.task_id.type_of_service == 'schouw':
				task_record.write({'worksheet_template_id': self.order_id.partner_id.worksheet_template_id.id})

		return task	

class SaleOrderOpname(models.Model):
	_inherit = "sale.order"

	worksheet_ids = fields.Many2many('worksheets.opname', compute='_compute_worksheet_ids', string='Worksheet associated to this sale')
	worksheet_count = fields.Integer(string='Worksheets', compute='_compute_worksheet_ids', groups="project.group_project_user")

	@api.depends('order_line.product_id.project_id')
	def _compute_worksheet_ids(self):
		for rec in self:
			rec.worksheet_ids = self.env['worksheets.opname'].search([('x_task_id', 'in', rec.order_line.task_id.ids)])
			rec.worksheet_count = len(rec.worksheet_ids)

	def action_view_worksheet(self):
		if self.partner_id.worksheet_template_id:
			action = self.partner_id.worksheet_template_id.action_id.read()[0]
			# modify context to force no create/import button
			context = literal_eval(action.get('context', '{}'))
			context['create'] = 0
			action['context'] = context
			return action

class worksheet_roofdata(models.Model):
	_inherit = "sale.roofdata"

	worksheet_id = fields.Many2one('worksheets.opname', string='Worksheet')
	partner_id = fields.Many2one('res.partner','Partner', compute='get_partner_worksheet', store=True)

	@api.depends('worksheet_id')
	def get_partner_worksheet(self):
		for rec in self:
			if rec.worksheet_id:
				if rec.worksheet_id.x_partner_id:
				    partner = rec.worksheet_id.x_partner_id.id
				    rec.write({
				      'partner_id': partner
				    })

class worksheet_obstaclesdata(models.Model):
	_inherit = "sale.obstacles"

	worksheet_id = fields.Many2one('worksheets.opname', string='Worksheet')
	partner_id = fields.Many2one('res.partner','Partner', compute='get_partner_worksheet', store=True)
	
	@api.depends('worksheet_id')
	def get_partner_worksheet(self):
		for rec in self:
			if rec.worksheet_id:
				if rec.worksheet_id.x_partner_id:
				    partner = rec.worksheet_id.x_partner_id.id
				    rec.write({
				      'partner_id': partner
				    })

class worksheet_otherpictures(models.Model):
	_inherit = "sale.other.pictures"

	worksheet_id = fields.Many2one('worksheets.opname', string='Worksheet')
	partner_id = fields.Many2one('res.partner','Partner', compute='get_partner_worksheet', store=True)

	@api.depends('worksheet_id')
	def get_partner_worksheet(self):
		for rec in self:
			if rec.worksheet_id:
				if rec.worksheet_id.x_partner_id:
				    partner = rec.worksheet_id.x_partner_id.id
				    rec.write({
				      'partner_id': partner
				    })