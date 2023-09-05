# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

class CompanyCode(models.Model):
    _inherit = "res.company"

    code_id = fields.Char(string='Company Code', size=4)

# TODO :
# CHANGE THE NAME_GET TO JOURNAL NAME (CURRENCY)(COMPANY CODE)
class CompanyJournal(models.Model):
    _inherit = 'account.journal'

    def name_get(self):
        res = []
        for journal in self:
            currency = journal.currency_id or journal.company_id.currency_id
            company = journal.company_id
            name = "%s (%s) (%s)" % (journal.name, currency.name, company.code_id)
            res += [(journal.id, name)]
        return res

# TODO :
# CHANGE THE NAME_GET TO ACCOUNT NAME (ACCOUNT CODE)(COMPANY CODE)
class CompanyAccount(models.Model):
    _inherit = 'account.account'

    def name_get(self):
        res = []
        for account in self:
            company = account.company_id
            if company.code_id:
                name = account.code + ' ' + account.name + ' (' + company.code_id + ')'
            else:
                name = account.code + ' ' + account.name 
            res.append((account.id, name))
        return res