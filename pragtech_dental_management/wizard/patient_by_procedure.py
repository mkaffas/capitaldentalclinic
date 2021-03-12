from odoo import models,fields,api


class patient_by_procedure_wizard(models.TransientModel):
    _name = 'patient.by.procedure.wizard'

    _description ='Patient By Procedure Wizard'
    date_start = fields.Date('From Date',required = True)
    date_end = fields.Date('To Date',required = True)
     
#     @api.multi
#     def print_report(self):
#         data = {} 
#         data['form'] = self.read(['date_start', 'date_end'])[0]
#         value = self.env['report'].get_action(self, 'pragtech_dental_management.report_patient_by_procedure', data)
#         return value
    
    def print_report(self):
        datas = {'active_ids': self.env.context.get('active_ids', []),'form':self.read(['date_start', 'date_end'])[0]}
        values=self.env.ref('pragtech_dental_management.patient_by_procedure_qweb').report_action(self, data=datas)
        return values