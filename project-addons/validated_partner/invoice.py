# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2015 Pexego All Rights Reserved
#    $Omar Castiñeira Saavedra <omar@pexego.es>$
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

from openerp import models, api, _, exceptions


class AccountInvoice(models.Model):

    _inherit = "account.invoice"

    @api.multi
    def invoice_validate(self):
        boss_group = self.env.ref("validated_partner.group_account_boss",
                                  False)
        for invoice in self:
            if not invoice.partner_id.validated:
                if boss_group not in self.env.user.groups_id:
                    raise exceptions.Warning(_("Cannot validate this "
                                               "invoice because partner is "
                                               "not validated and you are "
                                               "not in Financial Boss "
                                               "group"))
        return super(AccountInvoice, self).invoice_validate()
