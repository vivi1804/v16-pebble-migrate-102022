# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

# TODO :
# CHANGE THE NAME_GET TO VAT (COMPANY CODE)
class CompanyTax(models.Model):
    _inherit = 'account.tax'

    def name_get(self):
        res = []
        for tax in self:
            company = tax.company_id
            if company.code_id:
                name = "%s (%s)" % (tax.name, company.code_id)
            else:
                name = tax.name
            res += [(tax.id, name)]
        return res