# -*- coding: utf-8 -*-
{
    'name': 'Partner',
    'version': '1.1',
    'category': 'web',
    "description": """
        Clinic Req
    """,
    'depends': [
        'base',
    ],
    'data': [
        'views/partner.xml',
    ],
    'images': ['static/description/banner.png'],
    'qweb': [
        'static/src/xml/*.xml',
    ],
    'application': False,
    'installable': True,
    'license': 'LGPL-3',
}
