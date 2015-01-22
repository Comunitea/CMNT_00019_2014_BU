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
        Se sobreescribe para añadir la direccion de envio en la factura,
        al depender este modulo de pack se añade la funcionalidad sobreescrita
        en el modulo(pack.py:695)
        """
        todo = {}
        inv_line_obj = self.env['account.invoice.line']
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
            final_moves = self.env['stock.move']
            pack_moves = self.env['stock.move']
            for move in todo[key]:
                if not move.pack_component:
                    final_moves += move
                else:
                    pack_moves += move
            if final_moves:
                key_invoices = self._invoice_create_line(final_moves,
                                                         journal_id, type)
            else:
                delete_move = todo[key][0]
                key_invoices = self._invoice_create_line([delete_move],
                                                         journal_id, type)
                to_delete = inv_line_obj.search(
                    [('invoice_id', '=', key_invoices),
                     ('product_id', '=', delete_move.product_id.id)])
                to_delete.unlink()
            if pack_moves:
                pack_moves.write({'invoice_state': 'invoiced'})
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


class stock_transfer_details_items(models.TransientModel):
    _inherit = 'stock.transfer_details_items'

    @api.multi
    def put_in_pack(self):
        res = super(stock_transfer_details_items, self).put_in_pack()
        for packop in self:
            if packop.result_package_id:
                weight = packop.quantity * packop.product_id.weight
                measures = ''
                use_packaging = False
                for packaging in packop.product_id.packaging_ids:
                    if packaging.qty >= packop.quantity:
                        if not use_packaging:
                            use_packaging = packaging
                        else:
                            if packaging.qty < use_packaging.qty:
                                use_packaging = packaging
                if use_packaging:
                    measures = use_packaging.measures_str
                packop.result_package_id.write({'weight': weight, 'measures': measures})
        return res
