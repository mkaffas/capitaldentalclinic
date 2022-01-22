# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError


class NewModule(models.Model):
    _inherit = 'account.move'

    einv_is_submitted = fields.Boolean()


class PaymentCheck(models.Model):
    _name = "payment.check"

    name = fields.Char(string="Title")
    partner_id = fields.Many2one('res.partner', string="Partner Name")
    amount = fields.Float(string="Amount")
    payment_date = fields.Date()
    state = fields.Selection([('draft', 'Draft'), ('posted', 'Posted')], string='State',
                                    copy=False, default='draft')
    journal_id = fields.Many2one('account.journal', string="Payment Journal")
    check_lines = fields.One2many('payment.check.line', 'payment_check_id')
    payment_type = fields.Selection([('send', 'Send'), ('receive', 'Receive')], string='Payment Type',
                             copy=False, default='send')

    # @api.multi
    def button_check_lines(self):
        return {
            'name': _('Check Lines'),
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'payment.check.line',
            'view_id': False,
            'type': 'ir.actions.act_window',
            'domain': [('id', 'in', self.check_lines.ids)],
        }


class PaymentCheckLine(models.Model):
    _name = "payment.check.line"
    _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']
    _rec_name = 'check_number'

    check_number = fields.Char(string="Check Number", required=True)
    check_date = fields.Date(required=True)
    check_amount = fields.Float(string="Check Amount", required=True)
    check_bank_id = fields.Many2one('res.bank', string="Bank Name", required=True)
    bank_branch = fields.Char(string="Bank Branch")
    partner_id = fields.Many2one('res.partner', string="Partner Name", related="payment_id.partner_id")
    with_drawer_name = fields.Char(string="With Drawer Name")
    account_owner = fields.Char(string="Account Owner")
    state = fields.Selection([('holding', 'Holding'),
                              ('depoisted', 'Depoisted'),
                              ('to_vendor', 'To Vendor'),
                              ('paid_vendor', 'Paid Vendor'),
                              ('accepted', 'Accepted'),
                              ('rejected', 'Rejected'),
                              ('close', 'Closed'),
                              ('returned', 'Returned'),
                              ('cancel', 'Cancelled'),
                              ('complete_transfer', 'Complete Transfer')
                              ], string='Check State',
                               copy=False, default='holding')
    payment_check_id = fields.Many2one('payment.check', ondelete='cascade', index=True, copy=False)
    payment_id = fields.Many2one('account.payment', ondelete='cascade', index=True, copy=False)
    payment_state = fields.Selection([('draft', 'Draft'), ('posted', 'Posted'), ('sent', 'Sent'), ('reconciled', 'Reconciled'),
                              ('cancelled', 'Cancelled')], copy=False, string="Status", related="payment_id.state")
    check_type = fields.Selection(
        [('outbound', 'Send'), ('inbound', 'Received'), ('transfer', 'Internal Transfer')], copy=False, string="Check Type", compute="_compute_check_type", store=True)
    mozahar = fields.Selection([('moz', 'مظهر'), ('not_moz', 'غير مظهر')], copy=False, string="مظهر")
    mosatar = fields.Selection([('mos', 'مسطر'), ('not_mos', 'غير مسطر')], copy=False, string="مسطر")
    desc = fields.Char(string="Desc")

    # for reserve customer check id in case to pay this check to vendor
    customer_check_id = fields.Many2one('payment.check.line')
    # for bank buttons
    # from pop window of depoiset btn store default debit account of journal selected
    check_under_col = fields.Many2one('account.account')
    depoiset_journal_id = fields.Many2one('account.journal')
    # new_field_ids = fields.Many2many(comodel_name="", relation="", column1="", column2="", string="", )
    rejected_notes = fields.Text(string="Rejected Notes")
    move_ids = fields.Many2many('account.move',relation="move_idddd",)
    invoice_ids = fields.Many2many('account.move',string="Invoices", copy=False, readonly=True)
                                   #saber ,related="payment_id.invoice_ids")
    partial_collection_ids = fields.One2many('partial.collection', 'check_id')
    partial_state = fields.Selection([('partial', 'Partial'), ('no_partial', 'No Partial')], copy=False,
                                     string="Partial Or NOT", default='no_partial')
    remaining_amount = fields.Float(string="Remaining Amount", default='0.0', compute='compute_remaining_partials')





    # for partial collections
    @api.depends('partial_collection_ids','partial_collection_ids.partial_amount')
    def compute_remaining_partials(self):
        for check in self:
            if check.partial_collection_ids:
                total=0.0
                for partial in check.partial_collection_ids:
                    total += partial.partial_amount
                check.remaining_amount = check.check_amount - total
                check.partial_state = 'partial'
            else:
                check.remaining_amount = 0.0
                check.partial_state = 'no_partial'

    def action_return_customer(self):
        self.ensure_one()
        move_line_1 = {
            'account_id': self.payment_id.partner_id.property_account_receivable_id.id,
            'debit': self.check_amount,
            'credit': 0.0,
            'partner_id': self.payment_id.partner_id.id,
            'journal_id': self.payment_id.journal_id.id
        }
        move_line_2 = {
            'account_id': self.payment_id.journal_id.default_account_id.id,
            'debit': 0.0,
            'credit': self.check_amount,
            'partner_id': self.payment_id.partner_id.id,
            'journal_id': self.payment_id.journal_id.id
        }
        lines = [(0, 0, move_line_1), (0, 0, move_line_2)]
        move_vals = {
            'date': fields.Date.today(),
            'journal_id': self.payment_id.journal_id.id,
            'line_ids': lines,
        }
        move = self.env['account.move'].create(move_vals)
        if move:
            self.write({'move_ids': [(4, move.id, None)]})

        # for inverse account.move
        # move1 = self.env['account.move'].search([('name', '=', self.payment_id.move_name)])
        # if self.payment_id:
        #     self.payment_id.cancel()
        #     self.write({'state': 'returned'})

    def action_return_vendor(self):
        self.ensure_one()
        move_line_1 = {
            # 'account_id': self.payment_id.partner_id.property_account_receivable_id.id,
            'account_id': self.payment_id.journal_id.default_account_id.id,
            'debit': self.check_amount,
            'credit': 0.0,
            'partner_id': self.payment_id.partner_id.id,
            'journal_id': self.payment_id.journal_id.id
        }
        move_line_2 = {
            # 'account_id': self.payment_id.journal_id.default_account_id.id,
            'account_id': self.payment_id.partner_id.property_account_receivable_id.id,
            'debit': 0.0,
            'credit': self.check_amount,
            'partner_id': self.payment_id.partner_id.id,
            'journal_id': self.payment_id.journal_id.id
        }
        lines = [(0, 0, move_line_1), (0, 0, move_line_2)]
        move_vals = {
            'date': fields.Date.today(),
            'journal_id': self.payment_id.journal_id.id,
            'line_ids': lines,
        }
        move = self.env['account.move'].create(move_vals)
        if move:
            self.write({'move_ids': [(4, move.id, None)]})

    #         for test multi records return btn
    # @api.multi
    def test_return(self):
        line_ids = []
        payment_ids = []
        # take ids of checks
        for line in self:
            line_ids.append(line.id)
        payment_ids = self.mapped('payment_id')
        print(payment_ids)
        # must be one payment
        if len(payment_ids) > 1:
            raise UserError("Error , some of checks are not in the same payment")

        # check must be in holding or rejected state
        for line in self:
            if line.state not in ['holding', 'rejected']:
                raise UserError("Sorry , some of checks are not in the State  [Holding Or Rejected]")
        # take payment record
        payment_rec = []
        for line in self:
            payment_rec = line.payment_id
            line.payment_id.cancel2()
            break
        # for inverse account.move
        # self.action_return()

        # for line in self:
        #     if line.payment_id:
        #         line.write({'payment_id': False})
        # payment_rec.compute_total_check_amount()
        # payment_rec.action_draft()
        # payment_rec.post()
        for line in self:
            if line.check_type == 'inbound':
                line.action_return_customer()
                line.state = 'cancel'
            if line.check_type == 'outbound':
                line.action_return_vendor()
                line.state = 'returned'
            # make state of customer existing check holding
            if line.customer_check_id:
                line.customer_check_id.state = 'holding'
            # line.write({'payment_id': payment_rec.id})

    # def action_accept(self):
    #     self.write({'state': 'accepted'})

    # def action_reject(self):
    #     self.write({'state': 'rejected'})

    def action_cancel(self):
        self.write({'state': 'cancel'})

    def action_reset(self):
        self.write({'state': 'holding'})

    def execute_kill(self):
        self.write({'state': 'close'})

    def reset_to_holding(self):
        self.ensure_one()
        move_line_1 = {
            'account_id': self.payment_id.partner_id.property_account_receivable_id.id,
            # 'account_id': self.payment_id.journal_id.default_account_id.id,
            'debit': self.check_amount,
            'credit': 0.0,
            'journal_id': self.payment_id.journal_id.id,
            'partner_id': self.payment_id.partner_id.id
        }
        move_line_2 = {
            'account_id': self.payment_id.journal_id.default_account_id.id,
            # 'account_id': self.payment_id.partner_id.property_account_receivable_id.id,
            'debit': 0.0,
            'credit': self.check_amount,
            'journal_id': self.payment_id.journal_id.id,
            'partner_id': self.payment_id.partner_id.id
        }
        lines = [(0, 0, move_line_1), (0, 0, move_line_2)]
        move_vals = {
            'date': fields.Date.today(),
            'journal_id': self.payment_id.journal_id.id,
            'line_ids': lines,
        }
        move = self.env['account.move'].create(move_vals)
        if move:
            self.write({'move_ids': [(4, move.id, None)]})
            self.state = 'holding'

    # for smart btn
    # @api.multi
    def button_journal_items(self):
        return {
            'name': _('Journal Items'),
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'account.move',
            'view_id': False,
            'type': 'ir.actions.act_window',
            'domain': [('id', 'in', self.move_ids.ids)],
        }

    # @api.multi
    def unlink(self):
        for rec in self:
            if rec.state != 'cancel':
                raise UserError("Sorry, you can not delete this cheque it should be in cancel state")
            return super(PaymentCheckLine, self).unlink()

    @api.depends('payment_id.payment_type')
    def _compute_check_type(self):
        for line in self:
            if line.payment_id:
                if line.payment_id.payment_type == 'outbound':
                    line.check_type = 'outbound'
                if line.payment_id.payment_type == 'inbound':
                    line.check_type = 'inbound'
                if line.payment_id.payment_type == 'transfer':
                    line.check_type = 'transfer'

    # for check history records
    @api.model
    def create(self, vals):
        rec = super(PaymentCheckLine, self).create(vals)
        self.env['check.history'].create({'check_id': rec.id,
                                          'check_number': rec.check_number,
                                          'check_date': fields.date.today(),
                                          'check_amount': rec.check_amount,
                                          'reason': 'Created Check'
                                          })
        return rec

    # for check history records
    # @api.multi
    def write(self, vals):
        rec = super(PaymentCheckLine, self).write(vals)
        print(rec)
        print(vals)
        print(self)
        if 'state' in vals:
            self.env['check.history'].create({'check_id': self.id,
                                              'check_number': self.check_number,
                                              'check_date': fields.date.today(),
                                              'check_amount': self.check_amount,
                                              'reason': vals['state']
                                              })
        return rec

    # for smart btn
    # @api.multi
    def button_check_history(self):
        return {
            'name': _('Check History'),
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'check.history',
            'view_id': False,
            'type': 'ir.actions.act_window',
            'domain': [('check_id', '=', self.id)],
        }

    # @api.multi
    def action_transfer_return(self):
        self.ensure_one()
        x = self.id
        check_rec = self.env['payment.check.line'].browse(x)
        check_amount = check_rec.check_amount
        liq_account = self.env.user.company_id.transfer_account_id
        move_line_1 = {
            'account_id': check_rec.payment_id.destination_journal_id.default_account_id.id,
            'debit': 0.0,
            'credit': check_amount,
            'journal_id': check_rec.payment_id.destination_journal_id.id
        }
        move_line_2 = {
            'account_id': liq_account.id,
            'debit': check_amount,
            'credit': 0.0,
            'journal_id': check_rec.payment_id.destination_journal_id.id
        }
        lines = [(0, 0, move_line_2), (0, 0, move_line_1)]
        move_vals = {
            'date': fields.Date.today(),
            'journal_id': check_rec.payment_id.destination_journal_id.id,
            'line_ids': lines,
        }
        move1 = self.env['account.move'].create(move_vals)
        if move1:
            check_rec.write({'move_ids': [(4, move1.id, None)]})

        move_line_3 = {
            'account_id': liq_account.id,
            'debit': 0.0,
            'credit': check_amount,
            'journal_id': check_rec.payment_id.journal_id.id
        }
        move_line_4 = {
            'account_id': check_rec.payment_id.journal_id.default_account_id.id,
            'debit': check_amount,
            'credit': 0.0,
            'journal_id': check_rec.payment_id.journal_id.id
        }
        lines = [(0, 0, move_line_4), (0, 0, move_line_3)]
        move_vals = {
            'date': fields.Date.today(),
            'journal_id': check_rec.payment_id.journal_id.id,
            'line_ids': lines,
        }
        move2 = self.env['account.move'].create(move_vals)
        if move2:
            check_rec.write({'move_ids': [(4, move2.id, None)]})
            check_rec.state = 'cancel'
