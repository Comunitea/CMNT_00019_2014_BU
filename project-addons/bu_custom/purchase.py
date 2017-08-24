# -*- coding: utf-8 -*-
# © 2017 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api, exceptions, _


class PurchaseOrder(models.Model):

    _inherit = 'purchase.order'

    @api.multi
    def set_invoiced(self):
        self.order_line.write({'invoiced': True})
        self.step_workflow()
