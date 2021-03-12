# -*- coding: utf-8 -*-

import time
from odoo import api, models, _
from odoo.tools import float_is_zero
from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError

class ReportIncomeByProcedure(models.AbstractModel):

    _name = 'report.pragtech_dental_management.report_income_by_procedure'
    _description = "Invoice By Procedure Report"
    
    def get_income_procedure(self, start_date, end_date):
        history_ids=self.env['account.move'].search([('invoice_date','>=',start_date),('invoice_date','<=',end_date),('state','in',['draft','posted'])])


        prod_dict = {}
        for income in history_ids:
            if income:
                for line in income.invoice_line_ids:
                    if line.product_id.is_treatment:
                        if line.product_id.id in prod_dict:
#                         if prod_dict.has_key(line.product_id.id):
                            prod_dict[line.product_id.id][1] += 1
                            prod_dict[line.product_id.id][2] += line.price_unit
                        else:
                            prod_dict[line.product_id.id] = [line.product_id.name, 1, line.price_unit] 
        return [prod_dict]

    # @api.multi
    # def _get_report_values(self, docids, data=None):

#     @api.model
#     def render_html(self, docids, data=None):
#         self.model = self.env.context.get('active_model')
#         docs = self.env[self.model].browse(self.env.context.get('active_ids', []))
#         start_date = data['form']['date_start']
#         end_date = data['form']['date_end']
#         final_records = self.get_income_procedure(start_date, end_date)
# 
#         docargs = {
#             'doc_ids': self.ids,
#             'doc_model': self.model,
#             'data': data['form'],
#             'docs': docs,
#             'time': time,
#             'get_income_procedure': final_records,
#         }
#         return self.env['report'].render('pragtech_dental_management.income_by_procedure_qweb', docargs)
    
    
    def _get_report_values(self, docids, data=None):
        if not data.get('form') or not self.env.context.get('active_model') or not self.env.context.get('active_id'):
            raise UserError(_("Form content is missing, this report cannot be printed."))
        model = self.env.context.get('active_model')
        docs = self.env[model].browse(self.env.context.get('active_id'))
        start_date = data['form']['date_start']
        end_date = data['form']['date_end']
        final_records = self.get_income_procedure(start_date, end_date)
        return {
            'doc_ids': self.ids,
            'doc_model': 'income.by.procedure.wizard',
            'data': data['form'],
            'docs': docs,
            'time': time,
            'get_income_procedure': final_records,
        }
    
    
    def formatLang(self, value, digits=None, date=False, date_time=False, grouping=True, monetary=False, dp=False, currency_obj=False, lang=False):
        if lang:
            self.env.context['lang'] = lang
        return super(ReportIncomeByProcedure, self).formatLang(value, digits=digits, date=date, date_time=date_time, grouping=grouping, monetary=monetary, dp=dp, currency_obj=currency_obj)
