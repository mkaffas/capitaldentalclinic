# -*- coding: utf-8 -*-

import time
from odoo import api, models, _
from odoo.tools import float_is_zero
from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError

class ReportIncomeByInsurance(models.AbstractModel):

    _name = 'report.pragtech_dental_management.income_by_insurance'

    def get_income_insurance_company(self,start_date, end_date, insurance_company):
        # history_ids = self.env['account.move'].search([('date_invoice', '>=', start_date),('date_invoice', '<=', end_date),('state','in',['open','draft'])])
        history_ids=self.env['account.move'].search([('invoice_date','>=',start_date),('invoice_date','<=',end_date),('state','in',['draft','posted'])])

        prod_dict = {}
        for income in history_ids:
            if insurance_company:
                if income.insurance_company.id == insurance_company[0]:
#                     if prod_dict.has_key(income.insurance_company.id):
                    if income.insurance_company.id in prod_dict:
                        prod_dict[income.insurance_company.id][1] += 1
                        prod_dict[income.insurance_company.id][2] += income.amount_total
                    else:
                        prod_dict[income.insurance_company.id] = [income.insurance_company.name, 1, income.amount_total]
            else:
                if income.insurance_company:
#                     if prod_dict.has_key(income.insurance_company.id):
                    if income.insurance_company.id in prod_dict:
                        prod_dict[income.insurance_company.id][1] += 1
                        prod_dict[income.insurance_company.id][2] +=income.amount_total 
                    else:
                        prod_dict[income.insurance_company.id] = [income.insurance_company.name, 1, income.amount_total]
    
        return [prod_dict]

#     @api.model
#     def render_html(self, docids, data=None):
#         self.model = self.env.context.get('active_model')
#         docs = self.env[self.model].browse(self.env.context.get('active_ids', []))
#         start_date = data['form']['date_start']
#         end_date = data['form']['date_end']
#         insurance_company = data['form']['insurance_company']
#         final_records = self.get_income_insurance_company(start_date, end_date, insurance_company)
# 
#         docargs = {
#             'doc_ids': self.ids,
#             'doc_model': self.model,
#             'data': data['form'],
#             'docs': docs,
#             'time': time,
#             'get_income_insurance_company': final_records,
#         }
#         return self.env['report'].render('pragtech_dental_management.income_by_insurance', docargs)


    def _get_report_values(self, docids, data=None):
        if not data.get('form') or not self.env.context.get('active_model') or not self.env.context.get('active_id'):
            raise UserError(_("Form content is missing, this report cannot be printed."))
        model = self.env.context.get('active_model')
        docs = self.env[model].browse(self.env.context.get('active_id'))
        start_date = data['form']['date_start']
        end_date = data['form']['date_end']
        insurance_company = data['form']['insurance_company']
        if isinstance(insurance_company, tuple):
            insurance_company=insurance_company[0]
        final_records = self.get_income_insurance_company(start_date, end_date, insurance_company)
        return {
            'doc_ids': self.ids,
            'doc_model': 'income.by.insurance.company.wizard',
            'data': data['form'],
            'docs': docs,
            'time': time,
            'get_income_insurance_company': final_records,
        }
    
    def formatLang(self, value, digits=None, date=False, date_time=False, grouping=True, monetary=False, dp=False, currency_obj=False, lang=False):
        if lang:
            self.env.context['lang'] = lang
        return super(ReportIncomeByInsurance, self).formatLang(value, digits=digits, date=date, date_time=date_time, grouping=grouping, monetary=monetary, dp=dp, currency_obj=currency_obj)

