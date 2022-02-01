# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Restrict Duplicate Sale Order',
    'version': '13.0',
    'category': 'Sale',
    'description': """Restrict Duplicate Sale Order""",
    'depends': ['sale','stock','account'],
    'data': ['views/sale_duplicate_views.xml'],
    'installable': True,
    'auto_install': False,
    'application': True,
}
