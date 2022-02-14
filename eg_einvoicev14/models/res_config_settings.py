from odoo import models, fields, api, _
from datetime import datetime

class resConfigSettingsInherits(models.TransientModel):
    _inherit = 'res.config.settings'

    clientId = fields.Text(string='Client Id')
    clientSecret = fields.Text(string='Client Secret')
    configType = fields.Selection([('UAT', 'EEI-UAT Env'), ('PRD', 'EEI-PRD Env'), ('SIT', 'EEI-SIT Env')],string='Electronic Invoice Platform')
    invoiceVersion = fields.Selection([('0.9', '0.9'), ('1.0', '1.0')],string='Electronic Invoice Version',default='0.9',)



    @api.model
    def get_values(self):
        res = super(resConfigSettingsInherits, self).get_values()
        params = self.env['ir.config_parameter'].sudo()
        clientId = params.get_param('clientId', default=False)
        clientSecret = params.get_param('clientSecret', default=False)
        configType = params.get_param('configType', default=False)
        invoiceVersion = params.get_param('invoiceVersion', default=False)

        res.update(
            clientId=clientId,
            clientSecret=clientSecret,
            configType=configType,
            invoiceVersion = invoiceVersion
        )
        return res

    def set_values(self):
        super(resConfigSettingsInherits, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param("clientId", self.clientId)
        self.env['ir.config_parameter'].sudo().set_param("clientSecret", self.clientSecret)
        self.env['ir.config_parameter'].sudo().set_param("configType", self.configType)
        self.env['ir.config_parameter'].sudo().set_param("invoiceVersion", self.invoiceVersion)

