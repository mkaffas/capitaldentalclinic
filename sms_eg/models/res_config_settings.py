""" Initialize Res Config Settings """

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    """ Inherit res.config.setting model to add Res configuration"""

    _inherit = 'res.config.settings'

    eg_username = fields.Char(
        related="company_id.eg_username",
        readonly=False
    )
    eg_password = fields.Char(
        related="company_id.eg_password",
        readonly=False
    )
    eg_sender = fields.Char(
        related="company_id.eg_sender",
        readonly=False
    )
