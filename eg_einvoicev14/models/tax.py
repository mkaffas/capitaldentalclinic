# -*- coding: utf-8 -*-

from odoo import models, fields, api


class TaxType(models.Model):
    _name = 'tax.types'
    _rec_name = 'desc_ar'
    code = fields.Char(string="Code", required=False)
    desc_en = fields.Char(string="English Description", required=False)
    desc_ar = fields.Char(string="Arabic Description", required=False)


class SubTaxType(models.Model):
    _name = 'tax.sub.types'
    _rec_name = 'desc_ar'
    code = fields.Char(string="Code", required=False)
    desc_en = fields.Char(string="English Description", required=False)
    desc_ar = fields.Char(string="Arabic Description", required=False)
    tax_type_code = fields.Char(string="Tax Type Code", required=False)


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'
    tax_type_id = fields.Many2one(comodel_name="tax.types", string="Tax Type", required=False)
    sub_tax_type_id = fields.Many2one(comodel_name="tax.sub.types", string="Sub Tax Type", required=False)
    unit_type_id = fields.Many2one(comodel_name="uom.types", string="Unit Type", related='product_uom_id.unit_type_id',
                                   store=True)
    lot_id = fields.Many2one("stock.production.lot", "Lot",)
    product_tax_amount = fields.Float(string="", required=False,  readonly=False)

    # @api.onchange('product_id','product_tax_amount')
    # def _onchange_product_id_tax(self):
    #     for line in self:
    #         if line.product_id and line.product_tax_amount:
    #             line.product_id.write({'tax_amount':line.product_tax_amount})

    @api.onchange('sale_line_ids')
    def calc_lot_id(self):
        for rec in self:
            if rec.sale_line_ids:
                rec.lot_id = rec.sale_line_ids[0].lot_id.id
            else:
                rec.lot_id = False

    def _get_taxableItems(self, taxes_res):
        """
        Compute taxable lines
        :param taxes_res:
        :return: taxableItems
        """
        tax_obj = self.env['account.tax']
        taxableItems = []
        EGP = self.env.ref('base.EGP')
        if taxes_res:
            for tax_line in taxes_res:
                tax = tax_obj.browse(tax_line['id'])
                amount = abs(tax_line['amount'])
                if self.currency_id:
                    # TODO: NEEDED to be changed
                    amount = self.currency_id.compute(amount, EGP)
                taxType = tax.tax_type_id.code
                subType = tax.sub_tax_type_id.code
                if tax.tax_type_id.code == 'T1':
                    rate = 14
                else:
                    rate = 0
                taxableItems.append({
                    "taxType": taxType,
                    "amount": round(amount, 5),
                    "subType": subType,
                    "rate": round(rate, 5)
                })
        else:
            taxableItems = [{"taxType": "T1",
                             "amount": 0.00,
                             "subType": "V008",
                             "rate": 0.00}]
        return taxableItems

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


class AccountTax(models.Model):
    _inherit = 'account.tax'

    tax_type_id = fields.Many2one(comodel_name="tax.types", string="Tax Type", required=False)
    sub_tax_type_id = fields.Many2one(comodel_name="tax.sub.types", string="Sub Tax Type", required=False)

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
