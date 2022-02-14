# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Uom(models.Model):
    _inherit='uom.uom'
    unit_type_id= fields.Many2one(comodel_name="uom.types", string="Unit Type", required=False)

class UnitType(models.Model):
    _name='uom.types'
    _rec_name='code'
    code= fields.Char(string="Code", required=False)
    desc_en= fields.Char(string="English Description", required=False)
    desc_ar= fields.Char(string="Arabic Description", required=False)
