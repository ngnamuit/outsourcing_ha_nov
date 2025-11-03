# -*- coding: utf-8 -*-
from odoo import api, fields, models


class PalletType(models.Model):
    _name = "pallet.type"

    name = fields.Char("Name")

    _sql_constraints = [
        ('name_uniq', 'unique(name)', 'Name must be unique.'),
    ]



class CrackType(models.Model):
    _name = "crack.type"
    _description = "Crack Type"
    _order = "name"

    name = fields.Char(string="Name", required=True)
    beam_width = fields.Integer(string="Beam Width")
    pallets_type_id = fields.Many2one("pallet.type", string="Pallets Type")
    capacity = fields.Integer(string="Capacity")
    active = fields.Boolean(string="Active", default=True)

    _sql_constraints = [
        ('name_uniq', 'unique(name)', 'Name must be unique.'),
    ]
