# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Partner(models.Model):
    _inherit='res.partner'
    governateE = fields.Char(string='Governate')
    person_type = fields.Selection(string="Type", selection=[('B', 'Business In Egypt'), ('P', 'Natural Person'),('F', 'Foreigner'), ], required=False)
    regionCity = fields.Char(string='Region City')
    buildingNumber = fields.Char(string='Building Number')
    floor = fields.Char(string='Floor')
    room = fields.Char(string='Room')
    landmark = fields.Char(string='Landmark')
    additionalInformation = fields.Char(string='Additional Information')


