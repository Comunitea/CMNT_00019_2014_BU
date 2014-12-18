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

    weight_edit = fields.Float('Weight', compute='compute_weight', store=True,
                               readonly=False)
    weight_net_edit = fields.Float('Net weight', compute='compute_weight',
                                   store=True, readonly=False)

    @api.one
    @api.depends('weight', 'weight_net')
    def compute_weight(self):
        self.weight_edit = self.weight
        self.weight_net_edit = self.weight_net

    @api.multi
    def action_invoice_create(self, journal_id, group=False,
                              type='out_invoice'):
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
            key_invoices = self._invoice_create_line(todo[key], journal_id,
                                                     type)
            invoices += key_invoices
            if key._name == 'stock.picking':
                address = key.partner_id.id
            else:
                address = key.id
            self.env['account.invoice'].browse(key_invoices).write(
                {'shipping_address': address})
        return invoices


class product_packaging(models.Model):

    _inherit = 'product.packaging'

    measures_str = fields.Char('Measures', compute='_get_measures')

    @api.one
    def _get_measures(self):
        self.measures_str = str(self.ul.height) + 'X' + str(self.ul.width) + \
            'X' + str(self.ul.length)


class StockQuantPackage(models.Model):

    _inherit = 'stock.quant.package'

    measures = fields.Char('Measures')
    weight = fields.Float('Weight')
