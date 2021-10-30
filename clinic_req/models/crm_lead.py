# -*- coding: utf-8 -*-

from datetime import datetime

from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DF


class CRM(models.Model):
    _inherit = "crm.lead",

    patient = fields.Char('Patient', required=True, )
    appointment_id = fields.Many2one('medical.appointment', 'Patient')
    nationality = fields.Many2one(comodel_name="res.country",
                                  string="nationality", required=False, )

    @api.depends('birthday')
    def compute_age(self):
        for partner in self:
            if partner.birthday:
                today = fields.date.today()
                born = datetime.strptime(str(partner.birthday), '%Y-%m-%d')
                partner.age = today.year - born.year - (
                        (today.month, today.day) < (born.month, born.day))
            else:
                partner.age = 0

    patient_id = fields.Many2one(comodel_name="medical.patient", string="",
                                 required=False, )
    # activity_ids = fields.Many2many(comodel_name="mail.activity", string="Activities",compute="get_activity" )
    #
    # @api.depends('patient_id')
    # def get_activity(self):
    #     for line in self:
    #         list_activity = []
    #         for activity in self.env['mail.activity'].search([('patient_id','=',line.patient_id.id)]):
    #             list_activity.append(activity.id)
    #         line.activity_ids = [(6, 0, list_activity)]

    refer_patient_id = fields.Many2one(comodel_name="medical.patient",
                                       string="Referred By", required=False, )
    age = fields.Integer('Age', compute='compute_age')
    occupation_id = fields.Many2one('medical.occupation', 'Occupation')
    birthday = fields.Date('Birth Date')
    gender = fields.Selection([('m', 'Male'), ('f', 'Female'), ], 'Gender', )
    chief = fields.Many2one(comodel_name='chief.complaint',
                            string="Chief Complaint", required=False, )
    case = fields.Char(string="Case ID", compute='get_case_id')
    appointment_count = fields.Integer(string="Appointments", required=False,
                                       compute='count_appointment')
    name = fields.Char('Opportunity', required=False, index=True,
                       compute="get_name_opportunity")
    marital_status = fields.Selection(
        [('s', 'Single'), ('m', 'Married'), ('w', 'Widowed'), ('d', 'Divorced'),
         ('x', 'Separated'), ],
        'Marital Status')
    is_create_patient = fields.Boolean(string="", )
    referring_doctor_id = fields.Many2one('medical.physician',
                                          'Referring  Doctor', )
    branch_id = fields.Many2one(
        'dental.branch', group_expand='_group_expand_branch',
    )
    room_id = fields.Many2one(
        'medical.hospital.oprating.room', 'Room',
        required=False, tracking=True,
        domain="[('branch_id', '=', branch_id)]",
        group_expand='_group_expand_room'
    )

    @api.depends('mobile', 'patient')
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
                records = self.env['medical.appointment'].search(
                    [('crm_id', '=', line.id)])
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
            'context': {'default_crm_id': self.id, },
            'target': 'current',

        }

    def create_patient(self):
        partner_obj = self.env['res.partner'].sudo()
        partner = partner_obj.create({
            'name': self.patient,
            'is_patient': True,
            'type': 'contact',
            'mobile': self.mobile,
            'email': self.email_from,
            'phone': self.phone,
            'street': self.street,
            'street2': self.street2,
            'zip': self.zip,
            'city': self.city,
            'state_id': self.state_id.id,
            'country_id': self.country_id.id,
        })
        patient_obj = self.env['medical.patient'].sudo()
        patient = patient_obj.create({
            'partner_id': partner.id,
            'dob': self.birthday,
            'sex': self.gender,
            'marital_status': self.marital_status,
            'mobile': self.mobile,
            'occupation_id': self.occupation_id.id,
            'medium_id': self.medium_id.id,
            'source_id': self.source_id.id,
            'referred': self.referred,
            'email': self.email_from,
            'phone': self.phone,
            'chief': self.chief.id,
            'tag_ids': self.tag_ids.ids,
            'nationality_id': self.nationality.id,
            'note': self.description,
        })
        self.patient_id = patient.id
        self.is_create_patient = True

    def create_appointment(self):

        appointment_obj = self.env['medical.appointment']
        if not self.patient_id:
            raise UserError(_("Please create Patient."))
        vals = {
            'patient': self.patient_id.id,
            'crm_id': self.id,
            'chief': self.chief.id,
            'room_id': self.room_id.id,
            'branch_id': self.branch_id.id,
        }

        appointment = appointment_obj.sudo().create(vals)
        self.appointment_id = appointment.id
        wiz_form_id = self.env['ir.model.data'].get_object_reference(
            'pragtech_dental_management', 'medical_appointment_gantt')[1]
        return {
            'view_type': 'gantt',
            'view_id': wiz_form_id,
            'view_mode': 'gantt',
            'res_model': 'medical.appointment',
            'res_id': appointment.id,
            'nodestroy': True,
            'target': 'current',
            'type': 'ir.actions.act_window',
        }


