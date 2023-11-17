from odoo import models, fields, api, _
import uuid
from collections import defaultdict
from odoo.exceptions import UserError, AccessError
import datetime


class TimesheetPortal(models.Model):
	_inherit="account.analytic.line"    
	
	access_token = fields.Char("Security Token", default=lambda self: str(uuid.uuid4()), required=True, copy=False, readonly=True)
	approval_state = fields.Selection([('submitted','Submitted'),('wait','Waiting Approval'),('approved','Approved'),('rejected','Rejected')], default="submitted")
	manager_approval_on = fields.Datetime(string="Manager Approval On")
	approval_state_update = fields.Datetime(string="State Updated On")
	reason_rejected = fields.Text(string="Reason Rejected")

	##rewrite write to add user public
	def write(self, vals):
		print("test")
		return super(TimesheetPortal, self).write(vals)

	def action_share_link(self):
		for rec in self:
			if rec:
				if 'hr_timesheet.group_hr_timesheet_approver' not in rec.env.user.groups_id.mapped('name'):
					active_ids = rec._context.get('active_ids', [])  # Get selected record IDs
					lines_by_partner = defaultdict(list)

					# Group lines by partner
					for active_id in active_ids:
						current_record = rec.env['account.analytic.line'].browse(active_id)
						lines_by_partner[current_record.partner_id.id].append(current_record)

					# If there are multiple partners selected, show a warning
					if len(lines_by_partner) > 1:
						partner_names = [
							partner.name for partner in rec.env['res.partner'].browse(lines_by_partner.keys())
						]
						partner_names_str = ', '.join(partner_names)
						warning_msg = f"Selected lines belong to different partners: {partner_names_str}. You can only send emails to the same partner."
						
						# You can raise a UserError or handle the warning message as needed
						# For example:
						raise UserError(warning_msg)
						# Or show a warning using Odoo's messaging framework
						# rec.message_post(body=warning_msg, message_type='warning')

					# If only one partner is found, proceed to send the email
					if len(lines_by_partner) == 1:
						partner_id = list(lines_by_partner.keys())[0]

						# Generate URLs for each partner's set of IDs
						for partner_id, lines in lines_by_partner.items():
							# access_tokens = [line.access_token for line in lines]
							access_token = lines[0].access_token if lines else None
							base_url = rec.env['ir.config_parameter'].sudo().get_param('web.base.url')
							
							# Combine multiple IDs in the URL parameter
							ids_param = ','.join(str(line.id) for line in lines)

							for line in lines:
								line.write({
									'approval_state': 'wait',
									'manager_approval_on': datetime.datetime.now()
								})

						# link = f"{base_url}/my/timesheet/view?model={rec._name}&ids={ids_param}&access_token={'&access_token='.join(access_tokens)}"
						link = f"{base_url}/my/timesheet/view?model={rec._name}&ids={ids_param}&access_token={access_token}"

						# Send email to the customer with the timesheet links
						customer_email = rec.env['res.partner'].browse(partner_id).email

						email_template = rec.env.ref('odoo_timesheet_portal.timesheet_portal_invitation')  

						if email_template:
							email_template.with_context({'default_model': 'your.model'}).send_mail(
								rec.id, force_send=True, email_values={'email_to': customer_email, 'partner_ids': [(6, 0, [partner_id])], 'body_html': email_template.body_html.replace('%LINK%', link)})

							break
			else:
				warning_msg = f"You are not allowed! Please contact your manager."
				raise UserError(warning_msg)
	
	def action_reject(self):
		for rec in self:
			if rec:
				if 'hr_timesheet.group_hr_timesheet_approver' not in rec.env.user.groups_id.mapped('name'):
					active_ids = rec._context.get('active_ids', [])
					for active_id in active_ids:
						record = rec.env['account.analytic.line'].browse(active_id)
						record.write({
							'approval_state': 'rejected',
							'manager_approval_on': datetime.datetime.now()
						})
				else:
					warning_msg = f"You are not allowed! Please contact your manager."
					raise UserError(warning_msg)