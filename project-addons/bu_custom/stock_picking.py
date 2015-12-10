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


class StockPicking(models.Model):

    _inherit = 'stock.picking'

    currency = fields.Many2one('res.currency',
                               related='sale_id.currency_id', store=True)
    partner_id = fields.Many2one(states={'done': [('readonly', False)],
                                         'cancel': [('readonly', True)]})

    def link_backorder(self, picking, invoice_id):
        picking.write({'invoice_id': invoice_id})
        if picking.backorder_id:
            self.link_backorder(picking.backorder_id, invoice_id)

    def _create_invoice_from_picking(
            self, cr, uid, picking, vals, context=None):
        '''
            Para linkear bien la factura a los envios parciales
        '''
        invoice_id = super(StockPicking, self)._create_invoice_from_picking(
            cr, uid, picking, vals, context=context)
        if picking.backorder_id:
            self.link_backorder(picking.backorder_id, invoice_id)
        return invoice_id


class StockMove(models.Model):

    _inherit = 'stock.move'

    @api.multi
    def action_cancel(self):
        self.write({'invoice_state': 'none'})
        return super(StockMove, self).action_cancel()
