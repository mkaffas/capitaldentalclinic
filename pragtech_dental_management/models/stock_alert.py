# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools, _
#from mock import DEFAULT
from datetime import datetime
from dateutil.relativedelta import relativedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from odoo.exceptions import UserError, RedirectWarning, ValidationError
import smtplib
import time

class ResUsers(models.Model):
    _inherit='res.users'
    _description = "Res Users"
    
    negative_alert = fields.Boolean('Expiry Alert')


class PurchaseReportScheduler(models.Model):
    _name='purchase.report.scheduler'
    _description = "Purchase report Scheduler"
    
#################    Negative Stock Alert   ####################### 

#     def negative_stock(self,cr,uid,context=None):
#          
#         msg1 = MIMEMultipart('alternative')
#         msg1['Subject'] = "Expiry Alert"
#         users_ids=self.pool.get('res.users').search(cr,uid,[('negative_alert','=',True)])
#         html=self.extract_products1(cr,uid,context=context)
#         if html:
#             for user_id in users_ids:
#                 each_user=self.pool.get('res.users').browse(cr,uid,user_id,context=context)
#                 receivers=each_user.partner_id.email
#                 try:
#                     user_data = self.pool.get('ir.mail_server').browse(cr,uid,1)
#                     username = user_data.smtp_user
#                     password = user_data.smtp_pass
#                     host = user_data.smtp_host
#                     smtpObj = smtplib.SMTP(host=host, port=587)
#                     smtpObj.ehlo()
#                     smtpObj.starttls()
#                     smtpObj.ehlo()
#                     smtpObj.login(user=username, password=password)
#                       
#                     part2 = MIMEText(html, 'html')
#                     msg1.attach(part2)
#                     smtpObj.sendmail(username, receivers, msg1.as_string())  
#                 except:
#                     raise osv.except_osv(_("Error"), _("Error in sending mail!!"))
#         return True
    @api.model
    def _negative_stock(self):
        self.negative_stock()


    @api.model
    def negative_stock(self):
          
        msg1 = MIMEMultipart('alternative')
        msg1['Subject'] = "Expiry Alert"
        users_ids=self.env['res.users'].search([('negative_alert','=',True)])
        html=self.extract_products1()
        if html:
            for user_id in users_ids:
                receivers=user_id.partner_id.email
                try:
                    user_data = self.env['ir.mail_server'].browse(1)
                    username = user_data.smtp_user
                    password = user_data.smtp_pass
                    host = user_data.smtp_host
                    smtpObj = smtplib.SMTP(host=host, port=587)
                    smtpObj.ehlo()
                    smtpObj.starttls()
                    smtpObj.ehlo()
                    smtpObj.login(user=username, password=password)
                       
                    part2 = MIMEText(html, 'html')
                    msg1.attach(part2)
                    smtpObj.sendmail(username, receivers, msg1.as_string())  
                except:
                    raise UserError(_('Error in sending mail!!'))
        return True
    
#      
#     def extract_products1(self,cr,uid,context=None):
#         current_time = time.strftime('%Y-%m-%d')
#         production_ids = self.pool.get('stock.production.lot').search(cr,uid,[])
#         record = []
#         for lot in self.pool.get('stock.production.lot').browse(cr,uid,production_ids):
#             if lot.alert_date[0:10] == current_time:
#                 record.append(lot)
#         tab = ''
#         if record:
#             tab +="<html><body></br><table><tr><th align=left>Product Name</th><th width=40></th><th align=center>Serial Number</th><th width=30></th><th class=text-center>Expiry Date</th></tr>"
#             for each_record in record:-#                 tab=tab+ "<tr><td align=left>"+each_record.product_id.name+"</td><td width=20></td><td align=left>"+each_record.name+"</td><td width=30></td><td align=right>"+ str(each_record.life_date)+"</tr>"
#             tab=tab+"</table></body></html>"  
#         return tab

    def extract_products1(self):
        current_time = time.strftime('%Y-%m-%d')
        production_ids = self.env['stock.production.lot'].search([])
        record = []
        for lot in production_ids:
            if lot.alert_date == current_time:
                record.append(lot)
        tab = ''
        if record:
            tab +="<html><body></br><table><tr><th align=left>Product Name</th><th width=40></th><th align=center>Serial Number</th><th width=30></th><th class=text-center>Expiry Date</th></tr>"
            for each_record in record:
                tab=tab+ "<tr><td align=left>"+each_record.product_id.name+"</td><td width=20></td><td align=left>"+each_record.name+"</td><td width=30></td><td align=right>"+ str(each_record.life_date)+"</tr>"
            tab=tab+"</table></body></html>"  
        return tab
         
