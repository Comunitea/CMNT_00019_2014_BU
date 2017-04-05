# -*- coding: utf-8 -*-
# © 2017 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from openerp import models, fields, api, exceptions, _
from openerp.report import report_sxw

class sale_report_sxw(report_sxw.rml_parse):
    pass

class sale_report(models.AbstractModel):
    _name = 'report.sale.report_saleorder'
    _template = 'sale.report_saleorder'
    _inherit = 'report.abstract_report'
    _wrapped_report_class = sale_report_sxw
