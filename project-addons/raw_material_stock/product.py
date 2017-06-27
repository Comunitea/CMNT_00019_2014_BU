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

    used_stock = fields.Float('Used stock', compute='_get_used_stock',
                              store=False,
                              digits_compute=dp.get_precision('Product Unit of Measure'),
                              help="Quantity available + stock used in manufacturing")
    show_used_stock = fields.Boolean('Show used stock')

    @api.one
    @api.depends('show_used_stock', 'qty_available')
    def _get_used_stock(self):
        """
            Calculo del stock usado en producciones en stock.
        """
        if not self.show_used_stock:
            self.used_stock = 0
            return
        new_context = self.env.context
        if not self.env.context.get('warehouse', False):
            warehouse = self.env['stock.warehouse'].search(
                [('show_material_stock', '=', True)])
            if warehouse:
                new_context = dict(self.env.context)

                new_context['warehouse'] = [x.id for x in warehouse]
        uom_obj = self.with_context(new_context).env['product.uom']
        bom_lines = self.with_context(new_context).env['mrp.bom.line'].search([('product_id', '=',
                                                    self.id)])
        total_qty = self.with_context(new_context).qty_available
        for line in bom_lines:
            line_qty = uom_obj._compute_qty(line.product_uom.id,
                                            line.product_qty,
                                            self.uom_id.id)
            product_ids = line.bom_id.product_id or \
                line.bom_id.product_tmpl_id.product_variant_ids
            for variant in product_ids:
                bom_prod_qty = uom_obj._compute_qty(line.bom_id.product_uom.id,
                                                    line.bom_id.product_qty,
                                                    variant.uom_id.id)
                total_qty += (line_qty / bom_prod_qty) * \
                    (variant.used_stock != 0 and
                     variant.used_stock or
                     variant.qty_available)

        self.used_stock = total_qty
