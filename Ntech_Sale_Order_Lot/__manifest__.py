# See LICENSE file for full copyright and licensing details
{
    'name': 'Sale Order Lot Number',
    'version': '15.0',
    'category': 'Sale',
    'summary': """
        Sale Order Lot Number
     """,
    'author': 'Me',
    'depends': ['product_expiry', 'sale'],
    'data': [
        "views/sale_order_lot_views.xml",
    ],
    'auto_install': False,
    'installable': True,
    'application': True,
}
