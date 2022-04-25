# -*- coding: utf-8 -*-
import base64
import io
from odoo import models


class ReportXlsx(models.AbstractModel):
    _name = 'report.cdc_cash_flow.template_report_invoice_xlsx'
    _inherit = 'report.report_xlsx.abstract'
    _description = 'Report Xlsx'

    def write_tags(self,tags,row,sheet,format_white,rec):
        cr = self._cr
        for tag in tags:
            total_tag = 0
            row += 1
            sheet.write(row, 1, tag.name, format_white)
            accounts = self.env['account.account'].sudo().search([('tage_id', '=', tag.id)])
            for account in accounts:
                row += 1
                sheet.write(row, 2, account.display_name, format_white)

                cr.execute("""  
                                        SELECT debit,credit FROM account_move_line
                                        WHERE account_id = %s
                                              and CAST(date AS date) >= %s
                                              and CAST(date AS date) <= %s  """,
                           (account.id, rec.date_from, rec.date_to))
                data = [x for x in cr.fetchall()]
                debit = sum([x[0] for x in data])
                credit = sum([x[-1] for x in data])
                sheet.write(row, 3, str(round(credit - debit, 2)), format_white)
                total_tag += round(debit - credit, 2)
        return row,total_tag,tag

    def generate_xlsx_report(self, workbook, data, records):

        sheet = workbook.add_worksheet('Invoices Report')
        format_customer = workbook.add_format(
            {'font_size': 15, 'border': True, 'align': 'center', 'bg_color': '#333f4f', 'color': '#ffffff', })
        format_invoice = workbook.add_format(
            {'font_size': 15, 'border': True, 'align': 'center', 'bg_color': '#8496b0', 'color': 'black', })
        format_white = workbook.add_format({'font_size': 15, 'align': 'center'})
        sheet.set_column('A:A', 20)
        sheet.set_column('B:B', 20)
        sheet.set_column('C:C', 20)
        sheet.set_column('D:D', 25)
        sheet.set_column('E:E', 20)
        sheet.set_column('F:F', 27)
        sheet.set_column('G:G', 20)
        sheet.set_column('H:H', 10)
        sheet.set_column('I:I', 0.5)
        sheet.set_column('J:J', 15)
        sheet.set_column('K:K', 15)
        for rec in records:
            sheet.write(0, 0, 'FROM : ' + str(rec.date_from), format_white)
            sheet.write(0, 2, 'TO : ' + str(rec.date_to), format_white)
            sheet.write(1, 0, 'CDC CASh FLOW', format_white)

            tags = set(self.env['account.tage'].sudo().search([('type', '=', 'in')]))
            row = 3
            sheet.write(row, 1, 'CASh IN', format_customer)
            row,total_tag,tag=self.write_tags(tags,row,sheet,format_white,rec)
            row += 1
            sheet.write(row, 1, 'Total ' + str(tag.name), format_invoice)
            sheet.write(row, 3, str(total_tag), format_invoice)
            row+=1

            tags = set(self.env['account.tage'].sudo().search([('type', '=', 'out')]))
            sheet.write(row, 1, 'CASh OUT', format_customer)
            row, total_tag, tag = self.write_tags(tags, row, sheet, format_white, rec)
            row += 1
            sheet.write(row, 1, 'Total ' + str(tag.name), format_invoice)
            sheet.write(row, 3, str(total_tag), format_invoice)
