# -*- coding: utf-8 -*-

import time
from odoo import api, models, _
from odoo.tools import float_is_zero
from datetime import datetime
from odoo.exceptions import UserError
from dateutil.relativedelta import relativedelta


class ReportPatientByProcedure(models.AbstractModel):

    _name = 'report.pragtech_dental_management.report_patient_by_procedure'
    _description = "Patient By Procedure Report"
    
    def get_patient_procedure(self, start_date, end_date):
        # history_ids = self.env['account.move'].search([('date_invoice', '>=', start_date),('date_invoice', '<=', end_date),('state','in',['open','draft'])])
        history_ids=self.env['account.move'].search([('invoice_date','>=',start_date),('invoice_date','<=',end_date),('dentist','!=',False),('state','in',['draft','posted']),('move_type','=','out_invoice')])

        prod_dict = {}
        for income in history_ids:
            if income:
                for line in income.invoice_line_ids:
                    if line.product_id.is_treatment:
                        if line.product_id.id in prod_dict:
                            prod_dict[line.product_id.id][1] += 1
                        else:
                            prod_dict[line.product_id.id] = [line.product_id.name, 1] 
        return [prod_dict]
        

#     @api.model
#     def render_html(self, docids, data=None):
#         self.model = self.env.context.get('active_model')
#         docs = self.env[self.model].browse(self.env.context.get('active_ids', []))
#         start_date = data['form']['date_start']
#         end_date = data['form']['date_end']
#         final_records = self.get_patient_procedure(start_date, end_date)
# 
#         docargs = {
#             'doc_ids': self.ids,
#             'doc_model': self.model,
#             'data': data['form'],
#             'docs': docs,
#             'time': time,
#             'get_patient_procedure': final_records,
#         }
#         return self.env['report'].render('pragtech_dental_management.report_patient_by_procedure', docargs)

    def fetch_record(self, start_date, end_date):
        invoice_ids=self.env['account.move'].search([('invoice_date','>=',start_date),('invoice_date','<=',end_date),
                                                     ('dentist','!=',False),('state','in',['draft','posted']),('move_type','=','out_invoice')])

        res = []
        for each_record in invoice_ids:
            if not res:
                res.append({'dentist_id': each_record.dentist.id, 'dentist_name': each_record.dentist.name,
                            'customer_count': 1, 'total_amount': each_record.amount_total})
            else:
                flag = 0
                for each_res in res:
                    if each_record.dentist.id == each_res['dentist_id']:
                        each_res['customer_count'] += 1
                        each_res['total_amount'] += each_record.amount_total
                        flag = 1
                        break
                if flag == 0:
                    res.append({'dentist_id': each_record.dentist.id, 'dentist_name': each_record.dentist.name.name,
                                'customer_count': 1, 'total_amount': each_record.amount_total})

        return res
    
    def _get_report_values(self, docids, data=None):
        if not data.get('form') or not self.env.context.get('active_model') or not self.env.context.get('active_id'):
            raise UserError(_("Form content is missing, this report cannot be printed."))
        model = self.env.context.get('active_model')
        docs = self.env[model].browse(self.env.context.get('active_id'))
        # start_date = str(data['form']['start_date'])[:10]
        start_date = data['form']['date_start']
        s_date = str(start_date)[:10]
        # end_date = str(data['form']['end_date'])[:10]
        end_date = data['form']['date_end']
        e_date = str(end_date)[:10]

        final_records = self.get_patient_procedure(s_date, e_date)
        return {
            'doc_ids': self.ids,
            'doc_model': 'patient.by.procedure.wizard',
            'data': data['form'],
            'docs': docs,
            'time': time,
            'get_patient_procedure': final_records,
        }
    
    def formatLang(self, value, digits=None, date=False, date_time=False, grouping=True, monetary=False, dp=False, currency_obj=False, lang=False):
        if lang:
            self.env.context['lang'] = lang
        return super(ReportPatientByProcedure, self).formatLang(value, digits=digits, date=date, date_time=date_time, grouping=grouping, monetary=monetary, dp=dp, currency_obj=currency_obj)
