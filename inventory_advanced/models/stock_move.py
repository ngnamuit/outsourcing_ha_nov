# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError


class StockMove(models.Model):
    _inherit = "stock.move"

    product_volume = fields.Float(related="product_id.volume")
    product_weight = fields.Float(related="product_id.weight")
    picking_type_code = fields.Selection(related='picking_id.picking_type_code')
    suggest_line_ids = fields.One2many(
        "stock.suggest.location", "move_id", string="Suggested Location"
    )

    def action_fill_suggest_lines(self, limit=10):
        self.ensure_one()
        product = self.product_id or None
        quantity = self.product_uom_qty or 0
        warehouse_id = self.location_dest_id.warehouse_id.id if self.location_dest_id else\
            self.picking_id.location_dest_id.warehouse_id.id
        if not product or not quantity or not warehouse_id:
            raise UserError("Please set Product and Demand first.")

        unit_vol = (product.volume or 0.0)
        unit_w = (product.weight or 0.0)
        req_vol = unit_vol * quantity

        sql = f"""
            WITH valid AS (
                SELECT l.*
                FROM stock_location l
                WHERE l.active = TRUE
                  AND l.usage = 'internal'
                  AND l.is_rack_type = TRUE
                  AND l.warehouse_id = {warehouse_id}
            ),
            used AS (
                SELECT
                    q.location_id,
                    COALESCE(SUM(COALESCE(pt.volume,0) * q.quantity),0) AS used_m3,
                    COALESCE(SUM(COALESCE(pt.weight,0) * q.quantity),0) AS used_kg
                FROM stock_quant q
                JOIN product_product pp ON pp.id = q.product_id
                JOIN product_template pt ON pt.id = pp.product_tmpl_id
                WHERE q.quantity > 0
                  AND q.location_id IN (SELECT id FROM valid)
                GROUP BY q.location_id
            ),
            base AS (
                SELECT
                    l.id AS location_id,
                    COALESCE(l.volume, 0) AS capacity_m3,
                    COALESCE(l.weight, 3000) AS max_load_kg,
                    COALESCE(u.used_m3, 0) AS used_m3,
                    COALESCE(u.used_kg, 0) AS used_kg,
                    l.name,
                    l.rack_type_id,
                    rt.pallet_type_id,
                    rt.beam_width as beam_width_mm,
                    rt.capacity
                FROM valid l
                LEFT JOIN used u ON u.location_id = l.id
                LEFT JOIN rack_type rt ON rt.id = l.rack_type_id
            ),
            avail AS (
                SELECT
                    location_id,
                    capacity_m3,
                    used_m3,
                    GREATEST(capacity_m3 - used_m3, 0) AS available_m3,
                    GREATEST(max_load_kg - used_kg, 0) AS available_kg,
                    name,
                    rack_type_id,
                    pallet_type_id,
                    beam_width_mm,
                    capacity
                FROM base
            )
            SELECT location_id,
                   name,
                   capacity_m3, used_m3, available_m3, available_kg,
                   rack_type_id,
                   pallet_type_id,
                   beam_width_mm,
                   capacity
            FROM avail
            WHERE available_m3 >= {unit_vol}   -- minimum is a unit
              AND available_kg >= {unit_w}
            ORDER BY (available_m3 - {req_vol}) ASC  -- best-fit base on volume
            LIMIT 50;
        """
        self.env.cr.execute(sql)
        rows = self.env.cr.dictfetchall()

        remaining = quantity
        suggest_line_ids = []
        for row in rows:
            loc_id = row.get("location_id")
            av_m3 = float(row.get("available_m3") or 0.0)
            av_kg = float(row.get("available_kg") or 0.0)
            location_name = row.get("name")
            cap_by_vol = int(av_m3 // unit_vol) if unit_vol > 0.0 else int(remaining)
            cap_by_w = int(av_kg // unit_w) if unit_w > 0.0 else int(remaining)

            # skip if not vol or cap in shelf
            fit = max(0, min(cap_by_vol, cap_by_w))
            if fit <= 0:
                continue
            put = min(fit, remaining)

            values = {
                "name": location_name,
                "location_id": loc_id,
                "available_volume": av_m3,
                "available_weight": av_kg,
                "suggested_qty": float(put),
            }
            suggest_line_ids.append(values)
            remaining -= put

            if remaining <= 0 and len(suggest_line_ids) == limit:
                break

        if remaining > 0:
            suggest_line_ids.append({
                "location_id": False,
                "suggested_qty": float(remaining),
                "note": "Remaining qty not allocated due to space limits",
            })

        self.write({"suggest_line_ids": [(5, 0, 0)] + [(0, 0, line) for line in suggest_line_ids]})
        return True


    # def action_apply_suggest_lines(self):
    #     """Từ các dòng đã chọn -> tạo move lines (plan) theo location"""
    #     self.ensure_one()
    #     if not self.suggest_line_ids:
    #         raise UserError("No suggestions to apply.")
    #
    #     total = 0.0
    #     for s in self.suggest_line_ids.filtered("select"):
    #         if not s.location_id:
    #             continue
    #         qty = s.suggested_qty
    #         total += qty
    #         self.env["stock.move.line"].create({
    #             "move_id": self.id,
    #             "product_id": self.product_id.id,
    #             "product_uom_id": self.product_uom.id,
    #             "product_uom_qty": qty,
    #             "qty_done": 0.0,
    #             "location_id": self.location_id.id or self.picking_id.location_id.id,
    #             "location_dest_id": s.location_id.id,
    #             "company_id": self.company_id.id,
    #         })
    #     if total == 0.0:
    #         raise UserError("Please select at least one suggested line.")
    #     return True
