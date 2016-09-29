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

    @api.one
    def _get_minimum_stock(self):
        self.minimum_stock = sum([x.product_min_qty for x in
                                  self.orderpoint_ids])
