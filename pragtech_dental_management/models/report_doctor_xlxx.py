# -*- coding: utf-8 -*-

from odoo import _, api, fields, models


class DoctorReport(models.TransientModel):
    _name = 'doctor.report'
    _description = 'DoctorReport'

    start_date = fields.Datetime(string="Star Date", required=True, )
    end_date = fields.Datetime(string="End date", required=True, default=fields.Datetime.now)
    # dentist = fields.Many2one('medical.physician', 'Dentist', tracking=True)
    dentist_ids = fields.Many2many('medical.physician')

    def report_doctor(self):
        return self.env.ref(
            'pragtech_dental_management.id_doctor_report_xlxx').report_action(self)


class GeneralLedgerAccount(models.AbstractModel):
    _name = 'report.pragtech_dental_management.report_customer'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, doctors):
        for rec in doctors:
            domain = [('state', '=', 'completed'),
                      ('completion_date', '>=', rec.start_date),
                      ('completion_date', '<=', rec.end_date)]
            treatments = self.env['medical.teeth.treatment'].search(domain)
            dentists = list(set(treatments.mapped('dentist')))
            print('dentistsdentists', dentists)
            for dentist in dentists:
                sheet = workbook.add_worksheet(dentist.name)
                format0 = workbook.add_format({'font_size': 15, 'border': True, 'align': 'center'})
                format1 = workbook.add_format({'font_size': 15, 'align': 'center'})
                format3 = workbook.add_format(
                    {'align': 'center', 'bold': True, 'bg_color': '#4CE400', 'color': 'black', 'border': 5})
                sheet.set_column('A:A', 35)
                sheet.set_column('B:B', 15)
                sheet.set_column('C:C', 30)
                sheet.set_column('D:D', 15)
                sheet.set_column('E:E', 25)
                row = 1
                sheet.merge_range(0, 0, 0, 4, 'Report Doctor', format3)
                sheet.write(row + 1, 0, 'FROM : ' + str(rec.start_date), format1)
                sheet.write(row + 1, 4, 'TO : ' + str(rec.end_date), format1)
                row += 3
                sheet.write(row, 0, 'Patient', format3)
                sheet.write(row, 1, 'Patient ID', format3)
                sheet.write(row, 2, 'Description', format3)
                sheet.write(row, 3, 'Net Amount', format3)
                sheet.write(row, 4, 'Completion Date', format3)
                print("dentist", dentist.name)
                doctor_lines = self.env['medical.teeth.treatment'].sudo().search(
                    [('dentist', '=', dentist.id), ('id', 'in', treatments.ids)])
                print('doctor_lines', doctor_lines)
                total_net_amount = 0
                for line in doctor_lines:
                    row += 1
                    sheet.write(row, 0, line.patient_id.partner_id.name, format0)
                    sheet.write(row, 1, line.patient_id.patient_id, format0)
                    sheet.write(row, 2, line.description.name, format0)
                    sheet.write(row, 3, round(line.net_amount, 2), format0)
                    sheet.write(row, 4, str(line.completion_date), format0)
                    total_net_amount += line.net_amount
                row += 1
                sheet.write(row, 0, 'Total', format3)
                sheet.write(row, 1, '', format3)
                sheet.write(row, 2, '', format3)
                sheet.write(row, 3, round(total_net_amount, 2), format3)
                sheet.write(row, 4, '', format3)
