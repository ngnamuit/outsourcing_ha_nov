# -*- coding: utf-8 -*-
from odoo import api, fields, models


class StockLocation(models.Model):
    _inherit = "stock.location"

    height = fields.Float(string="Height (mm)")
    width = fields.Float(string="Width (mm)")
    deep = fields.Float(string="Depth (mm)")
    weight = fields.Float(string="Maximum Weight (kg)")
    volume = fields.Float(string="Maximum Volume (m3)", compute="_compute_volume", store=True)
    rack_type_id = fields.Many2one(
        "rack.type",
        string="Rack Type",
        help="Physical rack/pallet specification used for this location."
    )
    rack_type_beam_width = fields.Integer(related="rack_type_id.beam_width", string="Beam Width (mm)")
    rack_type_pallet_type_id = fields.Many2one(related="rack_type_id.pallet_type_id", string="Pallets Type")
    rack_type_capacity = fields.Integer(related="rack_type_id.capacity", string="Capacity")
    is_rack_type = fields.Boolean(
        string="Is Rack Type",
        help="Tick if this location follows a specific rack type layout for location suggestion"
    )

    @api.depends('height', 'deep', 'width')
    def _compute_volume(self):
        """Formula: volume (m³) = (height * deep * width) / 1,000,000,000"""
        for rec in self:
            h = rec.height or 0.0
            d = rec.deep or 0.0
            w = rec.width or 0.0
            rec.volume = (h * d * w) / 1000000000 if (h and d and w) else 0.0
