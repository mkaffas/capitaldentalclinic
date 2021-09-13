""" Initialize Res Company """

from odoo import fields, models


class ResCompany(models.Model):
    """
        Inherit Res Company:
    """
    _inherit = 'res.company'

    eg_username = fields.Char(
        string="Username"
    )
    eg_password = fields.Char(
        string="Password"
    )
    eg_sender = fields.Char(
        string="Sender ID"
    )
