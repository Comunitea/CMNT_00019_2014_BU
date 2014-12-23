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
    'name': "Documents customizations",
    'version': '1.0',
    'category': '',
    'description': """""",
    'author': 'Pexego',
    'website': '',
    "depends": ['account', 'stock', 'customer_product_name', 'delivery', 'hr'],
    "data": ['views/stock_picking_report.xml',
             'views/stock_picking_report_without_company.xml',
             'views/stock_packing_report.xml',
             'views/stock_internal_picking_report.xml',
             'views/sale_order_report.xml',
             'res_country_view.xml',
             'account_view.xml',
             'res_partner_view.xml',
             'picking_report.xml', 'views/account_invoice_report.xml',
             'views/mrp_production_report.xml', 'mrp_report.xml', 'stock_view.xml',
             'data/report.paperformat.csv'],
    "installable": True
}
