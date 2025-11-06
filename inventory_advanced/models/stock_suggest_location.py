# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError


class StockSuggestLocation(models.Model):
    _name = "stock.suggest.location"

    name = fields.Char("Location")
    move_id = fields.Many2one("stock.move", ondelete="cascade")
    move_line_id = fields.Many2one("stock.move.line", ondelete="cascade")

    location_id = fields.Many2one("stock.location", string="Shelf (Location)")

    available_volume = fields.Float("Available Volume (m³)")
    available_weight = fields.Float("Available Weight (kg)")
    percent_used = fields.Char("% Used", compute="_compute_used", store=False)
    suggested_qty = fields.Float("Suggested Qty")

    rack_type_id = fields.Many2one(related="location_id.rack_type_id", string="Rack Type")
    beam_width = fields.Integer(related="rack_type_id.beam_width")
    pallet_type_id = fields.Many2one(related="rack_type_id.pallet_type_id", string="Pallets Type")
    capacity = fields.Integer(related="rack_type_id.capacity")
    note = fields.Char("Notes")

    @api.model
    def default_get(self, fields):
        res = super().default_get(fields)
        if res.get("rack_type_id"):
            rack_obj = self.env['rack.type'].browse(res.get("rack_type_id"))
            res['pallet_type_id'] = rack_obj.pallet_type_id.id if rack_obj and rack_obj.pallet_type_id else False
        return res

    def _compute_used(self):
        for rec in self:
            max_vol = rec.location_id.volume or 0.0
            max_wt = rec.location_id.weight or 0.0
            used_vol = max(max_vol - rec.available_volume, 0)
            used_wt = max(max_wt - rec.available_weight, 0)
            vol_used_pct = round((used_vol / max_vol) * 100, 2) if max_vol else 0
            wt_used_pct = round((used_wt / max_wt) * 100, 2) if max_wt else 0
            rec.percent_used = f"{vol_used_pct}% vol / {wt_used_pct}% weight"
