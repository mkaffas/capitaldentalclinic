# -*- coding: utf-8 -*-
{
	'name' : 'Warehouse Stock location Access for Users',
	'author': "Edge Technologies",
	'version' : '14.0.1.1',
	'live_test_url':'https://youtu.be/RlGhjeGL1io',
	"images":['static/description/main_screenshot.png'],
	'summary' :'Stock access rules warehouse access rules stock location access for users warehouse access control warehouse limited access for users stock limited access for users stock location access control Stock Location limitation access Warehouse Limitation access',
	'description' : """
		Stock Locations Warehouse Limitations App """,
	'depends' : ['base','stock'],
	"license" : "OPL-1",
	'data' : [
		'security/stock_location_warehouse_limitation_security.xml',
		'views/stock_location_warehouse_limitation.xml',
		
	],
	'qweb' : [],
	'demo' : [],
	'installable' : True,
	'auto_install' : False,
	'price': 14,
	'category' : 'Warehouse',
	'currency': "EUR",
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
