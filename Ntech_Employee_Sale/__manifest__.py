# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Add employee in SO & INV',
    'version': '15.0',
    'category': 'Account',
    'description': """Add employee in SO & INV""",
    'depends': ['account','sale'],
    'data': ['views/employee_sale_views.xml'],
    'installable': True,
    'auto_install': False,
    'application': True,
}
