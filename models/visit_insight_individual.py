from odoo import fields, models, api


class VisitInsightIndividual(models.Model):
    # Identification attributes and database
    _name = 'visit.insight.individual'
    _description = 'Visit insight individual'
    # Inheritance by delegation
    # This essentially connects this model to the template.
    # Each 'visit' belongs to a 'template'.
    _inherits = {'visit.insight': 'visit_insight_id'}
    _order = 'check_in_datetime desc'

    # Basic fields
    companion_name = fields.Char(string="Name of companion/visitor", required=True)
    visitor2_personal_identification = fields.Char(string="ID Personal")

    # Relational fields
    visitor2_card_id = fields.Many2one('visitor.management.card',
                                       string="Visitor Card")

    type2_visitor_identification_id = fields.Many2one('type.visitor.identification',
                                                     string="Type visitor ID")
    visit_insight_id = fields.Many2one(
        'visit.insight',
        string="Visit template",
        required=True,
        ondelete='cascade'
    )

    # Selection fields, related fields to fetch visitor cards details
    visitor2_card_type = fields.Selection(string="Card type", selection=[
        ('customer', 'Customer'),
        ('student', 'Student'),
        ('supplier', 'Supplier'),
        ('visitor', 'Visitor')
    ], related='visitor2_card_id.type', required=False)

