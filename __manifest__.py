# -*- encoding: utf-8 -*-
# noinspection PyStatementEffect
{
    'name': 'Event Registration',
    'author': "Kaiser Quezada",
    'version': '12.0.1',
    'depends': [],
    'installable': True,
    'data': [
        # Security
        'security/ir.model.access.csv',
        # Data
        'data/contact.xml',
        'data/lead.xml',
        'data/server_action.xml',
        # Views
        'views/views.xml',
    ],
    'application': True,
}
