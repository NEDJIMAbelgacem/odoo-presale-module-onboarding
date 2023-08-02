# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'presale',
    'summary': 'Track pre-sale related things',
    'description': "Pre-Sale management app",
    'category': "PresSale Management",
    'depends': ['base', 'sale', 'product'],
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/cron_action.xml',
        'views/presale_order_line_views.xml',
        'views/presale_views.xml',
        'views/sale_order_views.xml',
        'views/presale_menus.xml',
    ],
    'installable': True,
    'application': True,
}