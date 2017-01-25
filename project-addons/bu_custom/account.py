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


class account_invoice(models.Model):

    _inherit = 'account.invoice'

    sale_ref = fields.Char(string='Sale ref', compute='_get_so')

    def _get_so(self):
        for record in self:
            refs = []
            for picking in record.picking_ids:
                if picking.sale_id:
                    sale_ref = picking.sale_id.client_order_ref
                    if sale_ref not in refs:
                        refs.append(sale_ref)

            for ref in refs:
                record.sale_ref = ref

    @api.multi
    def invoice_validate(self):
        res = super(account_invoice, self).invoice_validate()
        for invoice in self:
            if not invoice.reference:
                invoice.reference = invoice.number[invoice.number.rfind('/')+1:]


class AccountInvoiceReport(models.Model):

    _inherit = 'account.invoice.report'

    agent_id = fields.Many2one("sale.agent", 'Agent', readonly=True)
    invoice_id = fields.Many2one("account.invoice", 'Agent', readonly=True)

    def _sub_select(self):
        select_str = super(AccountInvoiceReport, self)._sub_select()
        select_str += ",ai.agent_id as agent_id, ail.invoice_id as invoice_id"
        return select_str

    def _select(self):
        select_str = super(AccountInvoiceReport, self)._select()
        select_str += ",sub.agent_id as agent_id, sub.invoice_id as invoice_id"
        return select_str

    def _group_by(self):
        group_by_str = super(AccountInvoiceReport, self)._group_by()
        group_by_str += ",ai.agent_id, ail.invoice_id"
        return group_by_str


class AccountInvoiceLine(models.Model):

    _inherit = 'account.invoice.line'

    product_category = fields.Many2one('product.category', 'Category',
                                       related="product_id.categ_id",
                                       store=True)
    product_brand = fields.Many2one('product.brand', 'Brand',
                                    related="product_id.product_brand_id",
                                    store=True)
    journal_id = fields.Many2one('account.journal', 'Journal',
                                 related="invoice_id.journal_id")
    invoice_type = fields.Selection(
        [('out_invoice','Customer Invoice'),
        ('in_invoice','Supplier Invoice'),
        ('out_refund','Customer Refund'),
        ('in_refund','Supplier Refund')],
        related='invoice_id.type', store=True)
    invoice_date = fields.Date(related='invoice_id.date_invoice', store=True)
    agent_id = fields.Many2one("sale.agent", "Agent", store=True,
                               related="invoice_id.agent_id")

