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

from openerp import models, api, fields, _
from datetime import date


class product_product(models.Model):

    _inherit = 'product.product'

    stock_min = fields.Float('Min stock', compute='_get_orderpoint_stock')

    @api.one
    def _get_orderpoint_stock(self):
        rules = self.env['stock.warehouse.orderpoint'].search(
            [('product_id', '=', self.id)], limit=1,
            order='product_min_qty desc')
        self.stock_min = rules and rules[0].product_min_qty or 0.0


class ParticularReport(models.AbstractModel):
    _name = 'report.custom_documents.mrp_production'

    @api.multi
    def render_html(self, data=None):
        report_obj = self.env['report']
        report = report_obj._get_report_from_name(
            'custom_documents.mrp_production')
        # objetos en un diccionario
        # {'constock': {'robot':[], 'manual':[]}, 'sinstock':{'robot':[],
        #                                                     'manual':[]}}
        docs = {
            _('with minimun stock'): {},
            _('without minimun stock'): {}
        }
        totals = {
            _('with minimun stock'): {},
            _('without minimun stock'): {},
            'total': {},
        }
        for production in self.env[report.model].browse(self._ids):
            rules = self.env['stock.warehouse.orderpoint'].search(
                [('product_id', '=', production.product_id.id)])
            if production.routing_id.name not in \
                    docs[_('with minimun stock')].keys() and rules:
                docs[_('with minimun stock')][production.routing_id.name] = []
                totals[_('with minimun stock')][production.routing_id.name] = 0.0
            if production.routing_id.name not in \
                    docs[_('without minimun stock')].keys() and not rules:
                docs[_('without minimun stock')][production.routing_id.name] = []
                totals[_('without minimun stock')][production.routing_id.name] = 0.0
            if production.routing_id.name not in totals['total'].keys():
                totals['total'][production.routing_id.name] = 0.0
            if rules:
                key = _('with minimun stock')
            else:
                key = _('without minimun stock')
            docs[key][production.routing_id.name].append(production)
            totals[key][production.routing_id.name] += production.product_qty
            totals['total'][production.routing_id.name] += \
                production.product_qty
        docargs = {
            'doc_ids': self._ids,
            'doc_model': report.model,
            'docs': docs,
            'totals': totals,
            'today': date.today().strftime('%d/%m/%Y')
        }
        return report_obj.render('custom_documents.mrp_production', docargs)
