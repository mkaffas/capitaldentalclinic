# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountJournal(models.Model):
    _inherit = "account.journal"
    # determine if this journal responsible for checks
    is_check = fields.Boolean(string="Is Check", default=False)
    # determine if this journal responsible for checks && existing check
    is_debit = fields.Boolean(string="Is Debit", default=False)


# Depoiset btn journals
class CheckDepoiset(models.TransientModel):
    _name = 'check.depoiset'
    _description = 'Depoiset Journals'

    debit_journal_id = fields.Many2one("account.journal", string="Debit Journal", required=True)
    # credit_journal_id = fields.Many2one("account.journal", string="Credit Journal")
    date = fields.Date(required=True, default=fields.Date.context_today)

    # @api.multi
    def action_depoiset(self):
        self.ensure_one()
        x = self._context.get('active_id')
        # print("ID = ", x)
        check_rec = self.env['payment.check.line'].browse(x)
        debit_notes_account = check_rec.payment_id.journal_id.default_account_id.id
        check_amount = check_rec.check_amount
        move_line_1 = {
            'account_id': self.debit_journal_id.default_account_id.id,
            'debit': check_amount,
            'credit': 0.0,
            'partner_id': check_rec.payment_id.partner_id.id,
            'journal_id': self.debit_journal_id.id,

        }
        move_line_2 = {
            'account_id': debit_notes_account,
            'debit': 0.0,
            'credit': check_amount,
            'partner_id': check_rec.payment_id.partner_id.id,
            'journal_id': self.debit_journal_id.id
        }
        lines = [(0, 0, move_line_1), (0, 0, move_line_2)]
        move_vals = {
            'date': self.date,
            'journal_id': self.debit_journal_id.id,
            'line_ids': lines,
        }
        move = self.env['account.move'].create(move_vals)
        if move:
            check_rec.write({'move_ids': [(4, move.id, None)]})
            check_rec.check_under_col = self.debit_journal_id.default_account_id.id
            check_rec.depoiset_journal_id = self.debit_journal_id.id
            check_rec.state = 'depoisted'
            # for check history records
            # self.env['check.history'].create({'check_id': check_rec.id,
            #                                   'check_number': check_rec.check_number,
            #                                   'check_date': check_rec.check_date,
            #                                   'check_amount': check_rec.check_amount,
            #                                   'reason': 'Deposited Check'
            #                                  })


# accepted btn journals
class CheckAccept(models.TransientModel):
    _name = 'check.accept'
    _description = 'Accept Journals'

    debit_journal_id = fields.Many2one("account.journal", string="Debit Journal", required=True)
    # credit_journal_id = fields.Many2one("account.journal", string="Credit Journal")
    date = fields.Date(required=True, default=fields.Date.context_today)

    # @api.multi
    def action_accept(self):
        self.ensure_one()
        x = self._context.get('active_id')
        check_rec = self.env['payment.check.line'].browse(x)
        check_under_col_account = check_rec.check_under_col.id
        check_amount = check_rec.check_amount
        move_line_1 = {
            'account_id': self.debit_journal_id.default_account_id.id,
            'debit': check_amount,
            'credit': 0.0,
            'partner_id': check_rec.payment_id.partner_id.id,
            'journal_id': self.debit_journal_id.id
        }
        move_line_2 = {
            'account_id': check_under_col_account,
            'debit': 0.0,
            'credit': check_amount,
            'partner_id': check_rec.payment_id.partner_id.id,
            'journal_id': self.debit_journal_id.id
        }
        lines = [(0, 0, move_line_1), (0, 0, move_line_2)]
        move_vals = {
            'date': self.date,
            'journal_id': self.debit_journal_id.id,
            'line_ids': lines,
        }
        move = self.env['account.move'].create(move_vals)
        if move:
            check_rec.write({'move_ids': [(4, move.id, None)]})
            check_rec.state = 'accepted'


