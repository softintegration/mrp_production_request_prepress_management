# -*- coding: utf-8 -*- 


{
    'name': 'Link Prepress management application and Manufacturing Requests module',
    'author': 'Soft-integration',
    'application': True,
    'installable': True,
    'auto_install': False,
    'qweb': [],
    'description': False,
    'images': [],
    'version': '1.0.1.7',
    'category': 'Prepress/Manufacturing',
    'demo': [],
    'depends': ['mrp_production_request','prepress_management'],
    'data': [
        'views/mrp_production_request_views.xml',
    ],
    'license': 'LGPL-3',
}
