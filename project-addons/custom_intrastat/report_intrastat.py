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

from openerp import models, fields
from openerp.tools.sql import drop_view_if_exists


class report_intrastat(models.Model):
    _inherit = "report.intrastat"

    partner_id = fields.Many2one('res.partner', 'Partner')
    country_id = fields.Many2one('res.country', 'Country')
    type = fields.Selection(selection_add=[('import_refund', 'Import refund'),
                                           ('export_refund', 'Export refund')])


    def init(self, cr):
        drop_view_if_exists(cr, 'report_intrastat')
        cr.execute("""
            create or replace view report_intrastat as (
                select
                    to_char(inv.date_invoice, 'YYYY') as name,
                    to_char(inv.date_invoice, 'MM') as month,
                    inv.partner_id as partner_id,
                    min(inv_line.id) as id,
                    intrastat.id as intrastat_id,
                    inv_country.id as country_id,
                    sum(case when inv_line.price_unit is not null
                            then
                                CASE WHEN inv.type in ('out_invoice', 'in_invoice') THEN inv_line.price_subtotal
                                     WHEN inv.type in ('out_refund', 'in_refund') THEN - inv_line.price_subtotal end

                            else 0
                        end) as value,
                    (SELECT sum(pick.weight_edit) as weight
                         from stock_picking pick
                         where pick.invoice_id = inv.id) as weight,
                    sum(
                        case when uom.category_id != puom.category_id then inv_line.quantity
                        else (inv_line.quantity * uom.factor) end
                    ) as supply_units,

                    inv.currency_id as currency_id,
                    inv.number as ref,
                    CASE WHEN inv.type = 'out_invoice' THEN 'export'
                         WHEN inv.type = 'in_invoice' THEN 'import'
                         WHEN inv.type = 'out_refund' THEN 'export_refund'
                         WHEN inv.type = 'in_refund' THEN 'import_refund'
                    END AS type
                from
                    account_invoice inv
                    left join account_invoice_line inv_line on inv_line.invoice_id=inv.id
                    left join (product_template pt
                        left join product_product pp on (pp.product_tmpl_id = pt.id))
                    on (inv_line.product_id = pp.id)
                    left join product_uom uom on uom.id=inv_line.uos_id
                    left join product_uom puom on puom.id = pt.uom_id
                    left join report_intrastat_code intrastat on pt.intrastat_id = intrastat.id
                    left join (res_partner inv_address
                        left join res_country inv_country on (inv_country.id = inv_address.country_id))
                    on (inv_address.id = inv.partner_id)
                where
                    inv.state in ('open','paid')
                    and inv_line.product_id is not null
                    and inv_country.intrastat=true
                group by to_char(inv.date_invoice, 'YYYY'), to_char(inv.date_invoice, 'MM'),
                         inv.partner_id,intrastat.id,inv.type,pt.intrastat_id, inv_country.id,inv.number,
                         inv.id, inv.currency_id)""")
