{
    'name' : 'HWSETA NLRD',
    'version' : '1.1',
    'author' : 'Dylan Bridge',
    'category' : 'nat learner reg db',
    'description' : """
HWSETA Upload module covers.
====================================
    - nlrd submissions
    """,
    'website': 'https://www.odoo.com/page/billing',
    'depends' : ['hwseta_etqe'],
    'data': [
        'security/hwseta_nlrd_security.xml',
        'security/ir.model.access.csv',
        'wizard/nlrd_wizard.xml',
        'wizard/admin_wizard.xml',
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
