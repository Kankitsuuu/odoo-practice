# -*- coding: utf-8 -*-
{
    'name': "Hospital Management",
    'version': '16.0.1.0.0',
    'summary': """
        Module for hospital automation""",
    'license': 'AGPL-3',
    'author': "Artiushenko Yaroslav",
    'maintainer': 'Artiushenko Yaroslav, '
                  'https://github.com/Kankitsuuu,'
                  'artyushenko01@gmail.com',
    'website': "https://github.com/Kankitsuuu/odoo-practice/tree/16.0-MODULE-2",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Administration',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/hospital_menus.xml',
        'views/hospital_doctor_views.xml',
        'views/hospital_patient_views.xml',
        'views/hospital_visit_views.xml',
        'views/hospital_disease_views.xml',
        'data/hospital_disease_data.xml',
    ],

    # only loaded in demonstration mode
    'demo': [
        'demo/hospital_doctor_demo.xml',
        'demo/hospital_patient_demo.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
