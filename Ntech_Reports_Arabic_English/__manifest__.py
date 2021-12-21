{
    'name': 'Print Reports in Arabic & English',
    'version': '1.0',
    'category': 'Invoice',
    'description': """
This Module will get Print Reports of Invoice in Arabic & English
    """,
    'author': 'khadeer',
    'website': 'https://www.nutechits.com/',
    'depends': ['account'],
    'data': [
        'account_invoice_arabic_english.xml',
        'views/report_invoice_arabic_english.xml',
        ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
