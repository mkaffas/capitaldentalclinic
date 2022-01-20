# -*- coding: utf-8 -*-
import datetime
from datetime import datetime

from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DF


class Partner(models.Model):
    _inherit = 'res.partner'

    ref_patient = fields.Char(string="Reference Patient", compute="get_ref",store=True )

    def get_ref(self):
        for line in self:
            obj = self.env['medical.patient'].search([('partner_id','=',line.id)],limit=1)
            if obj:
                line.ref_patient = obj.patient_id
            else:
                line.ref_patient = ''

    @api.depends('name', 'ref_patient')
    def name_get(self):
        result = []
        for partner in self:
            name = partner.name
            if partner.ref_patient:
                name = '[' + partner.ref_patient + ']' + name
            result.append((partner.id, name))
        return result

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        args = args or []
        recs = self.browse()
        if name:
            recs = self.search(
                ['|', ('name', operator, name), ('ref_patient', operator, name)])
        if not recs:
            recs = self.search([('name', operator, name)])
        return recs.name_get()