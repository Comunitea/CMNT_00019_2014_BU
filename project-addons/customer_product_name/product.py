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


class product_customer(models.Model):

    _name = 'product.customer'

    name = fields.Char('Name', size=64)
    customer_id = fields.Many2one('res.partner', 'Customer', required=True)
    product_id = fields.Many2one('product.template', 'Reference')


class product_template(models.Model):

    _inherit = 'product.template'

    product_customer_ids = fields.One2many('product.customer', 'product_id',
                                           'Customer name')


class product_product(models.Model):

    _inherit = 'product.product'

    def get_product_ref(self, partner):
        if isinstance(partner, ( int, long )):
            partner = self.env['res.partner'].browse(partner)
        name = self.env['product.customer'].search([('product_id', '=', self.id), ('customer_id', '=', partner.id)])
        return name and name[0].name or self.default_code

