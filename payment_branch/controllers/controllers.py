# -*- coding: utf-8 -*-
# from odoo import http


# class PaymentBtanch(http.Controller):
#     @http.route('/payment_branch/payment_branch/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/payment_branch/payment_branch/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('payment_branch.listing', {
#             'root': '/payment_branch/payment_branch',
#             'objects': http.request.env['payment_branch.payment_branch'].search([]),
#         })

#     @http.route('/payment_branch/payment_branch/objects/<model("payment_branch.payment_branch"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('payment_branch.object', {
#             'object': obj
#         })
