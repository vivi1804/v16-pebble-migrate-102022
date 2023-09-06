# -*- coding: utf-8 -*-
{
    'name': 'Project and Product References',
    'category': 'Website/Website',
    'summary': 'Publish your project references',
    'version': '1.0',
    'description': """
Publish your project and product detail as business references on your website to attract new potential prospects.
    """,
    'depends': [
        'website',
        'pebble_partner_extended',
        'solar_extended',
    ],
    'data': [
        'views/website_project_view.xml',
        'views/website_product_view.xml',
        'views/website_project_portal_view.xml',
        'views/website_product_portal_view.xml',
        'views/website_project_menu.xml',
        'security/ir.model.access.csv',
    ],
    'qweb': [],
    'installable': True,
}
