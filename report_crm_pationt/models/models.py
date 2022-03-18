# -*- coding: utf-8 -*-

from odoo import models, fields, api


class crm_stage(models.Model):
    _inherit = 'crm.stage'

    is_closed_stage = fields.Boolean(string="", )


class crm_lead(models.Model):
    _inherit = 'crm.lead'

    closed_on = fields.Date(string="", required=False, )
    closed_py = fields.Many2one(comodel_name="res.users", string="", required=False, )

    @api.constrains('stage_id')
    def get_closed_date(self):
        for rec in self:
            if rec.stage_id.is_closed_stage:
                rec.closed_on = fields.date.today()
                rec.closed_py = self.env.user.id


class CrmPatient(models.TransientModel):
    _name = 'crm.patient'
    _description = 'Crm Patient'

    create_date_from = fields.Datetime(string="Created Date From", required=False, )
    create_date_to = fields.Datetime(string="Created Date To", required=False, )
    closed_date_from = fields.Date(string="Closed Date From", required=False, )
    closed_date_to = fields.Date(string="Closed Date To", required=False, )
    creation_ids = fields.Many2many(comodel_name="res.users", string="Created Users", relation="creation__tapel",
                                    column1="creation_1", column2="creation_2", )
    closed_ids = fields.Many2many(comodel_name="res.users", string="Closed User", relation="closed_tapel",
                                  column1="closed_1", column2="closed_2", )

    def creation_patient(self):
        return self.env.ref(
            'report_crm_pationt.id_crm_patient_report').report_action(self)


class GeneralLedgerAccount(models.AbstractModel):
    _name = 'report.report_crm_pationt.crm_patient_template'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, patient):
        sheet = workbook.add_worksheet('Crm Patient Report')
        format1 = workbook.add_format({'font_size': 15, 'align': 'center','border': 5})
        format2 = workbook.add_format(
            {'font_size': 13, 'align': 'center', 'bold': True,'border': 5,'bg_color': '#97CF5C',})
        format3 = workbook.add_format(
            {'align': 'center', 'bold': True,  'color': 'black', 'border': 5})
        sheet.set_column('A:A', 25)
        sheet.set_column('B:B', 25)
        sheet.set_column('C:C', 25)
        sheet.set_column('D:D', 20)
        sheet.set_column('E:E', 20)
        sheet.set_column('F:F', 20)
        sheet.set_column('G:G', 20)
        sheet.set_column('H:H', 20)
        sheet.set_column('I:I', 20)
        sheet.set_column('J:J', 20)
        sheet.set_column('K:K', 20)
        row = 1
        for rec in patient:
            sheet.merge_range(0, 2, 0, 7, 'Report Crm patient', format3)
            row += 1
            sheet.write(row, 0, 'Opportunity', format2)
            sheet.write(row, 1, 'Created on', format2)
            sheet.write(row, 2, 'Closed on', format2)
            sheet.write(row, 3, 'closing  Duration', format2)
            sheet.write(row, 4, 'Source', format2)
            sheet.write(row, 5, 'Medium', format2)
            sheet.write(row, 6, 'Campaign', format2)
            sheet.write(row, 7, 'Created by', format2)
            sheet.write(row, 8, 'Closed by', format2)
            sheet.write(row, 9, 'Lost reason', format2)
            domain=[]
            if rec.create_date_from:
                domain.append(('create_date','>=',rec.create_date_from))
            if rec.create_date_to:
                domain.append(('create_date','<=',rec.create_date_to))
            if rec.closed_date_from:
                domain.append(('closed_on','>=',rec.closed_date_from))
            if rec.closed_date_to:
                domain.append(('closed_on','<=',rec.closed_date_to))
            if rec.creation_ids:
                domain.append(('create_uid','in',rec.creation_ids.ids))
            if rec.closed_ids:
                domain.append(('closed_py','in',rec.closed_ids.ids))
            crm_leads=self.env['crm.lead'].search(domain)
            for line in crm_leads:
                row += 1
                duration=""
                if line.closed_on and line.create_date:
                    duration=line.closed_on-line.create_date.date()
                sheet.write(row, 0, line.name, format1)
                sheet.write(row, 1, str(line.create_date), format1)
                sheet.write(row, 2, str(line.closed_on or "") or "", format1)
                sheet.write(row, 3, duration, format1)
                sheet.write(row, 4, line.source_id.name or "", format1)
                sheet.write(row, 5, line.medium_id.name or "", format1)
                sheet.write(row, 6, line.campaign_id.name or "", format1)
                sheet.write(row, 7, line.create_uid.name or "", format1)
                sheet.write(row, 8, line.closed_py.name or "", format1)
                sheet.write(row, 9, line.lost_reason.name or "", format1)

