""" Initialize Models """

import requests

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class SmsEg(models.Model):
    """
        Initialize Sms Eg:
    """
    _name = 'sms.eg'
    _description = 'SMS Eg'

    state = fields.Selection(
        [('draft', 'Draft'),
         ('sent', 'Sent'),
         ('error', 'Error')],
        string="Status",
        default='draft'
    )
    name = fields.Char(
        default="New",
        readonly=True
    )
    message = fields.Text(
        translate=True
    )
    partner_ids = fields.Many2many(
        "res.partner",
        string="Customers",
        domain="[('mobile', '!=', False)]"
    )
    sms_eg_template_id = fields.Many2one(
        "sms.eg.template",
        string="SMS Template"
    )

    @api.onchange('sms_eg_template_id')
    def _onchange_sms_eg_template_id(self):
        """ sms_eg_template_id """
        self.message = self.sms_eg_template_id.message

    def send_sms_eg(self):
        for rec in self:
            username = self.env.company.eg_username
            password = self.env.company.eg_password
            sender = self.env.company.eg_sender
            if not all([username, password, sender]):
                raise ValidationError(_('Missing SMS Configuration'))
            for partner in rec.partner_ids:
                message = rec.with_context(lang=partner.lang).message
                response = requests.request(
                    "GET",
                    f"https://smssmartegypt.com/sms/api/?"
                    f"username={username}&"
                    f"password={password}"
                    f"&sendername={sender}&"
                    f"mobiles={partner.mobile}&"
                    f"message={message}",
                    headers={'content-type': 'application/json',
                             'accept': 'application/json',
                             'accept-language': 'en-US'})
                if response.json().get('type') == 'success':
                    rec.state = 'sent'
                    self.name = self.env['ir.sequence'].next_by_code(
                        'sms.eg.sequence')
                else:
                    rec.state = 'error'
