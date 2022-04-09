# -*- coding: utf-8 -*-

from odoo import models, _
from odoo.exceptions import UserError


class ProductTemplateInherit(models.Model):
    _inherit = 'product.template'

    def action_archive(self):
        if self.env.user.id not in self.env.ref(
                "pragtech_dental_management.group_dental_mng_menu").users.ids and self.env.user.id not in self.env.ref(
                "base.group_system").users.ids and self.env.user.id not in self.env.ref(
                "pragtech_dental_management.group_dental_admin").users.ids:
            raise UserError(_("You can't archive"))
        return super(ProductTemplateInherit, self).action_archive()
