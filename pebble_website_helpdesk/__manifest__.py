# -*- coding: utf-8 -*-
{
    'name': 'Pebble Website Helpdesk Extended',
    'category': 'Website/Website',
    'summary': 'Additional zipcode and housenumber in helpdesk',
    'version': '1.0',
    'description': """
Additional field zipcode and house number in helpdesk.
    """,
    'depends': ['website_helpdesk'],
    'data': [
        'views/website_helpdesk_extended.xml',
        'views/website_helpdesk_extended_portal.xml',
        'data/website_helpdesk.xml',
        'data/action.xml',
    ],
    'qweb': [],
    'installable': True,
}
