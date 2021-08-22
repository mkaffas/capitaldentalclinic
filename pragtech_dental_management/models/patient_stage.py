""" Initialize Patient Stage """

from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError, Warning


class PatientStage(models.Model):
    """
        Initialize Patient Stage:
    """
    _name = 'patient.stage'
    _description = 'Patient Stage'

    name = fields.Char(
        required=True,
        translate=True,
    )
    active = fields.Boolean(
        default=True
    )
