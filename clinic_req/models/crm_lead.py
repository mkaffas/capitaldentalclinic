# -*- coding: utf-8 -*-

from odoo import api, models, fields ,_
import json
from datetime import datetime
from odoo.exceptions import UserError


class CRM(models.Model):
    _inherit = "crm.lead",

    patient = fields.Char('Patient', required=True, )
    appointment_id = fields.Many2one('medical.appointment', 'Patient', required=True, )
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

    patient_id = fields.Many2one(comodel_name="medical.patient", string="", required=False, )
    age = fields.Integer('Age', compute='compute_age')
    occupation_id = fields.Many2one('medical.occupation', 'Occupation')
    birthday = fields.Date('Birth Date')
    gender = fields.Selection([('m', 'Male'), ('f', 'Female'), ], 'Gender', )
    chief = fields.Many2one(comodel_name='chief.complaint',string="Chief Complaint", required=False, )
    case = fields.Char(string="Case ID",compute='get_case_id')
    appointment_count = fields.Integer(string="Appointments", required=False, compute='count_appointment')
    name = fields.Char('Opportunity', required=False, index=True,compute="get_name_opportunity")
    marital_status = fields.Selection(
        [('s', 'Single'), ('m', 'Married'), ('w', 'Widowed'), ('d', 'Divorced'), ('x', 'Separated'), ],
        'Marital Status')
    is_create_patient = fields.Boolean(string="",  )

    @api.depends('mobile','patient')
    def get_name_opportunity(self):
        for line in self:
            if line.patient and line.mobile:
                line.name = line.patient + ' / ' + str(line.mobile)
            else:
                line.name = ' / '

    def get_case_id(self):
        for case in self:
            if case.id:
                case.case = case.id
            else:
                case.case = '0'

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
            'context': {'default_crm_id': self.id,},
            'target': 'current',

        }

    def create_patient(self):
        partner_obj = self.env['res.partner']

        # vals_partner =
        partner = partner_obj.sudo().create({
            'name': self.patient,
            'is_patient': True,
            'type': 'contact'

        })
        patient_obj = self.env['medical.patient']
        patient = patient_obj.sudo().create({
            'partner_id': partner.id,
            'dob': self.birthday,
            'sex': self.gender,
            'marital_status': self.marital_status,
            'other_mobile': self.mobile,
            'occupation_id': self.occupation_id.id,
            'medium_id': self.medium_id.id,
        })
        self.patient_id = patient.id
        self.is_create_patient = True


    def create_appointment(self):

        appointment_obj = self.env['medical.appointment']
        if not self.patient_id:
            raise UserError(_("Please create Patient."))
        vals = {
            'patient': self.patient_id.id,
            'crm_id':self.id,
            'chief':self.chief.id,
        }

        appointment = appointment_obj.sudo().create(vals)
        self.appointment_id = appointment.id
        wiz_form_id = self.env['ir.model.data'].get_object_reference(
            'pragtech_dental_management', 'medical_appointment_view')[1]
        return {
            'view_type': 'form',
            'view_id': wiz_form_id,
            'view_mode': 'form',
            'res_model': 'medical.appointment',
            'res_id': appointment.id,
            'nodestroy': True,
            'target': 'current',
            'type': 'ir.actions.act_window',
        }


class Chief_Complaint(models.Model):
    _name = 'chief.complaint'

    name = fields.Char()


class Appointment(models.Model):
    _inherit = 'medical.appointment'

    crm_id = fields.Many2one(comodel_name="crm.lead", string="", required=False, )
    patient_coordinator = fields.Many2one(comodel_name="res.users", string="Patient Coordinator", required=False, )
    chief = fields.Many2one(comodel_name='chief.complaint', string="Chief Complaint", required=False, )

    def cancel(self):
        for rec in self:
            partners = [x.partner_id.id for x in self.env.ref('pragtech_dental_management.group_branch_manager').users]
            body ='<a target=_BLANK href="/web?#id=' + str(
                rec.id) + '&view_type=form&model=medical.appointment&action=" style="font-weight: bold">' + str(
                rec.name) + '</a>'
            if rec.doctor:
                partners.append(rec.doctor.user_id.partner_id.id)
            if rec.patient_coordinator:
                partners.append(rec.patient_coordinator.partner_id.id)
            if partners:
                self.sudo().message_post(
                    partner_ids=partners,
                    subject="Appointment " + str(rec.name) + " is Cancelled",
                    body="Appointment " + body + "is Cancelled with patient "+ str(rec.patient.partner_id.name),
                    message_type='comment',
                    subtype_id=self.env.ref('mail.mt_note').id,)
        self.write({'state': 'cancel'})

    def notify_patient_coordinator(self):
        for rec in self:
            if not rec.patient_coordinator:
                raise UserError(_("Please Add Patient Coordinator."))
            # partners = [x.partner_id.id for x in self.env.ref('pragtech_dental_management.group_branch_manager').users]
            body ='<a target=_BLANK href="/web?#id=' + str(
                rec.id) + '&view_type=form&model=medical.appointment&action=" style="font-weight: bold">' + str(
                rec.name) + '</a>'
            if rec.patient_coordinator:
                self.sudo().message_post(
                    partner_ids=[self.patient_coordinator.partner_id.id],
                    subject="Appointment " + str(rec.name) + "with patient " + str(rec.patient.partner_id.name),
                    body="You will be coordinator in Appointment " + body + "with patient "+ str(rec.patient.partner_id.name),
                    message_type='comment',
                    subtype_id=self.env.ref('mail.mt_note').id,)
