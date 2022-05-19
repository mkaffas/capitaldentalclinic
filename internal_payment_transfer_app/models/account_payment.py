# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

class account_payment(models.Model):
	_inherit = "account.payment"

	internal_transfer_type = fields.Selection([('a_to_a', 'Account To Account'),('j_to_j', 'Journal To Journal'),('j_to_a','Journal To Account'),('a_to_j','Account To Journal')],string=' Internal Transfer Type',default='a_to_a')
	from_account_id = fields.Many2one('account.account',string="From Account")
	to_account_id = fields.Many2one('account.account',string="To Account")
	to_journal_id = fields.Many2one('account.journal',string="To Journal")
	from_journal_id = fields.Many2one('account.journal',string="From Journal")

	@api.onchange('journal_id')
	def get_from_account_id(self):
		for rec in self:
			rec.from_account_id=rec.journal_id.default_account_id.id



	@api.depends('destination_account_id', 'journal_id')
	def _compute_is_internal_transfer(self):
		pass
		# for payment in self:
		# 	is_partner_ok = payment.partner_id
		# 	is_account_ok = payment.destination_account_id or payment.journal_id.company_id.transfer_account_id
		# 	payment.is_internal_transfer = is_partner_ok and is_account_ok

	@api.onchange('journal_id', 'internal_transfer_type', 'is_internal_transfer')
	def _onchange_journal(self):
		payment_account_list = []
		if self.is_internal_transfer and self.internal_transfer_type in ['a_to_a','a_to_j']:
			account_ids = self.env['account.account'].search([('internal_type','in',('receivable', 'payable', 'liquidity','other'))])
			if account_ids:
				return {'domain': {'from_account_id': [('id', 'in', account_ids.ids)]}}
		return {}

	@api.depends('journal_id', 'partner_id', 'partner_type', 'is_internal_transfer', 'internal_transfer_type', 'to_account_id', 'to_journal_id')
	def _compute_destination_account_id(self):
		self.destination_account_id = False
		for pay in self:
			if pay.is_internal_transfer:
				pay.destination_account_id = pay.journal_id.company_id.transfer_account_id
				# Custom Code
				if pay.internal_transfer_type == 'a_to_a' :
					pay.destination_account_id = pay.to_account_id

				if pay.internal_transfer_type == 'a_to_j' :
					pay.destination_account_id = pay.to_journal_id.payment_debit_account_id or pay.journal_id.company_id.transfer_account_id

				if pay.internal_transfer_type == 'j_to_a' :
					pay.destination_account_id = pay.to_account_id

				if pay.internal_transfer_type == 'j_to_j' :
					pay.destination_account_id = pay.to_journal_id.payment_debit_account_id or pay.journal_id.company_id.transfer_account_id

			elif pay.partner_type == 'customer':
				# Receive money from invoice or send money to refund it.
				if pay.partner_id:
					pay.destination_account_id = pay.partner_id.with_company(pay.company_id).property_account_receivable_id
				else:
					pay.destination_account_id = self.env['account.account'].search([
						('company_id', '=', pay.company_id.id),
						('internal_type', '=', 'receivable'),
					], limit=1)
			elif pay.partner_type == 'supplier':
				# Send money to pay a bill or receive money to refund it.
				if pay.partner_id:
					pay.destination_account_id = pay.partner_id.with_company(pay.company_id).property_account_payable_id
				else:
					pay.destination_account_id = self.env['account.account'].search([
						('company_id', '=', pay.company_id.id),
						('internal_type', '=', 'payable'),
					], limit=1)


	def _prepare_move_line_default_vals(self, write_off_line_vals=None):
		''' Prepare the dictionary to create the default account.move.lines for the current payment.
		:param write_off_line_vals: Optional dictionary to create a write-off account.move.line easily containing:
			* amount:       The amount to be added to the counterpart amount.
			* name:         The label to set on the line.
			* account_id:   The account on which create the write-off.
		:return: A list of python dictionary to be passed to the account.move.line's 'create' method.
		'''
		self.ensure_one()
		write_off_line_vals = write_off_line_vals or {}

		if not self.journal_id.payment_debit_account_id or not self.journal_id.payment_credit_account_id:
			raise UserError(_(
				"You can't create a new payment without an outstanding payments/receipts account set on the %s journal.",
				self.journal_id.display_name))

		# Compute amounts.
		write_off_amount = write_off_line_vals.get('amount', 0.0)

		if self.payment_type == 'inbound':
			# Receive money.
			counterpart_amount = -self.amount
			write_off_amount *= -1
		elif self.payment_type == 'outbound':
			# Send money.
			counterpart_amount = self.amount
		else:
			counterpart_amount = 0.0
			write_off_amount = 0.0

		balance = self.currency_id._convert(counterpart_amount, self.company_id.currency_id, self.company_id, self.date)
		counterpart_amount_currency = counterpart_amount
		write_off_balance = self.currency_id._convert(write_off_amount, self.company_id.currency_id, self.company_id, self.date)
		write_off_amount_currency = write_off_amount
		currency_id = self.currency_id.id

		if self.is_internal_transfer:
			if self.payment_type == 'inbound':
				liquidity_line_name = _('Transfer to %s', self.journal_id.name)
			else: # payment.payment_type == 'outbound':
				liquidity_line_name = _('Transfer from %s', self.journal_id.name)
		else:
			liquidity_line_name = self.payment_reference

		# Compute a default label to set on the journal items.

		payment_display_name = {
			'outbound-customer': _("Customer Reimbursement"),
			'inbound-customer': _("Customer Payment"),
			'outbound-supplier': _("Vendor Payment"),
			'inbound-supplier': _("Vendor Reimbursement"),
		}

		default_line_name = self.env['account.move.line']._get_default_line_name(
			payment_display_name['%s-%s' % (self.payment_type, self.partner_type)],
			self.amount,
			self.currency_id,
			self.date,
			partner=self.partner_id,
		)

		liquidity_line_account =  self.journal_id.payment_debit_account_id.id if balance < 0.0 else self.journal_id.payment_credit_account_id.id

		# Custom Code
		if self.is_internal_transfer == True and self.internal_transfer_type == 'a_to_a' :
			liquidity_line_account = self.from_account_id.id

		if self.is_internal_transfer == True and self.internal_transfer_type == 'a_to_j' :
			liquidity_line_account = self.from_account_id.id

		if self.is_internal_transfer == True and self.internal_transfer_type == 'j_to_a' :
			liquidity_line_account = self.from_journal_id.payment_credit_account_id.id

		if self.is_internal_transfer == True and self.internal_transfer_type == 'j_to_j' :
			liquidity_line_account = self.from_journal_id.payment_credit_account_id.id

		line_vals_list = [
			# Liquidity line.
			{
				'name': liquidity_line_name or default_line_name,
				'date_maturity': self.date,
				'amount_currency': -counterpart_amount_currency,
				'currency_id': currency_id,
				'debit': balance < 0.0 and -balance or 0.0,
				'credit': balance > 0.0 and balance or 0.0,
				'partner_id': self.partner_id.id,
				'account_id': liquidity_line_account,
				'journal_id': self.from_journal_id.id,
			},
			# Receivable / Payable.
			{
				'name': self.payment_reference or default_line_name,
				'date_maturity': self.date,
				'amount_currency': counterpart_amount_currency + write_off_amount_currency if currency_id else 0.0,
				'currency_id': currency_id,
				'debit': balance + write_off_balance > 0.0 and balance + write_off_balance or 0.0,
				'credit': balance + write_off_balance < 0.0 and -balance - write_off_balance or 0.0,
				'partner_id': self.partner_id.id,
				'account_id': self.destination_account_id.id,
				'journal_id': self.to_journal_id.id,
			},
		]
		if write_off_balance:
			# Write-off line.
			line_vals_list.append({
				'name': write_off_line_vals.get('name') or default_line_name,
				'amount_currency': -write_off_amount_currency,
				'currency_id': currency_id,
				'debit': write_off_balance < 0.0 and -write_off_balance or 0.0,
				'credit': write_off_balance > 0.0 and write_off_balance or 0.0,
				'partner_id': self.partner_id.id,
				'account_id': write_off_line_vals.get('account_id'),
			})
		return line_vals_list


	def _seek_for_lines(self):
		''' Helper used to dispatch the journal items between:
		- The lines using the temporary liquidity account.
		- The lines using the counterpart account.
		- The lines being the write-off lines.
		:return: (liquidity_lines, counterpart_lines, writeoff_lines)
		'''
		self.ensure_one()

		liquidity_lines = self.env['account.move.line']
		counterpart_lines = self.env['account.move.line']
		writeoff_lines = self.env['account.move.line']

		for line in self.move_id.line_ids:
			if line.account_id in (
					self.journal_id.default_account_id,
					self.journal_id.payment_debit_account_id,
					self.journal_id.payment_credit_account_id,
			):
				liquidity_lines += line
			elif line.account_id.internal_type in ('receivable', 'payable', 'liquidity','other'):
				counterpart_lines += line
			else:
				writeoff_lines += line

		return liquidity_lines, counterpart_lines, writeoff_lines