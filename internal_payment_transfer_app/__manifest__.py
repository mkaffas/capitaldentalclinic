# -*- coding: utf-8 -*-
{
    'name': 'Payment Transfer With Account/Journal Option',
    "author": "Edge Technologies",
    'version': '14.0.1.2',
    'live_test_url': "https://youtu.be/4_9w_0UIW3o",
    "images":['static/description/main_screenshot.png'],
    'summary': "Payment Journal to Account transfer payment Account to Journal transfer internal account transfer internal transfer payment  Account Payment Voucher payment account transfer payment account to account to transfer account cash transfer bank account transfer",
    'description': """ This app helps user to transfer payment internally with many options like account to account, journal to account, and account to journal. 

Payment Management For Internal Transfer
Journal to Account transfer
Account to Journal transfer
manage Payment
internal transfer
internal transfer payment 
managing internal transfer payment
Account Payment Voucher
Generate Payment
account transfer
payment account transfer
account to account to transfer 
Payment Management voucher
account Internal Transfer Request
account type Internal Transfer Request
Internal Transfer Request
account type
account payment type
payment account type
Account Types Menu
voucher account types
odoo Account Types Menu
account payment internal transfer option
account cash transfer bank account transfer bank account payment transfer cash account payment transfer
account payment with journal transfer option transfer from account to account transfer from journal to journal transfer 
odoo automatic payment transfer option from journal


    """,
    "license" : "OPL-1",
    'depends': ['base','sale_management','account','purchase','stock_account'],
    'data': [
            'views/inherit_payment.xml',
            ],
    'installable': True,
    'auto_install': False,
    'price': 18,
    'currency': "EUR",
    'category': 'Accounting',

}

