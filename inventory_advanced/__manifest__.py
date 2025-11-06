# -*- coding: utf-8 -*-
{
    "name": "Inventory Advanced",
    "summary": "Inventory Advanced",
    "version": "18.0.1.0.0",
    "category": "Inventory/Configuration",
    "author": "",
    "license": "OEEL-1",
    "depends": ["stock"],
    "data": [
        "security/ir.model.access.csv",
        "views/pallet_type_views.xml",
        "views/rack_type_views.xml",
        "views/stock_location_views.xml",
        "views/stock_move_views.xml",
        "views/menu_views.xml",
    ],
    'assets': {
        'web.assets_backend': [
            'inventory_advanced/static/src/scss/suggest.scss',
        ],
    },
    "application": False,
    "installable": True,
}
