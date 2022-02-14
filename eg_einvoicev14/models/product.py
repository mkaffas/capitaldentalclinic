# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProductTemplate(models.Model):
    _inherit = 'product.template'
    item_code = fields.Char(string="Item Code", required=False, company_dependent=True)
    item_type = fields.Char(string="Item Type", required=False, company_dependent=True)
    tax_type_id = fields.Many2one(comodel_name="tax.types", string="Tax Type", required=False, company_dependent=True)
    sub_tax_type_id = fields.Many2one(comodel_name="tax.sub.types", string="Sub Tax Type", required=False,
                                      company_dependent=True)
    is_tax = fields.Boolean(string="Product Tax",)

    @api.onchange('tax_type_id')
    def onchange_gender(self):
        if self.tax_type_id:
            return {
                'domain': {'sub_tax_type_id': [('tax_type_code', '=', self.tax_type_id.code)]}
            }

        else:
            return {
                'domain': {'sub_tax_type_id': []}
            }


class ProductProduct(models.Model):
    _inherit = 'product.product'

    tax_amount = fields.Float(string="Taxes", required=False, )
