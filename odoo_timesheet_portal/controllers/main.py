from dataclasses import fields
from odoo import http
from odoo.http import request
from werkzeug.exceptions import NotFound
import datetime

class TimesheetPortal(http.Controller):

    @http.route('/my/timesheet/view', type='http', auth="public", website=True)
    def timesheet_detail(self, model=None, ids=None, access_token=None, **kwargs):
        valid_token = request.env['account.analytic.line'].sudo().search([('access_token' , '=' , access_token)])

        timesheets = []
        if model == 'account.analytic.line' and valid_token: 
            ids_list = ids.split(',')  # Splitting comma-separated IDs
            timesheets = request.env['account.analytic.line'].sudo().browse([int(tid) for tid in ids_list])
        else:
            raise NotFound("Resource not found")

        return request.render("odoo_timesheet_portal.timesheet_detail_template", {'timesheets': timesheets})
    
    @http.route(['/approve'], type='json', auth="public", website=True, csrf=False)
    def handle_timesheet_approval(self, **kwargs):
        if kwargs:
            timesheet_id = kwargs['id']
            timesheet = request.env['account.analytic.line'].sudo().search([('id' , '=' , timesheet_id)])
            
            timesheet.write({'approval_state': 'approved','approval_state_update': datetime.datetime.now()})

    @http.route(['/approve_all'], type='json', auth="public", website=True, csrf=False)
    def handle_timesheet_approval_all(self, **kwargs):
        if kwargs:
            timesheet_ids_str = kwargs['ids']
            timesheet_ids = [int(id_str) for id_str in timesheet_ids_str.split(',')]
            
            for timesheet in timesheet_ids:
                timesheet = request.env['account.analytic.line'].sudo().search([('id' , '=' , timesheet)])
                timesheet.write({'approval_state': 'approved','approval_state_update': datetime.datetime.now()})

    @http.route(['/reject'], type='json', auth="public", website=True, csrf=False)
    def handle_timesheet_reject(self, **kwargs):
        if kwargs:
            timesheet_id = kwargs['id']
            reason = kwargs['reason']

            timesheet = request.env['account.analytic.line'].sudo().search([('id' , '=' , timesheet_id)])
            timesheet.write({'approval_state': 'rejected','approval_state_update': datetime.datetime.now(), "reason_rejected": reason})
