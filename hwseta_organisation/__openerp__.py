{
    'name' : 'HWSETA orgs',
    'version' : '1.1',
    'author' : 'Dylan Bridge',
    'category' : 'HWSETA',
    'description' : """
HWSETA Upload module covers.
====================================
    - Adds scheme.year recs to allow sync
    """,
    'website': 'https://www.odoo.com/page/billing',
    'depends' : ['hwseta_finance'],
    'data': [
        'data/scheme_year.xml',
        'views/wsp_submission_track.xml',
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
