# -*- coding: utf-8 -*-

from odoo import fields, models, _
import xlsxwriter
import base64
import os


class balances(models.TransientModel):
    _name = 'elect.reasons.wiz'
    reason_id= fields.Many2one(comodel_name="elect.reasons", string="Reason", required=True)
    status = fields.Char()

    def apply(self):
        invoices=self.env['account.move'].browse(self._context.get('active_ids'))
        for invoice in invoices:
            print(">>D>D>",invoice.send_electronic_invoice,invoice.electronic_invoice_status)
            if invoice.send_electronic_invoice:
                if invoice.electronic_invoice_status =='cancelled':
                    pass
                elif invoice.electronic_invoice_status =='rejected':
                    pass
                else:
                    print(">>>>")
                    invoice.cancel_reject(self.status,self.reason_id.name)


