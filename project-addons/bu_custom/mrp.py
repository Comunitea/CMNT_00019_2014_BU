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


class MrpProduction(models.Model):

    _inherit = 'mrp.production'

    total_produced = fields.Float('Qty produced', compute='_get_produced_qty_', store=True)
    move_lines = fields.One2many('stock.move', 'raw_material_production_id',
                                 'Products to Consume',
                                 domain=[('state', 'not in', ('done', 'cancel'))],
                                 readonly=True,
                                 states={'draft': [('readonly', False)],
                                         'confirmed': [('readonly', False)],
                                         'ready': [('readonly', False)],
                                         'in_production': [('readonly', False)]
                                 })
    @api.one
    @api.depends('move_created_ids2')
    def _get_produced_qty_(self):
        self.total_produced = sum([x.product_uom_qty for x in
                                   self.move_created_ids2])