class Chief_Complaint(models.Model):
    _name = 'chief.complaint'

    name = fields.Char()


class Survey(models.Model):
    _inherit = 'survey.survey'

    appointment_id = fields.Many2one(comodel_name="medical.appointment", string="", required=False, )


class Activites(models.Model):
    _inherit = 'mail.activity'

    patient_id = fields.Many2one(comodel_name="medical.patient", string="Patient", required=False, )
    phone = fields.Char(related='patient_id.phone', store=True, readonly=False)
    mobile = fields.Char(related='patient_id.mobile', store=True,
                         readonly=False)
    dob = fields.Date(related='patient_id.dob',string='Date of Birth')

    # def send_sms(self):
    #     obj = self.env['sms.eg'].sudo()
    #     for line in self:
    #         obj.create({
    #             'partner_ids': [(4, line.patient_id.partner_id.id)],
    #             'message': 'comment', })

    def action_send_sms(self):
        mail_ids = self.env['mail.activity'].browse(self._context.get('active_ids', False))
        lines = []
        for line in mail_ids:
            lines.append(line.patient_id.partner_id.id)
        return {'type': 'ir.actions.act_window',
                'name': _('Send SMS'),
                'res_model': 'sms.eg',
                'target': 'new',
                'view_id': self.env.ref('sms_eg.sms_eg_form').id,
                'view_mode': 'form',
                'context': {'default_partner_ids': [(6,0, lines)],'default_message': 'comment',}
                }


class Survey_app(models.Model):
    _name = 'appointment.survey'
    _rec_name = 'patient_id'
    _description = 'New Description'

    appointment_id = fields.Many2one(comodel_name="medical.appointment", string="Appointment", required=True, )
    patient_id = fields.Many2one(comodel_name="medical.patient", string="Patient", required=True, )
    doctor = fields.Many2one(comodel_name="medical.physician", string="Dentist", required=True, )
    state = fields.Selection(
        [('draft', 'Draft'),
         ('confirmed', 'Confirmed')], 'State',
        readonly=True, default='draft', tracking=True, )
    priority_reception = fields.Selection(
        [('0', 'Low'), ('1', 'Medium'), ('2', 'Medium'), ('3', 'High'), ('4', 'Normal High'), ('5', 'Very High')],
        'Reception', default='0', index=True)
    priority_medical_procedure = fields.Selection(
        [('0', 'Low'), ('1', 'Medium'), ('2', 'Medium'), ('3', 'High'), ('4', 'Normal High'), ('5', 'Very High')],
        'Medical Procedure', default='0', index=True)
    priority_sterilization_hygiene = fields.Selection(
        [('0', 'Low'), ('1', 'Medium'), ('2', 'Medium'), ('3', 'High'), ('4', 'Normal High'), ('5', 'Very High')],
        'Sterilization and hygiene', default='0', index=True)
    desc = fields.Text(string="Description", required=False, )

    def confirm(self):
        self.state = 'confirmed'


