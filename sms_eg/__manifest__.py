# -*- coding: utf-8 -*-
{
    'name': "SMS EG",
    'summary': """Send SMS to clients""",
    'author': "ProjoMania",
    'website': "http://www.ProjoMania.com",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['base', 'base_setup'],
    'data': [
        'security/ir.model.access.csv',
        'data/ir_sequence.xml',
        'views/sms_eg.xml',
        'views/sms_eg_template.xml',
        'views/res_config_settings.xml',
    ],
}
