# -*- encoding: utf-8 -*-
{
    'name': 'Odoo Dental Clinic Management',
    'version': '14.0.4',
    'author': 'Pragmatic TechSoft Pvt Ltd.',
    'category': 'Generic Modules/Others',
    'depends': ['base', 'website', 'sale_management', 'purchase', 'account', 'product', 'account',
                'attachment_indexation', 'google_calendar', 'product_expiry', 'web'],
    'summary': 'This Module Adds a drop-down for service links in systray Bookmarks odoo bookmarks Odoo - Dental Clinic Management app dental management system dental management module dental management odoo dental dental clinic management dental app',
    'description': """
This modules includes Dental Clinic Management Features
<keywords>
Odoo - Dental Clinic Management
dental
dental management app
dental management system
dental management module
dental management 
odoo dental
dental clinic management
dental app
""",
    'website': 'http://pragtech.co.in',
    "data": [
        'security/dental_security.xml',
        'security/ir.model.access.csv',
        'views/my_layout.xml',
        'data/dental_data.xml',
        'data/dose_units.xml',
        'data/medicament_form.xml',
        'data/snomed_frequencies.xml',
        'data/occupations.xml',
        'data/teeth_code.xml',
        'views/dental_view.xml',
        'wizard/wizard_actions.xml',
        'views/dental_sequences.xml',
        'report/income_by_procedure_qweb.xml',
        'report/patient_by_procedure_qweb.xml',
        'report/claim_report_qweb.xml',
        'report/claim_report_temp.xml',
        'report/income_by_insurance_company_qweb.xml',
        'views/dental_report.xml',
        'views/report_appointment.xml',
        'views/report_prescription.xml',
        'views/report_prescription_main.xml',
        'views/templates.xml',
        'views/report_patient_financing_agreement.xml',
        'views/report_income_by_procedure.xml',
        'views/report_patient_by_procedure.xml',
        'views/report_income_by_insurance_company.xml',
        'report/report_claim_form.xml',
        'report/report_daman_reimbursement.xml',
        'report/report_oman_reinburstment.xml',
        'report/report_nextcare_reimbursement.xml',
        'views/stock_alert.xml',
        'views/alert_data.xml',
        'views/financing_view.xml',
        'views/dental_invoice_view.xml',
        'report/account_invoice_report_view.xml',
        'report/report_income_by_doctor.xml',
        'report/report_patient_by_doctor.xml',
    ],
    'qweb': ['static/src/xml/perio_base.xml'],
    'images': ['images/Animated-dental-management.gif'],
    'live_test_url': 'http://www.pragtech.co.in/company/proposal-form.html?id=103&name=Odoo-Dental-Management',
    'license': 'OPL-1',
    'price': 999,
    'currency': 'EUR',
    'installable': True,
    'application': True,
    'auto_install': False,
}
