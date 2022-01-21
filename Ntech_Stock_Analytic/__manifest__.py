# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Added Analytic Account in Warehouse Operations',
    'version': '15.0',
    'category': 'Stock',
    'description': """Added Analytic Account in Warehouse Operations""",
    'depends': ['stock','account','purchase','sale','sale_stock','stock_account'],
    'data': ['views/stock_analytic_views.xml'],
    'installable': True,
    'auto_install': False,
    'application': True,
}
