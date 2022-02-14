# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Company(models.Model):
    _inherit = 'res.company'
    person_type = fields.Selection(string="Type", selection=[('B', 'Business In Egypt'), ('P', 'Natural Person'),
                                                             ('F', 'Foreigner'), ], required=False)
    governateE = fields.Char(string='Governate')
    regionCity = fields.Char(string='Region City')
    buildingNumber = fields.Char(string='Building Number')
    floor = fields.Char(string='Floor')
    room = fields.Char(string='Room')
    landmark = fields.Char(string='Landmark')
    additionalInformation = fields.Char(string='Additional Information')
    branchID = fields.Char(string='Branch Id')
    reg_no = fields.Char(string='Registration Number')
    activity_code = fields.Char(string='Taxpayer Activity Code')
    type = fields.Selection(string="Type",
                            selection=[('B', 'Business In Egypt'), ('P', 'Natural Person'), ('F', 'Foreigner'), ],
                            required=False)
    clientId = fields.Text(string='Client Id')
    clientSecret = fields.Text(string='Client Secret')
    configType = fields.Selection([('UAT', 'EEI-UAT Env'), ('PRD', 'EEI-PRD Env'), ('SIT', 'EEI-SIT Env')],
                                  string='Electronic Invoice Platform')
    invoiceVersion = fields.Selection([('0.9', '0.9'), ('1.0', '1.0')], string='Electronic Invoice Version',
                                      default='0.9', )
    sign_url = fields.Char(string="Signature URl", required=False, )

