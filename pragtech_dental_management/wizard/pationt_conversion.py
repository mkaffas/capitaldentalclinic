from odoo import api, fields, models,_


class pationt_conversion(models.TransientModel):
    _name = 'pationt.conversion.wizard'

    start_date = fields.Date(string="", required=False, )
    end_date = fields.Date(string="", required=False, )

    def open(self):
        for rec in self:
            patients=self.env['medical.patient'].sudo().search([('first_dignoses_date', '>=', rec.start_date), ('first_dignoses_date', '<=', rec.end_date),
                           ('first_dignoses_date', '!=', False)])
            print("patientspatients",patients)
            return {
                'type': 'ir.actions.act_window',
                'views': [[False, "tree"],[False, "form"]],
                # 'view_type': 'tree',
                # 'view_mode': 'tree',
                # 'view_id': False,
                'res_model': 'medical.patient',
                'domain': [('id', 'in', patients.ids)],

            }
            # return {
            #     'name': _('MedicalPatient'),
            #     'view_type': 'tree',
            #     'view_mode': 'tree',
            #     'res_model': 'medical.patient',
            #     'view_id': False,
            #     'type': 'ir.actions.act_window',
            #     'domain': [('first_dignoses_date', '>=', rec.start_date),('first_dignoses_date', '<=', rec.end_date),('first_dignoses_date', '!=', False)],
            # }
