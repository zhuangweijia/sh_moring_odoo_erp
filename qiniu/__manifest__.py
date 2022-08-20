# -*- coding: utf-8 -*-

{
    'name': 'OSS',
    'author': 'Musk',
    'website': '',
    'category': 'application',
    'version': '1.0',

    'summary': """
    """,
    'description': """
    """,
    'depends': ['base','mail'],
    'data': [
        'security/ir.model.access.csv',
        'views/pic_upload_qiniu.xml',
        'views/menu.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
