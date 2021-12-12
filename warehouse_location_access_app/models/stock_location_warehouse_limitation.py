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
    # _inherit = 'mail.thread'

    def send_products(self):
        stock_ids = self.env['stock.warehouse.orderpoint'].browse(self._context.get('active_ids', False))
        list_products = ""
        for line in stock_ids:
            list_products += line.product_id.name + " \n "
        body = 'All this products need to Replenishment ' + list_products
        partners = [x.partner_id.id for x in self.env.ref(
            'stock.group_stock_manager').users]

        if partners:
            self.env['product.product'].sudo().search([],limit=1).sudo().message_post(
                partner_ids=partners,
                subject="Products to Replenishment",
                body= body,
                message_type='comment',
                subtype_id=self.env.ref('mail.mt_note').id, )
        # if partners:
            # notification_ids = []
            # for partner in obj:
            #     notification_ids.append((0, 0, {
            #         'res_partner_id': partner.id,
            #         'notification_type': 'inbox'}))
            # partner.message_post(body=body, message_type='notification',
            #                   subtype_id=self.env.ref('mail.mt_comment').id, author_id=self.env.user.partner_id.id,
            #                   notification_ids=notification_ids)

            # self.env['mail.message'].create({
            #     'email_from': self.env.user.partner_id.email,
            #     'author_id': self.env.user.partner_id.id,
            #     'model': 'mail.channel',
            #     'message_type': 'comment',
            #     'subject': "Products to Replenishment",
            #     'subtype_id': self.env.ref('mail.mt_comment').id,
            #     'body': body,
            #     'channel_ids': [(4, self.env.ref('mail.channel_all_employees').id)],
            #     'res_id': self.env.ref('mail.channel_all_employees').id,  # here add the channel you created.
            # })
            # self.env['mail.message'].sudo().create({'message_type': "notification",
            #                                  "subtype_id": self.env.ref("mail.mt_comment").id,
            #                                  'body': body,
            #                                  'subject':"Products to Replenishment",
            #                                  'partner_ids': [(6,0, obj.ids)],
            #                                  # 'model': self._name,
            #                                  # 'res_id': self.id,
            #                                  })
            # obj.sudo().message_post(
            #     partner_ids=all_partners,
            #     subject="Products to Replenishment ",
            #     body=body,
            #     message_type='comment',
            #     subtype_id=self.env.ref('mail.mt_note').id)
