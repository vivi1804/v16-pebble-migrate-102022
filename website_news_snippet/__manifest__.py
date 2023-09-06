# -*- coding: utf-8 -*-
{
    'name': 'News snippet on website',
    'category': 'Website/Website',
    'summary': '',
    'version': '1.0',
    'description': """
Add snippet of the latest News in website
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
           '/website_news_snippet/static/src/js/s_latest_news.js',
       ],
    },
    'qweb': [],
    'installable': True,
}