class Appointment(models.Model):
    _inherit = 'medical.appointment'

    crm_id = fields.Many2one(comodel_name="crm.lead", string="",
                             required=False, )
    patient_coordinator = fields.Many2one(comodel_name="res.users",
                                          string="Patient Coordinator",
                                          related='patient.coordinator_id')
    chief = fields.Many2one(comodel_name='chief.complaint',
                            string="Chief Complaint", required=False, )

    def cancel(self):
        for rec in self:
            partners = self.env.ref(
                'pragtech_dental_management.group_branch_manager').users.filtered(
                lambda r: r.partner_id).mapped('partner_id.id')
            body = '<a target=_BLANK href="/web?#id=' + str(
                rec.id) + '&view_type=form&model=medical.appointment&action=" style="font-weight: bold">' + str(
                rec.name) + '</a>'
            if rec.doctor.user_id.partner_id:
                partners.append(rec.doctor.user_id.partner_id.id)
            if rec.patient_coordinator.partner_id:
                partners.append(rec.patient_coordinator.partner_id.id)
            if partners:
                rec.sudo().message_post(
                    partner_ids=partners,
                    subject="Appointment " + str(rec.name) + " is Cancelled",
                    body="Appointment " + body + "is Cancelled with patient " + str(
                        rec.patient.partner_id.name),
                    message_type='comment',
                    subtype_id=self.env.ref('mail.mt_note').id, )
        self.write({'state': 'cancel'})

    def notify_patient_coordinator(self):
        for rec in self:
            if not rec.patient_coordinator:
                raise UserError(_("Please Add Patient Coordinator."))
            # partners = [x.partner_id.id for x in self.env.ref('pragtech_dental_management.group_branch_manager').users]
            body = '<a target=_BLANK href="/web?#id=' + str(
                rec.id) + '&view_type=form&model=medical.appointment&action=" style="font-weight: bold">' + str(
                rec.name) + '</a>'
            if rec.patient_coordinator:
                self.sudo().message_post(
                    partner_ids=[self.patient_coordinator.partner_id.id],
                    subject="Appointment " + str(
                        rec.name) + "with patient " + str(
                        rec.patient.partner_id.name),
                    body="You will be coordinator in Appointment " + body + "with patient " + str(
                        rec.patient.partner_id.name),
                    message_type='comment',
                    subtype_id=self.env.ref('mail.mt_note').id, )

    def open_survey(self):
        """Method Open survey."""
        context = dict(self._context or {})
        wiz_form_id = self.env['ir.model.data'].get_object_reference(
            'clinic_req', 'appointment_survey_form')[1]
        return {
            'view_type': 'form',
            'view_id': wiz_form_id,
            'view_mode': 'form',
            'res_model': 'appointment.survey',
            # 'res_id': self.invc_id.id,
            'type': 'ir.actions.act_window',
            'target': 'current',
            'context': {'default_appointment_id': self.id,'default_patient_id':self.patient.id,'default_doctor':self.doctor.id},
        }

    # def open_survey(self):
    #     """Method Open survey."""
    #     context = dict(self._context or {})
    #     wiz_form_id = self.env['ir.model.data'].get_object_reference(
    #         'survey', 'survey_form')[1]
    #     return {
    #         'view_type': 'form',
    #         'view_id': wiz_form_id,
    #         'view_mode': 'form',
    #         'res_model': 'survey.survey',
    #         # 'res_id': self.invc_id.id,
    #         'type': 'ir.actions.act_window',
    #         'target': 'current',
    #         'context': {'default_appointment_id': self.id},
    #     }


class Physician(models.TransientModel):
    _name = 'physician.wizard'

    wizard_dentist_id = fields.Many2one(comodel_name="medical.physician", string="Dentist", required=True, )

    def select_doctor(self):
        patient_ids = self.env['medical.patient'].browse(self._context.get('active_ids', False))
        for line in patient_ids:
            for record in line.teeth_treatment_ids:
                record.dentist = self.wizard_dentist_id.id


