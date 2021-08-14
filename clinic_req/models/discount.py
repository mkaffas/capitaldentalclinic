# -*- coding: utf-8 -*-

from odoo import api, fields, models ,_
from odoo.exceptions import UserError



class discount(models.Model):

    _name = 'discount.limitation'
    _rec_name = 'group_id'

    group_id = fields.Many2one('res.groups')
    discount_limitation = fields.Integer(default=1)

    @api.constrains('discount_limitation')
    def check(self):
        for line in self:
            if line.discount_limitation == 0:
                raise UserError(_('Discount limit can not be Zero!'))