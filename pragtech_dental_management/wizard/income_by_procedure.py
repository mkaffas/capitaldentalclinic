from odoo import models,fields,api


class IncomeByProcedure_wizard(models.TransientModel):
    _name = 'income.by.procedure.wizard'
    _description ='Income By Procedure Wizard'
    
    date_start = fields.Date('From Date',required = True)
    date_end = fields.Date('To Date',required = True)
     
        
    def print_report(self):
        datas = {'active_ids': self.env.context.get('active_ids', []),'form':self.read(['date_start', 'date_end'])[0]}
        values=self.env.ref('pragtech_dental_management.income_by_procedure_qweb').report_action(self, data=datas)
        return values
    
    