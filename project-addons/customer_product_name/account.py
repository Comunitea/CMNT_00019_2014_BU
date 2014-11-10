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


class account_invoice_line(models.Model):

    _inherit = 'account.invoice.line'

    product_name = fields.Char('Product name', size=64,
                               compute='_get_product_name', store=False)

    @api.one
    @api.depends('product_id', 'invoice_id.partner_id')
    def _get_product_name(self):
        if self.invoice_id.type != 'out_invoice':
            self.product_name = self.product_id.name
            return
        if not self.product_id:
            self.product_name = ''
        else:
            if self.partner_id.parent_id:
                partner_id = self.partner_id.parent_id.id
            else:
                partner_id = self.partner_id.id
            search_domain = [('product_id', '=', self.product_id.product_tmpl_id.id), ('customer_id', '=', partner_id)]
            customer_names = self.env['product.customer'].search(search_domain)
            if customer_names:
                self.product_name = customer_names[0].name
            else:
                self.product_name = self.product_id.name
