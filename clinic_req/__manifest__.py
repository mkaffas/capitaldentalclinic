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
        'pragtech_dental_management'
    ],
    'data': [
        'views/crm.xml',
        # 'security/ir.model.access.csv',
    ],
    'images': ['static/description/banner.png'],
    'qweb': [
        'static/src/xml/*.xml',
    ],
    'application': False,
    'installable': True,
    'license': 'LGPL-3',
}