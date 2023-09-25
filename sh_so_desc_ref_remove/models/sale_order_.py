# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models,api

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'


    @api.onchange('product_id')
    def _compute_name(self):
    
        res = super(SaleOrderLine, self)._compute_name()
    
        for line in self:
            if self.product_id.description_sale:
                line.name = self.product_id.name + '\n' + self.product_id.description_sale
            else:
                line.name = self.product_id.name
        return res