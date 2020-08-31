##############################################################################
#
#    Copyright (C) 2015 Comunitea All Rights Reserved
#    $Jesús Ventosinos Mayor <jesus@comunitea.com>$
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
from odoo import models, fields, api


class AccountInvoice(models.Model):

    _inherit = 'account.invoice'

    sale_ref = fields.Char(string='Sale ref', compute='_get_so')

    def _get_so(self):
        for invoice in self:
            refs = invoice.invoice_line_ids.\
                mapped('sale_line_ids.order_id.client_order_ref')
            invoice.sale_ref = ",".join([x for x in refs if x])

    @api.multi
    def _get_computed_reference(self):
        self.ensure_one()
        if self.company_id.invoice_reference_type == 'invoice_number' and \
                not self.reference:
            return self.invoice_number[self.invoice_number.rfind('/') + 1:]
        else:
            return super()._get_computed_reference()


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
    invoice_date = fields.Date(related='invoice_id.date_invoice', store=True)
    invoice_type = fields.Selection(store=True)
