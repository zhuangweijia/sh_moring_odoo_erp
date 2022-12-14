# -*- coding: utf-8 -*-
{
    'name': "designer_management",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'BSH_ERP/BSH_ERP',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','mail','resource','web'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/designer_info.xml',
        'views/designer_project.xml',
        'views/designer_options.xml',
        'views/designer_ability_tag.xml',
        'views/menu.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo/demo.xml',
    ],
    'application': True,
}
