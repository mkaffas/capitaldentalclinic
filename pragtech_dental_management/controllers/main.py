# -*- coding: utf-8 -*-
import json
import logging
import werkzeug.utils

from odoo import http
from odoo.http import request

class DentalSiteController(http.Controller):

    @http.route(['/dental_management_perio_chart/web/<string:patient_id>'], type='http', auth='user')
    def a(self, debug=False, **k):
        patient_id = k['patient_id']
#         if not request.session.uid:
#             return http.local_redirect('/web/login?redirect=/hotel_room_dashboard/web')
 
#         return request.render('dental_management.dental_perio_chart')
        return request.render('dental_management.dental_perio_chart', {'patient_id':patient_id})
     
    @http.route(['/dental_management_chart/web/<string:ids>'], type='http', auth='user')
    def b(self, debug=False, **k):
        val_list = []
        val_list = k['ids'].split('_')
         
        patient_id = val_list[0]
        appt_id = ''
        if len(val_list) > 1:
            appt_id = val_list[1]
#         if not request.session.uid:
#             return http.local_redirect('/web/login?redirect=/hotel_room_dashboard/web')
        return request.render('dental_management.dental_chart', {'patient_id':patient_id,'appt_id':appt_id})

    
