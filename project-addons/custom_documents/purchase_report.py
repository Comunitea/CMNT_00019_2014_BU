# -*- coding: utf-8 -*-
# © 2017 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from openerp import models
from openerp.report import report_sxw

class purchase_report_sxw(report_sxw.rml_parse):
    pass

class purchase_report(models.AbstractModel):
    _name = 'report.purchase.report_purchaseorder'
    _template = 'purchase.report_purchaseorder'
    _inherit = 'report.abstract_report'
    _wrapped_report_class = purchase_report_sxw
