# -*- coding: utf-8 -*-

import time
from odoo import api, models, _
from odoo.tools import float_is_zero
from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError


class ReportIncomeByDoctor(models.AbstractModel):

    _name = 'report.pragtech_dental_management.report_income_by_doctor'
    _description = "Invoice Reporting"

    def fetch_record(self, start_date, end_date):
        invoice_ids=self.env['account.move'].search([('invoice_date','>=',start_date),('invoice_date','<=',end_date),('dentist','!=',False),('state','in',['draft','posted']),('move_type','=','out_invoice')])
        res=[]
        for each_record in invoice_ids:
            if not res:
                res.append({'dentist_id':each_record.dentist.id,'dentist_name':each_record.dentist.name,'customer_count':1,'total_amount':each_record.amount_total})
            else:
                flag=0
                for each_res in res:
                    if each_record.dentist.id ==each_res['dentist_id']:
                        each_res['customer_count']+=1
                        each_res['total_amount']+=each_record.amount_total
                        flag=1
                        break
                if flag==0:
                    res.append({'dentist_id':each_record.dentist.id,'dentist_name':each_record.dentist.name,'customer_count':1,'total_amount':each_record.amount_total})
                     
        return res

#     @api.model
#     def render_html(self, docids, data=None):
#         self.model = self.env.context.get('active_model')
#         docs = self.env[self.model].browse(self.env.context.get('active_ids', []))
#         start_date = data['form']['start_date']
#         end_date = data['form']['end_date']
#         final_records = self.fetch_record(start_date, end_date)
# 
#         docargs = {
#             'doc_ids': self.ids,
#             'doc_model': self.model,
#             'data': data['form'],
#             'docs': docs,
#             'time': time,
#             'get_income_by_dentist_info': final_records,
#         }
#         return self.env['report'].render('pragtech_dental_management.report_income_by_doctor', docargs)
    
    
    
    def _get_report_values(self, docids, data=None):
        if not data.get('form') or not self.env.context.get('active_model') or not self.env.context.get('active_id'):
            raise UserError(_("Form content is missing, this report cannot be printed."))
        model = self.env.context.get('active_model')
        docs = self.env[model].browse(self.env.context.get('active_id'))
        start_date = data['form']['start_date']
        end_date = data['form']['end_date']
        final_records = self.fetch_record(start_date, end_date)
        return {
            'doc_ids': self.ids,
            'doc_model': 'income.by.doctor.report.wizard',
            'data': data['form'],
            'docs': docs,
            'time': time,
            'get_income_by_dentist_info': final_records,
        }
    
    def formatLang(self, value, digits=None, date=False, date_time=False, grouping=True, monetary=False, dp=False, currency_obj=False, lang=False):
        if lang:
            self.env.context['lang'] = lang
        return super(ReportIncomeByDoctor, self).formatLang(value, digits=digits, date=date, date_time=date_time, grouping=grouping, monetary=monetary, dp=dp, currency_obj=currency_obj)

    
    
class ReportPatientByDoctor(models.AbstractModel):

    _name = 'report.pragtech_dental_management.report_patient_by_doctor'
    _description = "Patient By doctor Report"
    
    def fetch_record(self, start_date, end_date):
        # invoice_ids=self.env['account.move'].search([('date_invoice','>=',start_date),('date_invoice','<=',end_date),('dentist','!=',False),('state','in',['open','paid']),('type','=','out_invoice')])
        invoice_ids=self.env['account.move'].search([('invoice_date','>=',start_date),('invoice_date','<=',end_date),('dentist','!=',False),('state','in',['draft','posted']),('move_type','=','out_invoice')])

        res=[]
        for each_record in invoice_ids:
            if not res:
                res.append({'dentist_id':each_record.dentist.id,'dentist_name':each_record.dentist.name,'customer_count':1})
            else: 
                flag=0  
                for each_res in res:
                    if each_record.dentist.id ==each_res['dentist_id']:
                        each_res['customer_count']+=1
                        flag=1
                        break
                if flag==0:
                    res.append({'dentist_id':each_record.dentist.id,'dentist_name':each_record.dentist.name,'customer_count':1})
        return res
    
#     @api.model
#     def render_html(self, docids, data=None):
#         self.model = self.env.context.get('active_model')
#         docs = self.env[self.model].browse(self.env.context.get('active_ids', []))
#         start_date = data['form']['start_date']
#         end_date = data['form']['end_date']
#         final_records = self.fetch_record(start_date, end_date)
#     
#         docargs = {
#             'doc_ids': self.ids,
#             'doc_model': self.model,
#             'data': data['form'],
#             'docs': docs,
#             'time': time,
#             'get_income_by_dentist_info': final_records,
#         }
#         return self.env['report'].render('pragtech_dental_management.report_patient_by_doctor', docargs)
    
    def _get_report_values(self, docids, data=None):

        if not data.get('form') or not self.env.context.get('active_model') or not self.env.context.get('active_id'):
            raise UserError(_("Form content is missing, this report cannot be printed."))
        model = self.env.context.get('active_model')
        docs = self.env[model].browse(self.env.context.get('active_id'))
        start_date = data['form']['start_date']
        end_date = data['form']['end_date']
        final_records = self.fetch_record(start_date, end_date)
        return {
            'doc_ids': self.ids,
            'doc_model': 'patient.by.doctor.report.wizard',
            'data': data['form'],
            'docs': docs,
            'time': time,
            'get_income_by_dentist_info': final_records,
        }
    
    def formatLang(self, value, digits=None, date=False, date_time=False, grouping=True, monetary=False, dp=False, currency_obj=False, lang=False):
        if lang:
            self.env.context['lang'] = lang
        return super(ReportIncomeByDoctor, self).formatLang(value, digits=digits, date=date, date_time=date_time, grouping=grouping, monetary=monetary, dp=dp, currency_obj=currency_obj)
