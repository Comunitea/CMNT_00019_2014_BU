# -*- coding: utf-8 -*-
# © 2017 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api, exceptions, _


class PurchaseOrder(models.Model):

    _inherit = 'purchase.order'

    invoiced2 = fields.Boolean(store=True, compute='_compute_invoiced2')

    @api.multi
    def set_invoiced(self):
        self.order_line.write({'invoiced': True})
        self.step_workflow()

    @api.depends('order_line.invoiced', 'order_line.state')
    def _compute_invoiced2(self):
        for purchase in self:
            purchase.invoiced = all(line.invoiced for line in purchase.order_line if line.state != 'cancel')