class Patient(models.Model):
    _inherit = 'medical.patient'
    discount = fields.Float(string='Discount', digits='Discount',
                            default=0.0)
    service_amount = fields.Float(string="Service amount before tax",
                                  compute="get_amount_totals", )
    service_net = fields.Float(string="Service net amount",
                               compute="get_amount_totals", )
    total_discount = fields.Float(string="Total Discount",
                                  compute="get_amount_totals", tracking=True)
    total_payment = fields.Float(string="Total payment",
                                 compute="get_amount_totals", )
    total_net = fields.Float(string="Total Net", compute="get_amount_totals", )
    chief = fields.Many2one(comodel_name='chief.complaint',
                            string="Chief Complaint", required=False, )
    tag_ids = fields.Many2many(
        'crm.tag'
    )
    wizard_dentist_id = fields.Many2one(comodel_name="medical.physician", string="Dentist", required=False, )
    discount_for_total = fields.Float(string='Additional Discount total', digits='Discount',
                                      tracking=True,
                                      default=0.0)
    is_selected = fields.Boolean(string="Select All",  )
    discount_option = fields.Selection(string="Discount type", selection=[('percentage', 'Percentage'), ('fixed', 'Fixed'), ],default='percentage', required=False, )


    def send_sms(self):
        obj = self.env['sms.eg'].sudo()
        for line in self:
            obj.create({
                'partner_ids': [(4, line.partner_id.id)],
                'message': 'comment', })

    def action_appointment(self):

        appointment_obj = self.env['medical.appointment']
        vals = {
            'patient': self.id,
            'doctor': False,
            'appointment_edate': False,
            'appointment_sdate': False,
        }

        appointment = appointment_obj.sudo().create(vals)
        # self.appointment_id = appointment.id
        wiz_form_id = self.env['ir.model.data'].get_object_reference(
            'pragtech_dental_management', 'medical_appointment_gantt')[1]
        return {
            'view_type': 'gantt',
            'view_id': wiz_form_id,
            'view_mode': 'gantt',
            'res_model': 'medical.appointment',
            'res_id': appointment.id,
            'nodestroy': True,
            'target': 'current',
            'type': 'ir.actions.act_window',
        }

    @api.depends('teeth_treatment_ids', 'teeth_treatment_ids.amount', 'teeth_treatment_ids.discount',
                 'teeth_treatment_ids.net_amount','discount_for_total')
    def get_amount_totals(self):
        service_amount = 0
        service_net = 0
        total_payment = 0
        total_net = 0
        for record in self:
            for line in record.teeth_treatment_ids:
                service_amount += line.amount
                service_net += line.net_amount
            record.total_discount = service_amount - service_net
            record.service_amount = service_amount
            record.service_net = service_net
            obj_payment = self.env['account.payment'].search(
                [('partner_id', '=', record.partner_id.id)])
            for payment in obj_payment:
                if payment.payment_type == 'inbound':
                    total_payment += payment.amount
                elif payment.payment_type == 'outbound':
                    total_payment -= payment.amount
            record.total_payment = total_payment
            total_net = record.service_net - record.total_payment
            record.total_net = total_net - record.discount_for_total

    @api.onchange('discount_for_total')
    def change_total_discount(self):
        discount_amount_line = self.discount_for_total / len(self.teeth_treatment_ids)
        for line in self.teeth_treatment_ids:
            line.discount_amount = discount_amount_line + line.discount_amount
            line.get_discount()

    def open_partner_ledger(self):
        return {
            'type': 'ir.actions.client',
            'name': _('Partner Ledger'),
            'tag': 'account_report',
            'params': {
                'options': {'partner_ids': [self.partner_id.id]},
                'ignore_session': 'both',
            },
            'context': "{'model':'account.partner.ledger'}"
        }

    def dentist_multi_choose(self):
        return {'type': 'ir.actions.act_window',
                'name': _('Assign Doctor'),
                'res_model': 'physician.wizard',
                'target': 'new',
                'view_id': self.env.ref('clinic_req.assign_doctor_form').id,
                'view_mode': 'form',
                }
        # for line in self.teeth_treatment_ids:
        #     if self.wizard_dentist_id:
        #         line.dentist = self.wizard_dentist_id.id

    @api.onchange('is_selected')
    def select_all(self):
        if self.is_selected == True:
            for line in self.teeth_treatment_ids:
                line.is_selected = True
        else:
            for line in self.teeth_treatment_ids:
                line.is_selected = False

    # def unselect_all(self):
    #     for line in self.teeth_treatment_ids:
    #         line.is_selected = False

    def delete_selection(self):
        for line in self.teeth_treatment_ids:
            if line.is_selected == True and line.inv == False:
                line.sudo().unlink()
            elif line.is_selected == True and line.inv == False:
                raise UserError(
                    _('Can not delete this operation %s because you have an invoice on it  !!') % (line.description))

    def service_confirmation(self):
        for line in self.teeth_treatment_ids:
            if line.is_selected == True and line.inv == False:
                journal_id = self.env['account.journal'].search([
                    ('type', '=', 'sale')], limit=1)
                inv_line_main = {
                    'name': line.description.name,
                    'price_unit': line.amount or 0.00,
                    'quantity': 1,
                    'discount': line.discount,
                    'account_id': line.description.property_account_income_id.id or line.description.categ_id.property_account_income_categ_id.id or False,
                }
                inv_values = {
                    'partner_id': self.partner_id.id,
                    # 'patient_id': self.id,
                    'dentist': line.dentist.id,
                    'move_type': 'out_invoice',
                    'invoice_date': datetime.now().strftime(DF) or False,
                    'journal_id': journal_id and journal_id.id or False,
                    'teeth_id': self.id or False,
                }
                acc_id = self.env['account.move'].sudo().create(inv_values)
                acc_id.sudo().write({'invoice_line_ids': [(0, 0, inv_line_main)]})
                acc_id.action_post()
                line.sudo().write({'invc_id': acc_id.id, 'inv': True})

    def get_all_discount(self):
        for line in self.teeth_treatment_ids:
            if self.discount_option == 'percentage':
                if line.is_selected == True:
                    line.discount = self.discount
                    line.get_discount_amount()
                    line.is_selected = False
            elif self.discount_option == 'fixed':
                if line.is_selected == True:
                    line.discount_amount = self.discount
                    line.get_discount()
                    line.is_selected = False


