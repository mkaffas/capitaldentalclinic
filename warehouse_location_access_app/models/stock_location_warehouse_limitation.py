# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class ResUsers(models.Model):
    _inherit = 'res.users'

    available_location_ids = fields.Many2many('stock.location', 'res_user_location_default_rel', 'user_id',
                                              'location_id', string='Allowed Locations')

    def write(self, vals):
        if 'available_location_ids' in vals:
            self.env['ir.model.access'].call_cache_clearing_methods()
            self.env['ir.rule'].clear_caches()
            self.has_group.clear_cache(self)
        return super(ResUsers, self).write(vals)


class Orderpoint(models.Model):
    _inherit = 'stock.warehouse.orderpoint'

    def send_products(self):
        stock_ids = self.env['stock.warehouse.orderpoint'].browse(self._context.get('active_ids', False))
        list_products = ""
        for line in stock_ids:
            list_products += line.product_id.name + " \n "
        partners = self.env.ref(
            'stock.group_stock_manager').users.filtered(
            lambda r: r.partner_id).mapped('partner_id.id')
        obj = self.env['res.partner'].sudo().search([('id','=',partners)])
        body = 'All this products need to Replenishment' + list_products
        if partners:
            self.env['mail.message'].sudo().create({'message_type': "notification",
                                             "subtype_id": self.env.ref("mail.mt_comment").id,
                                             'body': body,
                                             'subject':"Products to Replenishment",
                                             'partner_ids': [(4, obj.ids)],
                                             'model': self._name,
                                             'res_id': self.id,
                                             })
            # obj.sudo().message_post(
            #     partner_ids=all_partners,
            #     subject="Products to Replenishment ",
            #     body=body,
            #     message_type='comment',
            #     subtype_id=self.env.ref('mail.mt_note').id)
