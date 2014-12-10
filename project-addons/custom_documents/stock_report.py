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
from openerp import models, api


class ParticularReport(models.AbstractModel):
    _name = 'report.custom_documents.report_packing'

    @api.multi
    def render_html(self, data=None):
        report_obj = self.env['report']
        report = report_obj._get_report_from_name('custom_documents.report_packing')
        docs = []
        lines = {}
        totals = {}
        for picking in self.env[report.model].browse(self._ids):
            totals[picking.id] = {'boxes': 0.0, 'qty': 0.0, 'weight': 0.0}
            docs.append(picking)
            pack_ops = {}
            line_pick = []
            for op in picking.pack_operation_ids:
                if op.result_package_id.id not in pack_ops.keys():
                    pack_ops[op.result_package_id.id] = []
                pack_ops[op.result_package_id.id].append(op)
            pack_merged = []
            for packing in pack_ops.keys():
                prod_list = []
                for op_line in pack_ops[packing]:
                    prod_list.append([op_line.product_id.id, op_line.product_qty])
                measure_package = pack_ops[packing][0].result_package_id
                measures = measure_package.packaging_id and measure_package.packaging_id.measures_str or measure_package.measures
                new_pack = [1, prod_list, measures, pack_ops[packing]]
                added = False
                for line in range(len(pack_merged)):
                    eq = False
                    for prod in new_pack[1]:
                        for o_prod in pack_merged[line][1]:
                            if o_prod == prod:
                                eq = True
                    if new_pack[2] == pack_merged[line][2] and eq:
                        pack_merged[line][0] += 1
                        added = True
                if not added:
                    pack_merged.append(new_pack)
            for packing in pack_merged:
                first = True
                for op_line in packing[3]:
                    if first:
                        size = ''
                        weight = 0
                        if op_line.result_package_id:
                            weight = op_line.result_package_id.weight
                            size = new_pack[2]

                        line_pick.append(
                            {'prod': op_line.product_id.name, 'boxes': packing[0],
                             'qty': op_line.product_qty * packing[0], 'weight': weight,
                             'size': size, 'span': len(packing[3])})
                        totals[picking.id]['boxes'] += packing[0]
                        totals[picking.id]['qty'] += op_line.product_qty * packing[0]
                        totals[picking.id]['weight'] += weight
                        first = False
                    else:
                        line_pick.append(
                            {'prod': op_line.product_id.name, 'boxes': None,
                             'qty': op_line.product_qty * packing[0], 'weight': None,
                             'size': None})
                        totals[picking.id]['qty'] += op_line.product_qty * packing[0]
            lines[picking.id] = line_pick
        docargs = {
            'doc_ids': self._ids,
            'doc_model': report.model,
            'docs': docs,
            'lines': lines,
            'totals': totals,
        }
        return report_obj.render('custom_documents.report_packing', docargs)
