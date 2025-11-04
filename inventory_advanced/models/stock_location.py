# -*- coding: utf-8 -*-
from odoo import api, fields, models


class StockLocation(models.Model):
    _inherit = "stock.location"

    height = fields.Float(string="Height (mm)")
    deep = fields.Float(string="Depth (mm)")
    weight = fields.Float(string="Weight (kg)")
    rack_type_id = fields.Many2one(
        "stock.package.type",
        string="Rack Type",
        help="Physical rack/pallet specification used for this location."
    )
    is_rack_type = fields.Boolean(
        string="Is Rack Type",
        help="Tick if this location follows a specific rack type layout for location suggestion"
    )

