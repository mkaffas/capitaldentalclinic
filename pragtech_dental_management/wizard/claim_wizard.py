from odoo import models, fields, api
import base64
import datetime


class ClaimWizard(models.TransientModel):
    _name = 'dental.claim.wizard'
    _description = "Dental Claim wizard"
    
    to_date = fields.Date(string='To Date')
    from_date = fields.Date(string='From Date')

    def print_report(self):
        datas = {'active_ids': self.env.context.get('active_ids', []),
                 'form':self.read(['to_date', 'from_date'])[0],
                 }
        values=self.env.ref('pragtech_dental_management.claim_report_qweb').report_action(self, data=datas)
        return values
    
    def generate_backlog_excel_report(self):
        import sys
        import xlsxwriter
        # Create an new Excel file and add a worksheet.
#         workbook = xlsxwriter.Workbook('/opt/odoo/backlog_demo.xlsx')
        workbook = xlsxwriter.Workbook('/home/pragmatic/Downloads/%s.xlsx'%self.from_date)
        worksheet = workbook.add_worksheet()
        # Add a font format to use to highlight cells.
        bold = workbook.add_format({'size': 10})
        normal = workbook.add_format({'size': 10})
        r = 0
        c = 0
        data_list = []
        output_header = ['Patient Name','MEM ID','Date of Birth','Nationality','Country of Residence','Sex','Mobile','Invoice Number','Healthcare Professional','Healthcare Professional ID','Healthcare Professional Type','Episode Number','Dentist','Appointment Start','Appointment End','Treatment','Treatment Code']
        for item in output_header:
            worksheet.write(r, c, item, bold)
            c += 1
