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
from openerp.osv import fields, osv
import openerp.addons.decimal_precision as dp


class sale_order(osv.osv):
    _inherit = 'sale.order'
    _columns = {
        'order_line': fields.one2many('sale.order.line', 'order_id', 'Order '
                'Lines', readonly=True, states={
                'draft': [('readonly', False)],
                'sent': [('readonly', False)],
                'shipping_except': [('readonly', False)]}, copy=True),
    }

    def action_ship_create(self, cr, uid, ids, context=None):
        procurement_obj = self.pool.get('procurement.order')
        sale_line_obj = self.pool.get('sale.order.line')
        for order in self.browse(cr, uid, ids, context=context):

            for line in order.order_line:
                #Try to fix exception procurement (possible when after a shipping exception the user choose to recreate)
                if line.procurement_ids:
                    for proc in line.procurement_ids:
                    #first check them to see if they are in exception or not (one of the related moves is cancelled)
                        if proc.state == 'cancel':
                            procurement_obj.write(cr, uid, proc.id,
                                              {'product_id':
                                                   line.product_id.id,
                                               'product_qty':
                                                   line.product_uom_qty,
                                               'product_uos_qty':
                                                   line.product_uos_qty
                                               })
                else:
                    if line.state == 'draft':
                        sale_line_obj.button_confirm(cr, uid, line.id)

        super(sale_order, self).action_ship_create(cr, uid, ids,
                                                   context=context)

class sale_order_line(osv.osv):
    _inherit = "sale.order.line"
    _columns = {
        'name': fields.text('Description',
                            required=True, readonly=True,
                            states={'draft': [('readonly', False)],
                                    'confirmed':[('readonly', False)]}),
        'product_id': fields.many2one(
            'product.product', 'Product',
            domain=[('sale_ok', '=', True)],
            change_default=True, readonly=True,
            states={'draft': [('readonly', False)],
                    'confirmed':[('readonly', False)]},
            ondelete='restrict'),
        'price_unit': fields.float(
            'Unit Price', required=True,
            digits_compute= dp.get_precision('Product Price'),
            readonly=True,
            states={'draft': [('readonly', False)],
                    'confirmed':[('readonly', False)]}),
        'tax_id': fields.many2many(
            'account.tax', 'sale_order_tax',
            'order_line_id', 'tax_id', 'Taxes', readonly=True,
            states={'draft': [('readonly', False)],
                    'confirmed':[('readonly', False)]}),
        'product_uom_qty': fields.float(
            'Quantity', digits_compute= dp.get_precision('Product UoS'),
            required=True, readonly=True,
            states={'draft': [('readonly', False)],
                    'confirmed':[('readonly', False)]}),
        'product_uom': fields.many2one(
            'product.uom', 'Unit of Measure ',
            required=True, readonly=True,
            states={'draft': [('readonly', False)],
                    'confirmed':[('readonly', False)]}),
        'product_uos_qty': fields.float(
            'Quantity (UoS)' ,digits_compute= dp.get_precision('Product UoS'),
            readonly=True,
            states={'draft': [('readonly', False)],
                    'confirmed':[('readonly', False)]}),
        'discount': fields.float('Discount (%)',
            digits_compute= dp.get_precision('Discount'), readonly=True,
            states={'draft': [('readonly', False)],
            'confirmed':[('readonly', False)]}),
        }
