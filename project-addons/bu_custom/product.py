# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2015 Pexego All Rights Reserved
#    $Jesús Ventosinos Mayor <jesus@pexego.es>$
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from openerp import models, fields, api


class ProductProduct(models.Model):

    _inherit = 'product.product'

    minimum_stock = fields.Float(string='Minimum stock',
                                 compute='_get_minimum_stock')
    manual_minimum_stock = fields.Float('Manual minimum stock')
    commercialized_in_miami = fields.Boolean()
    purchase_count = fields.Integer('# Purchases', compute='_get_purchase_count')

    @api.one
    def _get_minimum_stock(self):
        self.minimum_stock = sum([x.product_min_qty for x in
                                  self.orderpoint_ids])

    @api.multi
    def action_view_purchases(self):
        result = self.env['product.template']._get_act_window_dict(
            'purchase.action_purchase_line_product_tree')
        result['domain'] = "[('product_id','in',[" + ','.join(map(str, self.ids)) + "]), ('state', 'not in', ['draft', 'cancel'])]"
        return result

    @api.one
    def _get_purchase_count(self):
        self.purchase_count = self.env['purchase.order'].search_count(
            [('order_line.product_id', '=', self.id),
             ('state', 'not in', ['draft', 'cancel'])])

class ProductTemplate(models.Model):

    _inherit = 'product.template'

    miami = fields.Boolean('Miami')
