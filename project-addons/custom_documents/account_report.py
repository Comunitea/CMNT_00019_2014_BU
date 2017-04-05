# -*- coding: utf-8 -*-
# © 2017 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api, exceptions, _
from openerp.report import report_sxw

class invoice_report_sxw(report_sxw.rml_parse):
    pass

class invoice_report(models.AbstractModel):
    _name = 'report.account.report_invoice'
    _template = 'account.report_invoice'
    _inherit = 'report.abstract_report'
    _wrapped_report_class = invoice_report_sxw


class invoice_intrastat_report(models.AbstractModel):
    _name = 'report.report_intrastat.report_intrastatinvoice'
    _template = 'report_intrastat.report_intrastatinvoice'
    _inherit = 'report.abstract_report'
    _wrapped_report_class = invoice_report_sxw
