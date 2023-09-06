# -*- coding: utf-8 -*-
{
    'name': 'Blog snippet on website',
    'category': 'Website/Website',
    'summary': '',
    'version': '1.0',
    'description': """
Add snippet of the latest blog in website
    """,
    'depends': [
        'website_blog',
    ],
    'data': [
        'views/snippet.xml',
        'data/param.xml',
    ],
    'assets': {
       'web.assets_frontend': [
           '/website_blog_snippet/static/src/js/s_latest_posts.js',
       ],
    },
    'qweb': [],
    'installable': True,
}
