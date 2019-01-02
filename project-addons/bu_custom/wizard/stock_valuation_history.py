# -*- coding: utf-8 -*-
# © 2019 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from openerp import fields, models


class StockHistory(models.Model):
    _inherit = 'stock.history'

    product_type = fields.Selection(related='product_id.type', readonly=True)
