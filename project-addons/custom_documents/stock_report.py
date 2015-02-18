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


class PackingrReport(models.AbstractModel):
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
                            {'prod': op_line.product_id.get_product_ref(op_line.picking_id.partner_id), 'boxes': packing[0],
                             'qty': op_line.product_qty * packing[0], 'weight': weight,
                             'size': size, 'span': len(packing[3])})
                        totals[picking.id]['boxes'] += packing[0]
                        totals[picking.id]['qty'] += op_line.product_qty * packing[0]
                        totals[picking.id]['weight'] += weight
                        first = False
                    else:
                        line_pick.append(
                            {'prod': op_line.product_id.get_product_ref(op_line.picking_id.partner_id), 'boxes': None,
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


class picking_report(models.AbstractModel):
    _name = 'report.stock.report_picking_'

    @api.multi
    def render_html(self, data=None):
        report_obj = self.env['report']
        report = report_obj._get_report_from_name('stock.report_picking_')
        packs = {}
        for picking in self.env[report.model].browse(self._ids):
            if not picking.sale_id:
                continue
            packs[picking.id] = []
            my_context = dict(self.env.context)
            my_context['lang'] = picking.partner_id.lang
            for line in picking.sale_id.order_line:
                if line.pack_child_line_ids and not line.pack_parent_line_id:
                    packs[picking.id].append({
                        'product_id': line.product_id,
                        'product_name': line.with_context(my_context).product_id.name,
                        'qty': line.product_uom_qty,
                        'uom': line.with_context(my_context).product_uom.name
                    })

        docargs = {
            'doc_ids': self._ids,
            'doc_model': report.model,
            'docs': self.env[report.model].browse(self._ids),
            'packs': packs,
        }
        return report_obj.render('stock.report_picking_', docargs)


class picking_without_company_report(models.AbstractModel):
    _name = 'report.custom_documents.report_picking_final'

    @api.multi
    def render_html(self, data=None):
        report_obj = self.env['report']
        report = report_obj._get_report_from_name('custom_documents.report_picking_final')
        packs = {}
        for picking in self.env[report.model].browse(self._ids):
            if not picking.sale_id:
                continue
            packs[picking.id] = []
            my_context = dict(self.env.context)
            my_context['lang'] = picking.partner_id.lang
            for line in picking.sale_id.order_line:
                if line.pack_child_line_ids and not line.pack_parent_line_id:
                    packs[picking.id].append({
                        'product_id': line.product_id,
                        'product_name': line.with_context(my_context).product_id.name,
                        'qty': line.product_uom_qty,
                        'uom': line.with_context(my_context).product_uom.name
                    })

        docargs = {
            'doc_ids': self._ids,
            'doc_model': report.model,
            'docs': self.env[report.model].browse(self._ids),
            'packs': packs,
        }
        return report_obj.render('custom_documents.report_picking_final', docargs)


class picking_internal_report(models.AbstractModel):
    _name = 'report.custom_documents.report_internal_picking'

    @api.multi
    def render_html(self, data=None):
        report_obj = self.env['report']
        report = report_obj._get_report_from_name('custom_documents.report_internal_picking')
        packs = {}
        '''
            Estructura
            lin_: linea de venta de producto pack, si no forma parte de un pack es False
            mv*: movimientos
            [(lin_, [mv1, mv2, mv3])]
        '''
        for picking in self.env[report.model].browse(self._ids):
            packs[picking.id] = []
            packs_dict = {}
            for line in picking.move_lines:
                if line.pack_component:
                    move_sale = line.get_sale_line_id()
                    pack_top = False
                    line_aux = move_sale
                    while not pack_top:
                        line_aux = line_aux.pack_parent_line_id
                        if not line_aux.pack_parent_line_id:
                            pack_top = line_aux
                    if not packs_dict.get(pack_top.id, False):
                        packs_dict[pack_top.id] = []
                    packs_dict[pack_top.id].append(line)
                else:
                    packs[picking.id].append((False, [line]))
            for sale_line_id in packs_dict.keys():
                sale_line = self.env['sale.order.line'].browse(sale_line_id)
                packs[picking.id].append((sale_line, packs_dict[sale_line_id]))
        docargs = {
            'doc_ids': self._ids,
            'doc_model': report.model,
            'docs': self.env[report.model].browse(self._ids),
            'moves': packs,
        }
        return report_obj.render('custom_documents.report_internal_picking', docargs)
