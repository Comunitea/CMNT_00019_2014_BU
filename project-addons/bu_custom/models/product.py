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
from odoo import models, fields


class ProductProduct(models.Model):

    _inherit = 'product.product'

    manual_minimum_stock = fields.Float('Manual minimum stock')


class ProductTemplate(models.Model):

    _inherit = 'product.template'

    miami = fields.Boolean('Miami')
    manual_minimum_stock = fields.\
        Float('Manual minimum stock', readonly=True,
              related="product_variant_ids.manual_minimum_stock")
