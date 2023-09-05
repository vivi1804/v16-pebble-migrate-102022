#################################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2017 B-Informed Asia>
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

from odoo import models, fields, api, tools, _
from odoo.exceptions import UserError, ValidationError

# Table of template
class solar_saletemplate(models.Model):
    _inherit = "res.company"

    b2c_text = fields.Html('Algemene text in B2C offerte')
    extra_option_text = fields.Html('Extra opties tekst')
    vat_disclamer = fields.Html('Vat disclamer')