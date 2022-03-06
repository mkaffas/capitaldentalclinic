# -*- coding: utf-8 -*-
# from odoo import http


# class RegisterPaymentDraft(http.Controller):
#     @http.route('/register_payment_draft/register_payment_draft/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/register_payment_draft/register_payment_draft/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('register_payment_draft.listing', {
#             'root': '/register_payment_draft/register_payment_draft',
#             'objects': http.request.env['register_payment_draft.register_payment_draft'].search([]),
#         })

#     @http.route('/register_payment_draft/register_payment_draft/objects/<model("register_payment_draft.register_payment_draft"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('register_payment_draft.object', {
#             'object': obj
#         })
