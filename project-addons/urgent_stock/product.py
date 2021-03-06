# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2014 Pexego All Rights Reserved
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
import openerp.addons.decimal_precision as dp


class ProductProduct(models.Model):

    _inherit = 'product.product'

    urgent_stock = fields.Float('Urgent stock', compute='_get_urgent_stock',
                                store=False,
                                digits_compute=dp.get_precision('Product Unit of Measure'))

    @api.one
    def _get_urgent_stock(self):
        """
            Calculo del stock necesario para cubrir los albaranes de salida.
        """
        uom_obj = self.env['product.uom']
        new_context = self.env.context
        move_domain = [('state', 'in', ['waiting', 'confirmed']),
                       ('product_id', '=', self.id),
                       ('picking_type_id.code', '=', 'outgoing')]
        if not self.env.context.get('warehouse', False):
            warehouse = self.env['stock.warehouse'].search(
                [('show_material_stock', '=', True)])
            if warehouse:
                new_context = dict(self.env.context)
                new_context['warehouse'] = [x.id for x in warehouse]
            move_domain += [('warehouse_id', 'in', [x.id for x in warehouse])]

        moves_out = self.with_context(new_context).env['stock.move'].search(
            move_domain)
        total_qty = 0
        for move in moves_out:
            total_qty += uom_obj._compute_qty(move.product_uom.id,
                                              move.product_uom_qty,
                                              self.uom_id.id)
        if total_qty > self.with_context(new_context).qty_available:
            self.urgent_stock = total_qty - self.with_context(new_context).qty_available
        else:
            self.urgent_stock = 0
