# -*- coding: utf-8 -*-
{
    'name': 'References snippet on website',
    'category': 'Website/Website',
    'summary': '',
    'version': '1.0',
    'description': """
Add snippet of the latest reference in website
    """,
    'depends': [
        'website_project',
    ],
    'data': [
        'views/snippet.xml',
    ],
    'assets': {
       'web.assets_frontend': [
           '/website_project_snippet/static/src/js/s_latest_projects.js',
       ],
    },
    'qweb': [],
    'installable': True,
}
