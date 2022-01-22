# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError


class CheckHistory(models.Model):
    _name = "check.history"
    _description = 'Check History'

    check_id = fields.Many2one('payment.check.line')
    check_number = fields.Char(string="Check Number", required=True)
    check_date = fields.Date(required=True)
    check_amount = fields.Float(string="Check Amount", required=True)
    reason = fields.Char(string="Reason")
    # check_bank_id = fields.Many2one('res.bank', string="Bank Name", required=True)
    # bank_branch = fields.Char(string="Bank Branch")
    # partner_id = fields.Many2one('res.partner', string="Partner Name", related="payment_id.partner_id")
    # with_drawer_name = fields.Char(string="With Drawer Name")
    # account_owner = fields.Char(string="Account Owner")
    # state = fields.Selection([('holding', 'Holding'),
    #                           ('depoisted', 'Depoisted'),
    #                           ('to_vendor', 'To Vendor'),
    #                           ('paid_vendor', 'Paid Vendor'),
    #                           ('accepted', 'Accepted'),
    #                           ('rejected', 'Rejected'),
    #                           ('close', 'Closed'),
    #                           ('cancel', 'Cancelled')
    #                           ], string='Check State',
    #                          copy=False, default='holding')
    # payment_id = fields.Many2one('account.payment', ondelete='cascade', index=True, copy=False)