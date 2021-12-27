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

    transfer_id = fields.Many2one(comodel_name="stock.picking", string="", required=False, )
    qty = fields.Float(string="QTY",  required=False, )
    # _inherit = 'mail.thread'

    def action_transfer(self):
        stock_ids = self.env['stock.warehouse.orderpoint'].browse(self._context.get('active_ids', False))
        lines = []
        for line in stock_ids:
            lines.append(line.id)
        return {'type': 'ir.actions.act_window',
                'name': _('Transfer'),
                'res_model': 'warehouse.orderpoint.wizard',
                'target': 'new',
                'view_id': self.env.ref('warehouse_location_access_app.warehouse_orderpoint_wizard_form').id,
                'view_mode': 'form',
                'context': {'default_stock_ids': [(6, 0, lines)] }
                }

    def send_products(self):
        stock_ids = self.env['stock.warehouse.orderpoint'].browse(self._context.get('active_ids', False))
        list_products = ""
        for line in stock_ids:
            list_products += line.product_id.name + " \n "
        body = 'All this products need to Replenishment ' + list_products
        partners = [x.partner_id.id for x in self.env.ref(
            'stock.group_stock_manager').users]

        if partners:
            self.env['product.product'].sudo().search([], limit=1).sudo().message_post(
                partner_ids=partners,
                subject="Products to Replenishment",
                body=body,
                message_type='comment',
                subtype_id=self.env.ref('mail.mt_note').id, )


class Warehouse(models.TransientModel):
    _name = 'warehouse.orderpoint.wizard'

    src_location_id = fields.Many2one(comodel_name="stock.location", string="Location", required=True, )
    stock_ids = fields.Many2many(comodel_name="stock.warehouse.orderpoint",string="", )

    def create_transfer(self):
        list_products = []
        location_id = False
        for line in self.stock_ids:
            vals = {}
            vals['name'] = 'Order Point Transfer'
            vals['product_id'] = line.product_id.id
            vals['product_uom'] = line.product_id.uom_id.id
            location_id = line.location_id
            vals['product_uom_qty'] = line.qty
            list_products.append((0, 0, vals))
        if list_products:
            obj = self.env['stock.picking']
            obj_picking = self.env['stock.picking.type'].sudo().search(
                [('default_location_src_id', '=', self.src_location_id.id), ('code', '=', 'internal')], limit=1)
            obj.sudo().create({
                'picking_type_id': obj_picking.id,
                'location_id': self.src_location_id.id,
                'location_dest_id': location_id.id,
                'move_ids_without_package': list_products
            })
            for record in self.stock_ids:
                record.transfer_id = obj.id
            return {'type': 'ir.actions.act_window',
                    'name': _('Transfer'),
                    'res_model': 'stock.picking',
                    'target': 'current',
                    'view_id': self.env.ref('stock.vpicktree').id,
                    'view_mode': 'form',
                    'res_id': obj.id,
                    'domain' : [('id','=',obj.id)]
                    }
