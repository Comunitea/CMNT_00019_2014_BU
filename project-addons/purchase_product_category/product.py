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


class material_category(models.Model):

    _name = 'product.material.category'

    name = fields.Char('Name', size=64)
    complete_name = fields.Char(string='Name', compute='_get_complete_name')

    parent_id = fields.Many2one('product.material.category','Parent Category', select=True, ondelete='cascade')
    child_id = fields.One2many('product.material.category', 'parent_id', string='Child Categories')
    parent_left = fields.Integer('Left Parent', select=1)
    parent_right = fields.Integer('Right Parent', select=1)

    _parent_name = "parent_id"
    _parent_store = True
    _parent_order = 'name'
    _order = 'parent_left'

    @api.v8
    def name_get(self):
        res = []
        for obj in self:
            name = obj.name
            if obj.parent_id:
                name = obj.parent_id.complete_name + '/' + obj.name
            res.append((obj.id, name))
        return res

    @api.v7
    def name_get(self, cr, uid, ids, context=None):
        if isinstance(ids, (list, tuple)) and not len(ids):
            return []
        if isinstance(ids, (long, int)):
            ids = [ids]
        reads = self.read(cr, uid, ids, ['name','parent_id'], context=context)
        res = []
        for record in reads:
            name = record['name']
            if record['parent_id']:
                name = record['parent_id'][1]+' / '+name
            res.append((record['id'], name))
        return res


    @api.one
    @api.depends('name', 'parent_id')
    def _get_complete_name(self):
        names = self.name_get()
        self.complete_name = names and names[0][1]


    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        if not args:
            args = []
        if name:
            # Be sure name_search is symetric to name_get
            name = name.split(' / ')[-1]
            ids = self.search([('name', operator, name)] + args, limit=limit)
        else:
            ids = self.search(args, limit=limit)
        return ids.name_get()

class product_template(models.Model):

    _inherit = 'product.template'

    material_categ_id = fields.Many2one('product.material.category', 'Material category')
