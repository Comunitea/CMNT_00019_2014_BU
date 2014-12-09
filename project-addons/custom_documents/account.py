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
from datetime import date


class AccountInvoice(models.Model):

    _inherit = "account.invoice"

    validation_date = fields.Date('Validation date')
    validated_by = fields.Many2one('res.users', 'Validated by')
    shipping_address = fields.Many2one('res.partner', 'Shipping address')

    @api.multi
    def invoice_validate(self):
        self.write({'validation_date': date.today(), 'validated_by': self.env.user.id})
        return super(AccountInvoice, self).invoice_validate()
