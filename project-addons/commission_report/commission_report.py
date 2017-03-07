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

from openerp import models, fields, tools


class commission_report(models.Model):

    _name = "commission.report"
    _description = "Sale commission report"
    _auto = False

    product_id = fields.Many2one('product.product', 'Product')
    agent_id = fields.Many2one('sale.agent', 'Agent')
    qty = fields.Float('Quantity')
    settled = fields.Boolean('Settled')
    inv_date = fields.Date('Date invoice')
    partner_id = fields.Many2one("res.partner", "Customer")
    invoice_id = fields.Many2one("account.invoice", "Invoice")
    price_unit = fields.Float("Price unit")
    commission_amount = fields.Float("Commission amount")
    journal_id = fields.Many2one("account.journal", "Journal")

    def init(self, cr):
        tools.drop_view_if_exists(cr, self._table)
        cr.execute("""CREATE or REPLACE VIEW %s as (
            SELECT c_line.id,
                i_line.product_id  AS product_id,
                c_line.agent_id  AS agent_id,
                c_line.quantity  AS commission_amount,
                c_line.settled  AS settled,
                inv.date_invoice  AS inv_date,
                inv.state  AS state,
                inv.partner_id as partner_id,
                inv.id as invoice_id,
                inv.journal_id as journal_id,
                sum(i_line.price_unit * (1 - (i_line.discount / 100.0))) as price_unit,
                sum(i_line.quantity) as qty
            FROM account_invoice_line AS i_line
                JOIN invoice_line_agent  AS c_line ON i_line.id=c_line.invoice_line_id
                JOIN account_invoice  AS inv ON i_line.invoice_id=inv.id
            WHERE inv.state IN ('open', 'paid')
            GROUP BY i_line.product_id, c_line.agent_id, c_line.quantity, c_line.settled, inv.date_invoice, inv.state, c_line.id, inv.partner_id, inv.id, inv.journal_id
        )""" % (self._table,))
