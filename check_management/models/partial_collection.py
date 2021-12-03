# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError


class PartialCollection(models.Model):
    _name = "partial.collection"

    partial_amount = fields.Float(string="Partial Amount")
    date = fields.Date(string="Date")
    check_id = fields.Many2one('payment.check.line')

    # for check history records
    @api.model
    def create(self, vals):
        rec = super(PartialCollection, self).create(vals)
        self.env['check.history'].create({'check_id': rec.check_id.id,
                                          'check_number': rec.check_id.check_number,
                                          'check_date': fields.date.today(),
                                          'check_amount': rec.partial_amount,
                                          'reason': 'Partial Cash'
                                          })
        return rec


# Collection btn
class PartialCollectionWizard(models.TransientModel):
    _name = "partial.collection.wizard"

    wizard_partial_amount = fields.Float(string="Partial Amount", required=True)
    debit_journal_id = fields.Many2one("account.journal", string="Debit Journal", required=True)
    credit_journal_id = fields.Many2one("account.journal", string="Credit Journal", required=True)
    date = fields.Date(required=True, default=fields.Date.context_today)

    # @api.multi
    def action_collection(self):
        self.ensure_one()
        x = self._context.get('active_id')
        check_rec = self.env['payment.check.line'].browse(x)
        total_partials = 0.0
        for line in check_rec.partial_collection_ids:
            total_partials += line.partial_amount
        if (total_partials + self.wizard_partial_amount) > check_rec.check_amount:
            raise ValidationError(_('Error ! total Partial Amount is bigger than the check amount'))

        partial = self.env['partial.collection'].create({'partial_amount': self.wizard_partial_amount,
                                                         'date': self.date,
                                                         'check_id': check_rec.id
                                                         })
        move_line_1 = {
            'account_id': self.debit_journal_id.default_account_id.id,
            'debit': self.wizard_partial_amount,
            'credit': 0.0,
            'partner_id': check_rec.payment_id.partner_id.id,
            'journal_id': self.debit_journal_id.id,

        }
        move_line_2 = {
            'account_id': self.credit_journal_id.default_account_id.id,
            'debit': 0.0,
            'credit': self.wizard_partial_amount,
            'partner_id': check_rec.payment_id.partner_id.id,
            'journal_id': self.credit_journal_id.id
        }
        lines = [(0, 0, move_line_1), (0, 0, move_line_2)]
        move_vals = {
            'date': self.date,
            'journal_id': self.credit_journal_id.id,
            'line_ids': lines,
        }
        move = self.env['account.move'].create(move_vals)
        if move:
            check_rec.write({'move_ids': [(4, move.id, None)]})


