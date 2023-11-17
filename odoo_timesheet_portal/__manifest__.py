# -*- coding: utf-8 -*-
{
    'name': "Timesheet Portal Approval",

    'summary': """
        Customer can approve timesheet from portal.""",

    'description': """
        Customer can approve timesheet from portal.
    """,

    'author': "Oranjewood",
    'category': "tools",
    'version': "16.0.1",
    "license": "LGPL-3",
    # any module necessary for this one to work correctly
    'depends': ['hr_timesheet','portal'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/timesheet_portal.xml',
        'views/timesheet.xml',
        'views/email_template.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            '/odoo_timesheet_portal/static/src/js/timesheet_approve.js',
            '/odoo_timesheet_portal/static/src/css/reason.css',
        ],
    },
    
    'images': ['static/description/banner.jpg'],
    'autoinstall': False,
    'installable': True,
    'application': False
}
