# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging
import re

from odoo import api, fields, models, tools, _
from odoo.exceptions import ValidationError
from odoo.osv import expression
from odoo.tools import float_compare

_logger = logging.getLogger(__name__)

class WorksheetTemplate(models.Model):
    _inherit = 'worksheet.template'
   
    module_template = fields.Boolean('Template by module')

    # overwrite the create function, because when you import a data it will create automatical a module.
    # in some cases you want to push the template by module

    # def create(self, vals):
    #     raise Warning('you are creating an custom template')
    #     if not self.module_template:
    #         template = super(ProjectWorksheetTemplate, self).create(vals)
    #         if not self.env.context.get('fsm_worksheet_no_generation'):
    #             self._generate_worksheet_model(template)
    #         return template
    #     if self.module_template:
    #         raise Warning('2')

    @api.model
    def create(self, vals):
        template = super(models.Model, self).create(vals)
        if vals and vals.get('module_template'):
            #raise Warning ("It is time to make your own worksheet")
            return template
        else:
            if not self.env.context.get('fsm_worksheet_no_generation'):
                #raise Warning ("Grazy time")
                self._generate_worksheet_model(template)
            return template
        