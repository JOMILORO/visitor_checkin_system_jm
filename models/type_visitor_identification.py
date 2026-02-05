from odoo import fields, models, api


class TypeVisitorIdentification(models.Model):
    # Identification attributes and database
    _name = 'type.visitor.identification'
    _description = 'Type visitor identification'
    # Behavioral and order attributes
    _order = 'name'

    name = fields.Char(string="Visitor identification name", required=True, index=True)
    active = fields.Boolean(string="Active", default=True)
    short_description = fields.Text(string="Short description", required=False, copy=False)