class Teeth(models.Model):
    _inherit = 'medical.teeth.treatment'

    inv = fields.Boolean(string='Is Invoice?')
    invc_id = fields.Many2one('account.move', string='Invoice')
    account_id = fields.Many2one(comodel_name="account.account",
                                 string="Account", required=False, )
    discount = fields.Float(string='Discount (%)', digits='Discount',
                            tracking=True,
                            default=0.0)
    net_amount = fields.Float(string="Net Amount", compute="get_net_amount")
    is_selected = fields.Boolean(string="", )

    @api.constrains('discount')
    def check(self):
        if self.env.user.has_group('clinic_req.discount_user_group'):
            obj = self.env['discount.limitation'].search(
                [('group_id', '=', 'Discount User')], limit=1)
            if obj.discount_limitation < self.discount:
                raise UserError(_('You are not allowed this discount !!'))
        elif self.env.user.has_group('clinic_req.discount_manager_group'):
            obj = self.env['discount.limitation'].search(
                [('group_id', '=', 'Discount Manager')], limit=1)
            if obj.discount_limitation < self.discount:
                raise UserError(_('You are not allowed this discount !!'))
        elif self.env.user.has_group('clinic_req.discount_admin_group'):
            obj = self.env['discount.limitation'].search(
                [('group_id', '=', 'Discount Admin')], limit=1)
            if obj.discount_limitation < self.discount:
                raise UserError(_('You are not allowed this discount !!'))

    @api.depends('discount', 'amount')
    def get_net_amount(self):
        for line in self:
            line.net_amount = line.amount - (
                    (line.amount * line.discount) / 100)

    discount_amount = fields.Float(string="Discount Amount", required=False, )

    @api.onchange('discount', 'amount')
    def get_discount_amount(self):
        for line in self:
            line.discount_amount = (line.amount * line.discount) / 100

    @api.onchange('discount_amount', 'amount')
    def get_discount(self):
        for line in self:
            if line.amount != 0:
                line.discount = (line.discount_amount / (line.amount)) * 100

    @api.model
    def create(self, values):
        res = super(Teeth, self).create(values)

        for line in res:
            if not self.env.user.has_group('group_dental_admin'):
                partners = self.env.ref(
                    'pragtech_dental_management.group_branch_manager').users.filtered(
                    lambda r: r.partner_id).mapped('partner_id.id')
                partners_admin = self.env.ref(
                    'pragtech_dental_management.group_dental_admin').users.filtered(
                    lambda r: r.partner_id).mapped('partner_id.id')
                all_partners = partners
                body = '<a target=_BLANK href="/web?#id=' + str(
                    line.patient_id.id) + '&view_type=form&model=medical.patient&action=" style="font-weight: bold">' + '</a>'
                if all_partners:
                    line.sudo().message_post(
                        partner_ids=all_partners,
                        subject="Operation " + str(
                            line.description.name) + " is created",
                        body="New service " + body + "added to Patient " + str(
                            line.patient_id.partner_id.name),
                        message_type='comment',
                        subtype_id=self.env.ref('mail.mt_note').id)
        return res

    def create_invoice(self):
        """Create invoice for Rent Schedule."""
        for line in self:
            # if not line.account_id:
            #     raise UserError(_('Please Add the incoming Account !!'))
            self.ensure_one()
            journal_id = self.env['account.journal'].search([
                ('type', '=', 'sale')], limit=1)
            inv_line_main = {
                'name': line.description.name,
                'price_unit': line.amount or 0.00,
                'quantity': 1,
                'discount': line.discount,
                'account_id': line.description.property_account_income_id.id or line.description.categ_id.property_account_income_categ_id.id or False,
            }
            inv_values = {
                'partner_id': line.patient_id.partner_id.id,
                'patient_id': line.patient_id.id,
                'dentist': line.dentist.id,
                'move_type': 'out_invoice',
                'invoice_date': datetime.now().strftime(DF) or False,
                'journal_id': journal_id and journal_id.id or False,
                'teeth_id': line.patient_id and line.patient_id.id or False,
            }
            acc_id = self.env['account.move'].create(inv_values)
            acc_id.write({'invoice_line_ids': [(0, 0, inv_line_main)]})
            acc_id.action_post()
            self.write({'invc_id': acc_id.id, 'inv': True})
            # context = dict(self._context or {})
            # wiz_form_id = self.env['ir.model.data'].get_object_reference(
            #     'account', 'view_move_form')[1]
            #
            # return {
            #     'view_type': 'form',
            #     'view_id': wiz_form_id,
            #     'view_mode': 'form',
            #     'res_model': 'account.move',
            #     'res_id': self.invc_id.id,
            #     'type': 'ir.actions.act_window',
            #     'target': 'current',
            #     'context': context,
            # }

    def open_invoice(self):
        """Method Open Invoice."""
        context = dict(self._context or {})
        wiz_form_id = self.env['ir.model.data'].get_object_reference(
            'account', 'view_move_form')[1]
        return {
            'view_type': 'form',
            'view_id': wiz_form_id,
            'view_mode': 'form',
            'res_model': 'account.move',
            'res_id': self.invc_id.id,
            'type': 'ir.actions.act_window',
            'target': 'current',
            'context': context,
        }


class NewModule(models.Model):
    _inherit = 'account.move'

    teeth_id = fields.Many2one(comodel_name="medical.patient", string="",
                               required=False, )
