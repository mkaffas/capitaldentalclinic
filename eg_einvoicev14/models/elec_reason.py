from odoo import api, fields, models
from odoo.exceptions import ValidationError


class EleReason(models.Model):
    _name='elect.reasons'
    name = fields.Char(string="Name", required=True)

