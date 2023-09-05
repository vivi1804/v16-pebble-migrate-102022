# -*- coding: utf-8 -*-
#################################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2017 B-informed Asia <info@B-informed.id>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#################################################################################



# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

from . import models

from odoo import api, SUPERUSER_ID

def _update_partners_with_default_data(cr, registry):
    """ TThis hook will update all res.partners with the nessary worktemplates
    """
    env = api.Environment(cr, SUPERUSER_ID, {})
    opname = env.ref('industry_fsm_pebble_worksheets.fsm_worksheet_template_opname')
    partners_ids = env['res.partner'].search([('worksheet_template_id', '=', False)])
    partners_ids.write({'worksheet_template_id': opname})