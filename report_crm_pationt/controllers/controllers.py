# -*- coding: utf-8 -*-
# from odoo import http


# class ReportCrmPationt(http.Controller):
#     @http.route('/report_crm_pationt/report_crm_pationt/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/report_crm_pationt/report_crm_pationt/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('report_crm_pationt.listing', {
#             'root': '/report_crm_pationt/report_crm_pationt',
#             'objects': http.request.env['report_crm_pationt.report_crm_pationt'].search([]),
#         })

#     @http.route('/report_crm_pationt/report_crm_pationt/objects/<model("report_crm_pationt.report_crm_pationt"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('report_crm_pationt.object', {
#             'object': obj
#         })
