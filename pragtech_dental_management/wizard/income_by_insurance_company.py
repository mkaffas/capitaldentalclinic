from odoo import models,fields,api


class IncomeByInsuranceCompanyWizard(models.TransientModel):
    _name = 'income.by.insurance.company.wizard'
    _description = "Invoice By Insurance Company Wizard"

    _description ='Income By Procedure Wizard'
    date_start = fields.Date('From Date',required = True)
    date_end = fields.Date('To Date',required = True)
    insurance_company = fields.Many2one('res.partner', 'Insurance Company')
    
     
#     @api.multi
#     def print_report(self):
#         data = {}
#         data['form'] = self.read(['date_start', 'date_end', 'insurance_company'])[0]
#         value = self.env['report'].get_action(self, 'pragtech_dental_management.income_by_insurance', data)
#         return value
    
    def print_report(self):
        datas = {'active_ids': self.env.context.get('active_ids', []),'form':self.read(['date_start', 'date_end','insurance_company'])[0]}
        values=self.env.ref('pragtech_dental_management.income_by_insurance_company_qweb').report_action(self, data=datas)
        return values