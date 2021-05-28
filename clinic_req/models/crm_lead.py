# -*- coding: utf-8 -*-

from odoo import api, models, fields
import json
from datetime import datetime


class CRM(models.Model):
    _inherit = "crm.lead",

    patient = fields.Many2one('medical.patient', 'Patient ID', required=True, )
    nationality = fields.Many2one(comodel_name="res.country", string="nationality", required=False, )

    @api.depends('birthday')
    def compute_age(self):
        for partner in self:
            if partner.birthday:
                today = fields.date.today()
                born = datetime.strptime(str(partner.birthday), '%Y-%m-%d')
                partner.age = today.year - born.year - ((today.month, today.day) < (born.month, born.day))
            else:
                partner.age = 0

    age = fields.Integer('Age', compute='compute_age')
    birthday = fields.Date('Birth Day')
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], 'Gender')
    chief = fields.Char(string="Chief Complaint", required=False, )
    case = fields.Integer(string="Case ID",)
    appointment_count = fields.Integer(string="Appointments", required=False, compute='count_appointment')

    # @api.depends('id')
    # def get_case_id(self):
    #     for case in self:
    #         case.case = case.id

    # @api.depends('appointment_count')
    def count_appointment(self):
        for line in self:
            appointment_count = 0
            if line.id:
                records = self.env['medical.appointment'].search([('crm_id', '=', line.id)])
                for rec in records:
                    appointment_count += 1
            line.appointment_count = appointment_count

    def open_appointment(self):
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'medical.appointment',
            'view_mode': 'tree,form',
            'view_type': 'form',
            'name': 'Appointment',
            'domain': [('crm_id', '=', self.id)],
            'context': {'default_patient': self.patient.id, 'default_crm_id': self.id,},
            'target': 'current',

        }

    def create_appointment(self):
        obj = self.env['medical.appointment']
        for line in self:
            appointment_vals = {
                'crm_id': line.id,
                'patient': line.patient.id,
            }
            obj.sudo().create(appointment_vals)


class Appointment(models.Model):
    _inherit = 'medical.appointment'

    crm_id = fields.Many2one(comodel_name="crm.lead", string="", required=False, )
