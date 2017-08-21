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


class ResPartner(models.Model):

    _inherit = 'res.partner'

    checked_by = fields.Char('Checked by')
    document_name = fields.Char('Document name',
                                compute='_get_document_name')

    @api.multi
    def _get_top_document_name(self):
        if self.parent_id:
           return self.parent_id._get_top_document_name()
        else:
            return self.name
        return ''
    @api.multi
    def _get_document_name(self):
        for partner in self:
            partner.document_name = partner._get_top_document_name()
