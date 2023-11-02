{
    'name': "Hospital Management",
    'version': '16.0.0.0.1',
    'summary': """
        Module for hospital automation""",
    'license': 'AGPL-3',
    'author': "Artiushenko Yaroslav",
    'maintainer': 'Artiushenko Yaroslav, '
                  'https://github.com/Kankitsuuu,'
                  'artyushenko01@gmail.com',
    'website': "https://github.com/Kankitsuuu/odoo-practice",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base
    # /data/ir_module_category_data.xml
    # for the full list
    'category': 'Administration',
    'depends': ['base', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'data/hospital_disease_data.xml',
        'data/hospital_doctor_specialty_data.xml',
        'views/hospital_menus.xml',
        'views/hospital_doctor_views.xml',
        'views/hospital_patient_views.xml',
        'views/hospital_patient_analysis_views.xml',
        'views/hospital_patient_analysis_category_views.xml',
        'views/hospital_visit_views.xml',
        'views/hospital_disease_views.xml',
        'views/hospital_disease_category_views.xml',
        'views/hospital_diagnosis_views.xml',
        'views/hospital_contact_person_views.xml',
        'views/hospital_doctor_change_views.xml',
        'views/hospital_doctor_schedule_views.xml',
        'views/hospital_doctor_specialty_views.xml',
        'wizard/doctor_change_multi_wizard_views.xml',
        'wizard/doctor_schedule_wizard_views.xml',
        'wizard/disease_periodic_report_wizard_views.xml',
        'wizard/patient_change_visit_wizard_views.xml',
        'wizard/visit_create_wizard_views.xml',
        'reports/disease_periodic_report_template.xml',
        'data/hospital_disease_data.xml',
    ],

    # only loaded in demonstration mode
    'demo': [
        'demo/hospital_doctor_demo.xml',
        'demo/hospital_patient_demo.xml',
        'demo/hospital_disease_demo.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
