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


class stock_transfer_details_items(models.TransientModel):

    _inherit = 'stock.transfer_details_items'
    _order = 'product_id desc'

    @api.multi
    def split_all(self):
        for det in self:
            if det.quantity > 1:
                for x in range(1, int(det.quantity)):
                    det.quantity = (det.quantity-1)
                    new_id = det.copy(context=self.env.context)
                    new_id.quantity = 1
                    new_id.packop_id = False
                    new_id.put_in_pack()
                    if new_id.product_id and new_id.product_id.packaging_ids:
                        pack_ids = [x for x in new_id.product_id.packaging_ids
                                    if x.qty == 1]
                        if not pack_ids:
                            continue
                        pack = pack_ids[0]
                        new_id.result_package_id.measures = \
                            str(pack.ul.height) + 'X' + str(pack.ul.width) + \
                            'X' + str(pack.ul.length)
                        new_id.result_package_id.weight = pack.weight
                det.put_in_pack()
                if det.product_id and det.product_id.packaging_ids:
                    pack_ids = [x for x in det.product_id.packaging_ids if
                                x.qty == 1]
                    if not pack_ids:
                        continue
                    pack = pack_ids[0]
                    det.result_package_id.measures = str(pack.ul.height) + \
                        'X' + str(pack.ul.width) + 'X' + str(pack.ul.length)
                    det.result_package_id.weight = pack.weight
        if self and self[0]:
            return self[0].transfer_id.wizard_view()
