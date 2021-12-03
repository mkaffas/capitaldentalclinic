# -*- coding: utf-8 -*-
from odoo import http

# class CheckManagement(http.Controller):
#     @http.route('/check_management/check_management/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/check_management/check_management/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('check_management.listing', {
#             'root': '/check_management/check_management',
#             'objects': http.request.env['check_management.check_management'].search([]),
#         })

#     @http.route('/check_management/check_management/objects/<model("check_management.check_management"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('check_management.object', {
#             'object': obj
#         })