# -*- coding: utf-8 -*-
{
    'name': "check_management",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "IBS - khaled habib",
    'website': "http://www.ibs-odoo.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/11.0/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'account'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/payment_check.xml',
        'views/journal.xml',
        'views/transient.xml',
        'views/partial_transient.xml',
        'views/payment_check_line.xml',
        'views/payment_check_line_line.xml',
        'views/move_menus.xml',
        'views/check_history.xml',


    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}