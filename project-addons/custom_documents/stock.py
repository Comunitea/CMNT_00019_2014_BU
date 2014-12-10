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


class StockPicking(models.Model):

    _inherit = 'stock.picking'

    '''weight_o = fields.Float('Weight')
    weight_net_o = fields.Float('Net weight')
    weight_manual_changed = fields.Boolean('Changed')
    auto_changed = fields.Boolean('Changed')'''

    @api.multi
    def action_invoice_create(self, journal_id, group=False, type='out_invoice'):
        """ Creates invoice based on the invoice state selected for picking.
        @param journal_id: Id of journal
        @param group: Whether to create a group invoice or not
        @param type: Type invoice to be created
        @return: Ids of created invoices for the pickings
        """
        todo = {}
        for picking in self:
            if group:
                key = picking.partner_id
            else:
                key = picking
            for move in picking.move_lines:
                if move.invoice_state == '2binvoiced':
                    if (move.state != 'cancel') and not move.scrapped:
                        todo.setdefault(key, [])
                        todo[key].append(move)
        invoices = []
        for key in todo.keys():
            key_invoices = self._invoice_create_line(todo[key], journal_id, type)
            invoices += key_invoices
            if key._name == 'stock.picking':
                address = key.partner_id.id
            else:
                address = key.id
            self.env['account.invoice'].browse(key_invoices).write({'shipping_address': address})
        return invoices

    ''' @api.onchange('move_lines')
    def onchange_moves(self):
        import ipdb; ipdb.set_trace()
        if not self.weight_manual_changed:
            self.weight_o = sum([x.wieght for x in self.move_lines])
            self.weight_net_o = sum([x.weight_net for x in self.move_lines])
            self.atuo_changed = True

    @api.onchange('weight_o')
    def onchange_weight_o(self):
        if self.auto_changed:
            self.weight_manual_changed = False
        else:
            self.weight_manual_changed = True


    @api.one
    def write(self, vals):
        import ipdb; ipdb.set_trace()
        if not self.vals.get('auto_changed', False):
            vals['weight_manual_changed'] = True
        return super(StockPicking, self).write(vals)'''

class product_packaging(models.Model):

    _inherit = 'product.packaging'

    measures_str = fields.Char('Measures', compute='_get_measures')

    @api.one
    def _get_measures(self):
        self.measures_str = str(self.ul.height) + 'X' + str(self.ul.width) + 'X' + str(self.ul.length)

class StockQuantPackage(models.Model):

    _inherit = 'stock.quant.package'

    measures = fields.Char('Measures')
    weight = fields.Float('Weight')