#         picking_type_ids = self.env['stock.picking.type'].search(['|', ('name', 'ilike', 'Delivery order'), ('name', 'ilike', 'dropship')])
#
#             
#         picking_ids = self.env['stock.picking'].search([('state', '!=', 'done'),('state', '!=', 'cancel'), ('picking_type_id', 'in', picking_type_ids.ids)])
#
#         for picking in picking_ids: #[:5]:
#             for line in picking.move_lines_related:
#                 line_list = []
#                 
#                 line_list.append(picking.name)
#                 
#     #             appending name
#                 if picking.sale_id.partner_id :
#                     line_list.append(picking.sale_id.partner_id.name)
#                 else:
#                     line_list.append('')
#                
#     #            if a sale order is associated with the picking 
#                 if picking.sale_id :
#                     line_list.append(picking.sale_id.name)
#                     if picking.sale_id.client_order_ref:
#                         line_list.append(picking.sale_id.client_order_ref)
#                     else:
#                         line_list.append('')
# #                     line_list.append(picking.sale_id.date_order)
#                     
#                     t_date= datetime.datetime.strptime(picking.sale_id.date_order, "%Y-%m-%d %H:%M:%S").strftime('%d-%m-%Y')
#                     line_list.append(t_date)
#                 
#                 else :
#                     line_list.append('')
#                     line_list.append('')
#                     line_list.append('')
#                     
#                 if picking.purchase_id:
#                     line_list.append(picking.purchase_id.name)
#                     line_list.append(picking.purchase_id.partner_id.name)
# #                     line_list.append(picking.purchase_id.date_order)
#                     t_date= datetime.datetime.strptime(picking.purchase_id.date_order, "%Y-%m-%d %H:%M:%S").strftime('%d-%m-%Y')
#                     line_list.append(t_date)
#                     
#                 else:
#                     line_list.append('')
#                     line_list.append('')
#                     line_list.append('')
#                     
#                 line_list.append(line.product_id.default_code)
# #                 line_list.append(line.product_id.default_code)
#                 
# #                 if picking is attached to a PO / code for product decription
#                 if picking.purchase_id:
#                     flag = False
# #                     if refrence to purchase order line exists
#                     if line.purchase_line_id:
#                         flag = True
#                         line_list.append(line.purchase_line_id.name)
# #                         else iterate through all lines in the po
#                     else : 
#                         for po_line in picking.purchase_id:
#                             if po_line.product_id.id == line.product_id.id:
#                                 flag = True
#                                 line_list.append(po_line.name)
#                         if flag == False:
#                             line_list.append('')
# #                 if no PO fetch price from SO
#                 elif picking.sale_id :
#                     flag = False
#                     for so_line in picking.sale_id.order_line:
#                         if so_line.product_id.id == line.product_id.id:
#                             flag = True
#                             line_list.append(so_line.name)
#                     if flag == False:
#                             line_list.append('')
#                 else:
#                     line_list.append('')
#                     
#                 line_list.append(line.product_uom_qty)
#  
#                  
# #                 if picking is attached to a PO / code for unit price
#                 if picking.purchase_id:
# #                     if refrence to purchase roder line exists
#                     if line.purchase_line_id:
#                         line_list.append(line.purchase_line_id.price_unit)
# #                         else iterate through all lines in the po
#                     else : 
#                         for po_line in picking.purchase_id:
#                             if po_line.product_id.id == line.product_id.id:
#                                 line_list.append(po_line.price_unit)
# #                 if no PO fetch price from SO
#                 elif picking.sale_id :
#                     for so_line in picking.sale_id.order_line:
#                         if so_line.product_id.id == line.product_id.id:
#                             line_list.append(so_line.price_unit)
#                 else:
#                     line_list.append(line.product_id.lst_price)
#                    
#                 data_list.append(line_list)        
#                     
        inv_data = self.env['account.move'].search \
            ([('date_invoice', '>=', self.from_date),('date_invoice', '<=', self.to_date),('patient','!=',False)])
        for inv in inv_data:
            data = []
            data.append(inv.patient.name.name)
            if inv.patient.name.ref:
                data.append(inv.patient.name.ref)
            else:
                data.append('')
            if inv.patient.dob:
                data.append(inv.patient.dob)
            else:
                data.append('')
            if inv.patient.nationality_id:
                data.append(inv.patient.nationality_id.name)
            else:
                data.append('')
            if inv.patient.name.country_id:
                data.append(inv.patient.name.country_id.name)
            else:
                data.append('')
            if inv.patient.sex:
                if inv.patient.sex == 'm':
                    data.append('Male')
                else:
                    data.append('Female')
            else:
                data.append('')
            if inv.patient.mobile:
                data.append(inv.patient.mobile)
            else:
                data.append('')
            if inv.number:
                data.append(inv.number)
            else:
                data.append('')
            if inv.dentist:
                data.append(inv.dentist.name.name)
            else:
                data.append('')
            if inv.dentist.code:
                data.append(inv.dentist.code)
            else:
                data.append('')
            if inv.dentist.speciality:
                data.append(inv.dentist.speciality.name)
            else:
                data.append('')
            if inv.patient.apt_id:
                apt_line = []
                dentist_line = []
                app_start = []
                app_end = []
                for apt in inv.patient.apt_id:
                    if apt:
                        apt_line.append(apt.name)
                        if apt.doctor:
                            dentist_line.append(apt.doctor.name.name)
                        else:
                            dentist_line.append('')
                        if apt.appointment_sdate:
                            app_start.append(apt.appointment_sdate)
                        else:
                            app_start.append('')
                        if apt.appointment_edate:
                            app_end.append(apt.appointment_edate)
                        else:
                            app_end.append('')
                    else:
                        apt_line.append('')
                data.append('1402')#apt_line)
                data.append('Arshad')#dentist_line)
                data.append('06/06/2018')#app_start)
                data.append('06/06/2018')#app_end)
            else:
                data.append('')
                data.append('')
                data.append('')
                data.append('')
            if inv.invoice_line_ids:
                product =[]
                p_code =[]
                for line in inv.invoice_line_ids:
                    product.append(line.product_id.name)
                    if line.product_id.default_code:
                        p_code.append(line.product_id.default_code)
                    else:
                        p_code.append('')
                data.append('Product1')#product)
                data.append('P00000112')#p_code)
            else:
                data.append('')
                data.append('')
            
            data_list.append(data)
            
#         data_list = [['1','2'],['1','GFHC'],['22','adygb']]  
        r += 1
        for data in data_list:
            c = 0
            for item in data:
                worksheet.write(r, c, item, normal)
                c += 1
            r += 1
            
            
        workbook.close()
#         data = base64.b64encode(open('/tmp/%s.xlsx'%self.from_date,'rb').read())
