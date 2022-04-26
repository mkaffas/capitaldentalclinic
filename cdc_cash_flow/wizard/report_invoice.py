# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class ReportInvoice(models.TransientModel):
    _name = 'report.invoice'
    _description = 'Report Invoice'

    date_from = fields.Date(string="Date From", required=True, )
    date_to = fields.Date(string="Date To", required=True, )

    @api.onchange('date_form', 'date_to')
    def check_date(self):
        for rec in self:
            if rec.date_to < rec.date_from:
                raise UserError(_("The date to must be less than the end date form"))

    def export_xlsx(self):
        return self.env.ref(
            'cdc_cash_flow.id_report_invoice_xlsx').report_action(self)

class AccountTage(models.Model):
    _name = 'account.tage'
    _rec_name = 'name'
    _description = 'account tage'

    name = fields.Char(string="Name", required=True,)
    type = fields.Selection(string="", selection=[('in', 'CASH IN'), ('out', 'CASH OUT'), ], required=True, )

class AccountAccount(models.Model):
    _inherit = 'account.account'

    tage_id = fields.Many2one(comodel_name="account.tage", string="Cash Flow Tage", required=False, )
