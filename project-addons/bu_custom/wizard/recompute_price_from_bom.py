# -*- coding: utf-8 -*-
# © 2016 Comunitea - Javier Colmenero <javier@comunitea.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, fields, api


class RecomputePriceFromBom(models.TransientModel):

    _name = 'recompute.price.from.bom'

    real_time_accounting = \
        fields.Boolean("Generate accounting entries when real-time",
                       default=False)
    recursive = fields.Boolean("Change prices of child BoMs too",
                               default=True)

    @api.multi
    def recompute_price_from_bom(self):
        boom_objs = self.env['mrp.bom'].search([])
        # Get all diferent product.template objs in the all the BoM
        prod_ids = boom_objs.mapped('product_tmpl_id.id')
        self.pool.get('product.template').\
            compute_price(self._cr, self._uid, [], template_ids=prod_ids,
                          real_time_accounting=self.real_time_accounting,
                          recursive=self.recursive)

    @api.model
    def _do_cron(self):
        self.create({}).recompute_price_from_bom()
