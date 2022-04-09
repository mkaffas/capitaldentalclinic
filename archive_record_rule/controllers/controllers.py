# -*- coding: utf-8 -*-
# from odoo import http


# class ArchiveRecordRule(http.Controller):
#     @http.route('/archive_record_rule/archive_record_rule/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/archive_record_rule/archive_record_rule/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('archive_record_rule.listing', {
#             'root': '/archive_record_rule/archive_record_rule',
#             'objects': http.request.env['archive_record_rule.archive_record_rule'].search([]),
#         })

#     @http.route('/archive_record_rule/archive_record_rule/objects/<model("archive_record_rule.archive_record_rule"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('archive_record_rule.object', {
#             'object': obj
#         })
