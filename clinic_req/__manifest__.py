# -*- coding: utf-8 -*-
{
    'name': 'Clinic Req',
    'version': '1.1',
    'category': 'web',
    "description": """
        Clinic Req
    """,
    'depends': [
        'base',
        'crm',
        'pragtech_dental_management',
        'survey',
        'mail',
        'date_range'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/crm.xml',
        'views/discount.xml',
        'views/inherit_remake.xml',
        'views/wizzard_label.xml',
    ],
    'images': ['static/description/banner.png'],
    'qweb': [
        'static/src/xml/*.xml',
    ],
    'application': False,
    'installable': True,
    'license': 'LGPL-3',
}
