{
    'name': 'Labex LIMS Core',
    'version': '1.0.0',
    'category': 'Healthcare/Laboratory',
    'summary': 'Advanced Laboratory Information Management System for Odoo',
    'description': """
        Core module for managing laboratory operations, including:
        * Sample Registration and Tracking
        * Test Definition and Execution
        * Equipment Management
        * Results Recording and Validation
    """,
    'author': 'Jules AI',
    'website': 'https://www.yourcompany.com',
    'depends': ['base', 'mail', 'stock', 'uom'],
    'data': [
        'security/ir.model.access.csv',
        'data/ir_sequence_data.xml',
        'views/lims_menus.xml',
        'views/lims_patient_views.xml',
        'views/lims_sample_views.xml',
        'views/lims_equipment_views.xml',
        'views/lims_config_views.xml',
        'views/res_company_views.xml',
        'reports/lims_sample_report.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
