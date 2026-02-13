# -*- coding: utf-8 -*-
from odoo import fields, models, api


class VehicleInsight(models.Model):
    # Identification attributes and database
    _name = 'vehicle.insight'
    _description = 'Vehicle insight'

    # Special fields with internal behavior
    name = fields.Char(string="License plate", required=True, index=True)

    # Relational fields
    brand_id = fields.Many2one('vehicle.brand', string="Make (of car)",
                               required=True)
    visit_insight_id = fields.Many2one('visit.insight', string="Vehicle ID",
                                       ondelete='cascade')

    # Basic fields
    trailer_plate = fields.Char(string="Trailer plate", required=False, copy=False)
    model = fields.Char(string="Model", required=False, copy=False)
    year_manufacture = fields.Char(string="Year manufacture", required=False,
                                   copy=False)
    color = fields.Integer(string="Color", readonly=False)

    # Basic fields, related fields to fetch visits details
    folio = fields.Char(string="Folio", related="visit_insight_id.name")
    partner_name = fields.Char(string="Visitor name", related="visit_insight_id.partner_id.name")
    visitor_company_name = fields.Char(string="Company name", related="visit_insight_id.visitor_company_name")
    employee_name = fields.Char(string="Meeting With", related="visit_insight_id.employee_id.name")
    visitor_card_name = fields.Char(string="Visitor Card", related="visit_insight_id.visitor_card_id.name")
    check_in_datetime = fields.Datetime(string="CheckIn Date", related="visit_insight_id.check_in_datetime")
    check_out_datetime = fields.Datetime(string="CheckOut Date", related="visit_insight_id.check_out_datetime")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('checkin', 'CheckIn'),
        ('checkout', 'CheckOut'),
        ('cancelled', 'Cancelled')
    ], string='Status', related="visit_insight_id.state")



class VehicleBrand(models.Model):
    # Identification attributes and database
    _name = 'vehicle.brand'
    _description = 'Vehicle brand'
    # Behavioral and order attributes
    _order = 'name'

    # Special fields with internal behavior
    name = fields.Char(string="Make (of car)", required=True, index=True)

    # Selection fields
    category = fields.Selection(string="category", selection=[
        ('automobile', 'Automobile'),
        ('truck_automobile', 'Truck/Automobile'),
        ('truck', 'Truck')
    ], required=True, default='automobile', copy=True)

    # Basic fields
    origin = fields.Char(string="Main origin", required=True, copy=False)
    segment = fields.Char(string="Featured segment", required=False, copy=False)


