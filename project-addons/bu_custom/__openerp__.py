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

{
    'name': "BU customizations",
    'version': '1.0',
    'category': '',
    'description': """""",
    'author': 'Pexego',
    'website': '',
    "depends": ['sale_stock', 'stock', 'technical_office', 'l10n_es_aeat_mod340'],
    "data": ['sale_view.xml', 'mrp_view.xml', 'stock_view.xml',
             'wizard/stock_transfer_details_view.xml', 'product_view.xml',
             'invoice_view.xml'],
    "installable": True
}
