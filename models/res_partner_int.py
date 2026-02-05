from odoo import fields, models


class ResPartnerInt(models.Model):
    _inherit = 'res.partner'

    def compute_visitor_count(self):
        visitor_count = self.env['visit.insight'].search_count(
            [('partner_id', 'in', [a.id for a in self])])
        self.visitor_count = visitor_count

    # Basic fields
    is_visitor = fields.Boolean(string="Is visitor")
    visitor_personal_identification = fields.Char(string="ID Personal")
    visitor_count = fields.Integer(string="Visits",
                                   compute='compute_visitor_count',
                                   readonly=True)

    # Relational fields
    type_visitor_identification_id = fields.Many2one(
        'type.visitor.identification',
        string="Type visitor ID")

    # Binary and monetary data fields
    personal_id_imagen = fields.Binary(string="Personal ID imagen face A")
    personal_id_imagen_b = fields.Binary(string="Personal ID imagen face B")

    def copy(self, default=None):
        default = default or {}
        if self.is_visitor:
            default['name'] = 'New visitor'
        res = super(ResPartnerInt, self).copy(default)
        return res

    def action_view_visits(self):
        # This method now correctly fetches every visit for the same visitor
        return {
            'type': 'ir.actions.act_window',
            'name': 'All Visits of Visitor',
            'view_mode': 'tree,form',
            'res_model': 'visit.insight',
            'domain': [('partner_id', '=', self.id)],
            # This domain will fetch all visits for the same visitor
            'context': dict(self._context),
        }