# -*- coding: utf-8 -*-
{
    'name': "eg_einvoicev14",

    'summary': """ Egyptian e-Invoicing """,

    'description': """
        Egyptian e-Invoicing
    """,

    'author': "TC Company",
    'website': "https://sdk.invoicing.eta.gov.eg",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'accounting',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','sale','account','product','uom','sale_order_lot_selection'],

    # always loaded
    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',
        'data/uom.types.csv',
        'data/tax.types.csv',
        'data/tax.sub.types.csv',
        'wizards/elect_inv_reason.xml',
        'views/elect_reaons.xml',
        'views/company.xml',
        'views/partner.xml',
        'views/product.xml',
        'views/units.xml',
        # 'views/res_config_settings.xml',
        'views/invoice.xml',

    ],

}
