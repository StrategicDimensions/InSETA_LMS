{
    'name' : 'HWSETA Reports',
    'version' : '1.1',
    'author' : 'Dylan Bridge',
    'category' : 'Skills and Development Management',
    'description' : """
HWSETA Report module covers.
====================================
    - accreditations
    """,
    'website': 'https://www.odoo.com/page/billing',
    'depends' : ['hwseta_etqe'],
    'data': [
        'wizard/seta_report_wizard.xml',
        'data/data.xml',
        'security/hwseta_report_security.xml',
        'security/ir.model.access.csv',
    ],
    'qweb' : [

    ],
    'demo': [
    ],
    'test': [
    ],
    
    'installable': True,
    'auto_install': False,
}
