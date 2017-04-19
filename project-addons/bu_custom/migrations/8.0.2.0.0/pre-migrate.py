# -*- coding: utf-8 -*-
# © 2017 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

def migrate(cr, version):
    cr.execute(""" UPDATE mrp_bom mb
                   SET name = '[' || pp.default_code || '] ' || pt.name
                   FROM product_template pt JOIN product_product pp ON pt.id = pp.product_tmpl_id
                   WHERE mb.product_tmpl_id = pt.id
 """)
