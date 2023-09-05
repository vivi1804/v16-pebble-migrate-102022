# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

class ProductServiceType(models.Model):
    _inherit = 'product.template'

    type_of_service = fields.Selection([ ('schouw', 'Schouw'),('montage', 'Montage'),('kraan', 'Hulpmiddelen'),('no_type', 'No Special Type')],'Type of Service', default='no_type', required=True)

class ProjectTaskService(models.Model):
    _inherit = 'project.task'

    type_of_service = fields.Selection([('schouw', 'Schouw'),('montage', 'Montage'),('kraan', 'Hulpmiddelen'),('no_type', 'No Special Type')], 'Type of Service', related='sale_line_id.product_id.type_of_service', store=True)
    eigen_kraan = fields.Boolean('Eigen Kraan')
    rss = fields.Many2one('maintenance.equipment',string='RSS')
    inkooporder = fields.Many2one('purchase.order',string='Inkooporder')
    state_inkoop = fields.Selection([ ('draft', 'RFQ'),('sent', 'RFQ Sent'),('to approve', 'To Approve'),('purchase', 'Purchase Order'),('cancel', 'Cancelled')],'Status Inkoop', related='inkooporder.state')
    inkoop_datum = fields.Datetime('Inkooporder Gapland Datum', related='inkooporder.date_planned')
    auto_update_delivery = fields.Boolean('Automatic Update Delivery', related='sale_line_id.order_id.auto_update_delivery', default=True)
    auto_update_invoice = fields.Boolean('Automatic Update Invoice', related='sale_line_id.order_id.auto_update_invoice', default=True)

class SaleOrderService(models.Model):
    _inherit = 'sale.order'

    schouw_datum = fields.Date('Schouw Datum')
    installatie_datum = fields.Date('Installatie Datum')
    kraan_datum = fields.Date('Kraan Datum')
    inzet_eigen_middelen = fields.Boolean('Inzet Eigen Hulpmiddelen')
    kraan_inkooporder = fields.Many2one('purchase.order', string='Inkooporder')
    state_inkooporder = fields.Selection([ ('draft', 'RFQ'),('sent', 'RFQ Sent'),('to approve', 'To Approve'),('purchase', 'Purchase Order'),('cancel', 'Cancelled')],'Status Inkoop', related='kraan_inkooporder.state')
    geplande_levering_po = fields.Datetime('Geplande Levering PO', related='kraan_inkooporder.date_planned')
    auto_update_delivery = fields.Boolean('Automatic Update Delivery', default=True)
    auto_update_invoice = fields.Boolean('Automatic Update Invoice', default=True)