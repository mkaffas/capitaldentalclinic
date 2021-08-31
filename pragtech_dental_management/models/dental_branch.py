""" Initialize Dental Branch """

from odoo import fields, models


class DentalBranch(models.Model):
    """
        Initialize Dental Branch:
         -
    """
    _name = 'dental.branch'
    _description = 'Dental Branch'
    _check_company_auto = True

    name = fields.Char(
        required=True,
        translate=True,
    )
    active = fields.Boolean(
        default=True
    )
    room_ids = fields.One2many(
        'medical.hospital.oprating.room',
        'branch_id'
    )
