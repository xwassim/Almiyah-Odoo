# -*- coding: utf-8 -*-
{
    'name': "Reclamation Pgi",

    'summary': """Gestion Des Reclamations""",

    'description': """
        Gestion des reclamations module pour :
            - Gerer reclamation
            - Gerer clients et interventions            
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Test',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','hr','website',],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'security/securitychamp.xml',
        'templates.xml',
        'views/reclamation.xml',
        'views/agent.xml',
        'views/reclamant.xml',
        'views/website_form.xml',
        'views/intervention.xml',
        'views/equipe.xml',
        'views/decision.xml',
        'views/menu.xml',
	    'reports/reports.xml',
    ],

    # only loaded in demonstration mode
    'demo': [
        'demo.xml',
    ],
}
