# -*- coding: utf-8 -*-

from odoo import models, fields, _
from datetime import timedelta
from odoo.exceptions import UserError


class Payment_Branch(models.TransientModel):
    _name = 'payment.branch'

    today = fields.Boolean(string="", )
    yesterday = fields.Boolean(string="", )

    def open(self):
        for rec in self:
            records = []
            if rec.yesterday and rec.today:
                records = self.env('account.payment').sudo().search(
                    ['|', ('date', '=', fields.Date.today()), (fields.Date.today() - timedelta(days=1)),
                     ("branch_id", 'in', self.env.user.partner_id.branchs_ids.ids)]).ids
            elif rec.yesterday:
                records = self.env('account.payment').sudo().search([(fields.Date.today() - timedelta(days=1)),
                                                                     ("branch_id", 'in',
                                                                      self.env.user.partner_id.branchs_ids.ids)]).ids
            elif rec.today:
                records = self.env('account.payment').sudo().search([('date', '=', fields.Date.today()),
                                                                     ("branch_id", 'in',
                                                                      self.env.user.partner_id.branchs_ids.ids)]).ids
            else:
                raise UserError(_('You must choose today or yesterday'))
            print("records",records)
            return {
                'name': _('Check Lines'),
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'account.payment',
                'view_id': False,
                'type': 'ir.actions.act_window',
                'domain': [('id', 'in', records)],
            }

