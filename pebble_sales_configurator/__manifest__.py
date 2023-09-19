# -*- coding: utf-8 -*-
{
    'name': 'Sales configurator on portal',
    'category': 'Website/Website',
    'summary': 'sales configurator on portal',
    'version': '1.0',
    'description': """
    """,
    'depends': [
        'website',
        'crm',
        'sale',
        'sale_management',
        'solar_extended',
    ],
    'assets': {
        'web.assets_frontend': [
            '/pebble_sales_configurator/static/src/js/main.js',  # Include your local JavaScript file
            '/pebble_sales_configurator/static/src/css/web_style.css',
        ],
        'web.assets_vendor': [
            'https://ajax.googleapis.com/ajax/libs/jquery/2.1.1/jquery.min.js',  # Include the external JavaScript file from a URL
        # Include other vendor libraries as needed
        ],
    },
    'data': [
        'security/security.xml',
        'views/sales_config_view.xml',
        'views/website_sales_config_portal_view.xml',
        'views/website_sales_config_portal_images_view.xml',
        'views/sales_res_company.xml',
        'data/sales_config_menuitem.xml',
        'data/website_config_enphase.xml',
        'data/action.xml',
        'security/ir.model.access.csv',
        'reports/sales_configurator_report_template.xml',
    ],
    'qweb': [],
    'installable': True,
}