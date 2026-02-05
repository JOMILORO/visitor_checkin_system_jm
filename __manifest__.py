# -*- coding: utf-8 -*-
{
    'name': "Visitor Check-in System",

    'summary': "Visitor Management by JOMILORO",

    'description': 'Manage Visitors: Oversee guest arrivals and departures, Keep Check-In, Check-Out. Details of Visitors: Maintain records of visitor entries and exits. '
                   'Issue Visitor Pass: Provide identification passes for access. Manage Visitor Belongings: Secure and track items brought by guests. '
                   'Manage Employee Belongings: Monitor and store personal items of staff. Print Property Label: Create and print labels for tracking property items.',

    'author': "Confecciones Textiles de Teziutlán",
    'maintainer': 'José Miguel López Roano',
    'website': "https://www.confetex.mx",
    
    'category': 'Human Resources/Visitor Check-in System',
    'version': '17.0.1.0.0',

    # any module necessary for this one to work correctly
    'depends': ['base', 'hr', 'contacts'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'demo/demo.xml',
        'data/ir_sequence_data.xml',
        'views/visitor_checkin_system_mn.xml',
        'views/visitor_management_card_vw.xml',
        'views/property_counter_vw.xml',
        'views/visit_insight_vw.xml',
        'views/vehicle_insight_vw.xml',
        'views/type_visitor_identification_vw.xml',
        'views/visit_insight_individual_vw.xml',
        'views/res_partner_int_vw.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [],
    'images': ['static/description/banner.gif'],
    'license': 'LGPL-3',
    'application': True,
    'installable': True,
    'auto_install': False,
}