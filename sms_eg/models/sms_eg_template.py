""" Initialize Sms Eg Template """

from odoo import fields, models


class SmsEgTemplate(models.Model):
    """
        Initialize Sms Eg Template:
    """
    _name = 'sms.eg.template'
    _description = 'Sms Eg Template'

    name = fields.Char(
        required=True
    )
    message = fields.Text(
        required=True,
        translate=True
    )
