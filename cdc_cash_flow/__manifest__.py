# -*- coding: utf-8 -*-
{
    'name': "cash flow",

    'description': """
        Invoices Report
    """,

    'author': "Initium Solutions",
    'website': "https://www.initium-me.com",

    'category': 'Accounting/Accounting',
    'version': '0.1',

    'depends': ['base', 'account', 'report_xlsx'],

    'data': [
        'security/ir.model.access.csv',
        'report/report_invoice.xml',
        'wizard/report_invoice.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}