# Reject btn journals
class CheckReject(models.TransientModel):
    _name = 'check.reject'
    _description = 'Reject Journals'

    debit_journal_id = fields.Many2one("account.journal", string="Debit Journal", required=True)
    notes = fields.Text(string="rejected Reasons")
    date = fields.Date(required=True, default=fields.Date.context_today)

    # @api.multi
    def action_reject(self):
        self.ensure_one()
        x = self._context.get('active_id')
        check_rec = self.env['payment.check.line'].browse(x)
        debit_notes_account = check_rec.payment_id.journal_id.default_account_id.id
        # check_under_col_account = check_rec.check_under_col.id
        check_amount = check_rec.check_amount

        move_line_1 = {
            'account_id': debit_notes_account,
            'debit': check_amount,
            'credit': 0.0,
            'partner_id': check_rec.payment_id.partner_id.id,
            'journal_id': check_rec.depoiset_journal_id.id
        }
        move_line_2 = {
            'account_id': self.debit_journal_id.default_account_id.id,
            'debit': 0.0,
            'credit': check_amount,
            'partner_id': check_rec.payment_id.partner_id.id,
            'journal_id': check_rec.depoiset_journal_id.id
        }
        lines = [(0, 0, move_line_1), (0, 0, move_line_2)]
        move_vals = {
            'date': self.date,
            'journal_id': check_rec.depoiset_journal_id.id,
            'line_ids': lines,
        }
        move = self.env['account.move'].create(move_vals)
        if move:
            check_rec.rejected_notes = self.notes
            check_rec.write({'move_ids': [(4, move.id, None)]})
            check_rec.state = 'rejected'


# Deducted btn journals
class CheckDeduct(models.TransientModel):
    _name = 'check.deduct'
    _description = 'Deduct Journals'

    credit_journal_id = fields.Many2one("account.journal", string="Credit Journal", required=True)
    # credit_journal_id = fields.Many2one("account.journal", string="Credit Journal")
    date = fields.Date(required=True, default=fields.Date.context_today)

    # @api.multi
    def action_deduct(self):
        self.ensure_one()
        x = self._context.get('active_id')
        check_rec = self.env['payment.check.line'].browse(x)
        # check_under_col_account = check_rec.check_under_col.id
        check_amount = check_rec.check_amount
        move_line_1 = {
            'account_id': self.credit_journal_id.default_account_id.id,
            'debit': 0.0,
            'credit': check_amount,
            'partner_id': check_rec.payment_id.partner_id.id,
            'journal_id': self.credit_journal_id.id
        }
        move_line_2 = {
            'account_id': check_rec.payment_id.journal_id.default_account_id.id,
            'debit': check_amount,
            'credit': 0.0,
            'partner_id': check_rec.payment_id.partner_id.id,
            'journal_id': self.credit_journal_id.id
        }
        lines = [(0, 0, move_line_2), (0, 0, move_line_1)]
        move_vals = {
            'date': self.date,
            'journal_id': self.credit_journal_id.id,
            'line_ids': lines,
        }
        move = self.env['account.move'].create(move_vals)
        if move:
            check_rec.write({'move_ids': [(4, move.id, None)]})
            check_rec.state = 'paid_vendor'


# Deducted Transfer
class TransferDeduct(models.TransientModel):
    _name = 'transfer.deduct'
    _description = 'Deduct Transfer'

    bank_journal_id = fields.Many2one("account.journal", string="Bank Journal", required=True)
    cash_journal_id = fields.Many2one("account.journal", string="Cash Journal", required=True)
    date = fields.Date(required=True, default=fields.Date.context_today)

    # @api.multi
    def action_transfer_deduct(self):
        self.ensure_one()
        x = self._context.get('active_id')
        check_rec = self.env['payment.check.line'].browse(x)
        # check_under_col_account = check_rec.check_under_col.id
        check_amount = check_rec.check_amount
        move_line_1 = {
            'account_id': check_rec.payment_id.destination_journal_id.default_account_id.id,
            'debit': 0.0,
            'credit': check_amount,
            'journal_id': self.cash_journal_id.id
        }
        move_line_2 = {
            'account_id': self.cash_journal_id.default_account_id.id,
            'debit': check_amount,
            'credit': 0.0,
            'journal_id': self.cash_journal_id.id
        }
        lines = [(0, 0, move_line_2), (0, 0, move_line_1)]
        move_vals = {
            'date': self.date,
            'journal_id': self.cash_journal_id.id,
            'line_ids': lines,
        }
        move1 = self.env['account.move'].create(move_vals)
        if move1:
            check_rec.write({'move_ids': [(4, move1.id, None)]})

        move_line_3 = {
            'account_id': self.bank_journal_id.default_account_id.id,
            'debit': 0.0,
            'credit': check_amount,
            'journal_id': self.bank_journal_id.id
        }
        move_line_4 = {
            'account_id': check_rec.payment_id.journal_id.default_account_id.id,
            'debit': check_amount,
            'credit': 0.0,
            'journal_id': self.bank_journal_id.id
        }
        lines = [(0, 0, move_line_4), (0, 0, move_line_3)]
        move_vals = {
            'date': self.date,
            'journal_id': self.bank_journal_id.id,
            'line_ids': lines,
        }
        move2 = self.env['account.move'].create(move_vals)
        if move2:
            check_rec.write({'move_ids': [(4, move2.id, None)]})
            check_rec.state = 'complete_transfer'
