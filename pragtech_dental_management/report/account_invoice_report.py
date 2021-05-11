# -*- coding: utf-8 -*-

from odoo import tools
from odoo import models, fields, api


class AccountInvoiceReport(models.Model):
    _inherit = "account.invoice.report"
    _description = "Invoices Statistics"

    dentist = fields.Many2one('medical.physician', 'Dentist')
    insurance_company = fields.Many2one('res.partner', 'Insurance Company',
                                        domain=[('is_insurance_company', '=', True)])

    @property
    def _table_query(self):
        return '%s %s %s' % (self._select(), self._from(), self._where())

    @api.model
    def _select(self):
        return '''
                SELECT
                    line.id,
                    line.move_id,
                    line.product_id,
                    line.account_id,
                    line.analytic_account_id,
                    line.journal_id,
                    line.company_id,
                    line.company_currency_id,
                    line.partner_id AS commercial_partner_id,
                    move.state,
                    move.move_type,
                    move.partner_id,
                    move.invoice_user_id,
                    move.fiscal_position_id,
                    move.payment_state,
                    move.invoice_date,
                    move.invoice_date_due,
                    uom_template.id                                             AS product_uom_id,
                    template.categ_id                                           AS product_categ_id,
                    line.quantity / NULLIF(COALESCE(uom_line.factor, 1) / COALESCE(uom_template.factor, 1), 0.0) * (CASE WHEN move.move_type IN ('in_invoice','out_refund','in_receipt') THEN -1 ELSE 1 END)
                                                                                AS quantity,
                    -line.balance * currency_table.rate                         AS price_subtotal,
                    -line.balance / NULLIF(COALESCE(uom_line.factor, 1) / COALESCE(uom_template.factor, 1), 0.0) * currency_table.rate
                                                                                AS price_average,
                    COALESCE(partner.country_id, commercial_partner.country_id) AS country_id
            '''

    @api.model
    def _from(self):
        return '''
                FROM account_move_line line
                    LEFT JOIN res_partner partner ON partner.id = line.partner_id
                    LEFT JOIN product_product product ON product.id = line.product_id
                    LEFT JOIN account_account account ON account.id = line.account_id
                    LEFT JOIN account_account_type user_type ON user_type.id = account.user_type_id
                    LEFT JOIN product_template template ON template.id = product.product_tmpl_id
                    LEFT JOIN uom_uom uom_line ON uom_line.id = line.product_uom_id
                    LEFT JOIN uom_uom uom_template ON uom_template.id = template.uom_id
                    INNER JOIN account_move move ON move.id = line.move_id
                    LEFT JOIN res_partner commercial_partner ON commercial_partner.id = move.commercial_partner_id
                    JOIN {currency_table} ON currency_table.company_id = line.company_id
            '''.format(
            currency_table=self.env['res.currency']._get_query_currency_table({'multi_company': True, 'date': {'date_to': fields.Date.today()}}),
        )

    @api.model
    def _where(self):
        return '''
                WHERE move.move_type IN ('out_invoice', 'out_refund', 'in_invoice', 'in_refund', 'out_receipt', 'in_receipt')
                    AND line.account_id IS NOT NULL
                    AND NOT line.exclude_from_invoice_tab
            '''

    # def _select(self):
    #     select_str = """
    #         SELECT sub.id, sub.date, sub.product_id, sub.partner_id, sub.country_id, sub.analytic_account_id,
    #             sub.invoice_payment_term_id, sub.uom_name, sub.currency_id, sub.journal_id,
    #             sub.fiscal_position_id, sub.invoice_user_id, sub.company_id, sub.nbr, sub.type, sub.state,
    #             sub.weight, sub.volume,
    #             sub.categ_id, sub.invoice_date_due, sub.invoice_partner_bank_id,
    #             sub.product_qty, sub.price_subtotal as price_subtotal, sub.price_average as price_average,
    #             COALESCE(cr.rate, 1) as currency_rate, sub.residual as residual, sub.commercial_partner_id as commercial_partner_id, sub.dentist as dentist,  sub.insurance_company as insurance_company
    #     """
    #     return select_str

    # def _sub_select(self):
    #     select_str = """
    #             SELECT ail.id AS id,
    #                 ai.date AS date,
    #                 ail.product_id, ai.partner_id, ai.invoice_payment_term_id, ail.analytic_account_id,
    #                 u2.name AS uom_name,
    #                 ai.currency_id, ai.journal_id, ai.fiscal_position_id, ai.invoice_user_id, ai.company_id,
    #                 1 AS nbr,
    #                 ai.type, ai.state, pt.categ_id, ai.invoice_date_due,  ail.account_id AS account_line_id,
    #                 ai.invoice_partner_bank_id,ai.dentist as dentist,  ai.insurance_company as insurance_company,
    #                 SUM ((invoice_type.sign * ail.quantity) / (u.factor * u2.factor)) AS product_qty,
    #                 SUM(ail.price_subtotal) AS price_subtotal,
    #                 SUM(ABS(ail.price_subtotal)) / CASE
    #                         WHEN SUM(ail.quantity / u.factor * u2.factor) <> 0::numeric
    #                            THEN SUM(ail.quantity / u.factor * u2.factor)
    #                            ELSE 1::numeric
    #                         END AS price_average,
    #                 (SELECT count(*) FROM account_move_line l where move_id = ai.id) *
    #                 count(*) * invoice_type.sign AS residual,
    #                 ai.commercial_partner_id as commercial_partner_id,
    #                 partner.country_id,
    #                 SUM(pr.weight * (invoice_type.sign*ail.quantity) / u.factor * u2.factor) AS weight,
    #                 SUM(pr.volume * (invoice_type.sign*ail.quantity) / u.factor * u2.factor) AS volume
    #     """
    #     return select_str

    # def _from(self):
    #     from_str = """
    #             FROM account_move_line ail
    #             JOIN account_move ai ON ai.id = ail.move_id
    #             JOIN res_partner partner ON ai.commercial_partner_id = partner.id
    #             LEFT JOIN product_product pr ON pr.id = ail.product_id
    #             left JOIN product_template pt ON pt.id = pr.product_tmpl_id
    #             LEFT JOIN uom_uom u ON u.id = ail.product_uom_id
    #             LEFT JOIN uom_uom u2 ON u2.id = pt.uom_id
    #             JOIN (
    #                 -- Temporary table to decide if the qty should be added or retrieved (Invoice vs Refund)
    #                 SELECT id,(CASE
    #                      WHEN ai.type::text = ANY (ARRAY['out_refund'::character varying::text, 'in_invoice'::character varying::text])
    #                         THEN -1
    #                         ELSE 1
    #                     END) AS sign
    #                 FROM account_move ai
    #             ) AS invoice_type ON invoice_type.id = ai.id
    #     """
    #     return from_str
    # @api.model
    # def _from(self):
    #     return '''
    #             FROM account_move_line line
    #                 LEFT JOIN res_partner partner ON partner.id = line.partner_id
    #                 LEFT JOIN product_product product ON product.id = line.product_id
    #                 LEFT JOIN account_account account ON account.id = line.account_id
    #                 LEFT JOIN account_account_type user_type ON user_type.id = account.user_type_id
    #                 LEFT JOIN product_template template ON template.id = product.product_tmpl_id
    #                 LEFT JOIN uom_uom uom_line ON uom_line.id = line.product_uom_id
    #                 LEFT JOIN uom_uom uom_template ON uom_template.id = template.uom_id
    #                 INNER JOIN account_move move ON move.id = line.move_id
    #                 LEFT JOIN res_partner commercial_partner ON commercial_partner.id = move.commercial_partner_id
    #                 JOIN {currency_table} ON currency_table.company_id = line.company_id
    #         '''.format(
    #         currency_table=self.env['res.currency']._get_query_currency_table({'multi_company': True, 'date': {'date_to': fields.Date.today()}}),
    #     )

    # def _group_by(self):
    #     group_by_str = """
    #             GROUP BY ail.id, ail.product_id, ail.analytic_account_id, ai.date, ai.id,
    #                 ai.partner_id, ai.invoice_payment_term_id, u2.name, u2.id, ai.currency_id, ai.journal_id,
    #                 ai.fiscal_position_id, ai.invoice_user_id, ai.company_id, ai.type, invoice_type.sign, ai.state, pt.categ_id,
    #                 ai.invoice_date_due, ail.account_id, ai.invoice_partner_bank_id,
    #                 ai.commercial_partner_id, partner.country_id, ai.dentist, ai.insurance_company
    #     """
    #     return group_by_str

    # @api.model_cr
    # def init(self):
    #     # self._table = account_invoice_report
    #     tools.drop_view_if_exists(self.env.cr, self._table)
    #     self.env.cr.execute("""CREATE or REPLACE VIEW %s as (
    #         WITH currency_rate AS (%s)
    #         %s
    #         FROM (
    #             %s %s %s
    #         ) AS sub
    #         LEFT JOIN currency_rate cr ON
    #             (cr.currency_id = sub.currency_id AND
    #              cr.company_id = sub.company_id AND
    #              cr.date_start <= COALESCE(sub.date, NOW()) AND
    #              (cr.date_end IS NULL OR cr.date_end > COALESCE(sub.date, NOW())))
    #     )""" % (
    #         self._table, self.env['res.currency']._select_companies_rates(),
    #         self._select(), self._sub_select(), self._from(), self._group_by()))
