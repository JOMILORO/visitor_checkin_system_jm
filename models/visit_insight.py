# -*- coding: utf-8 -*-
import logging
from email.policy import default
from datetime import timedelta

from odoo import fields, models, _, api

logger = logging.getLogger(__name__)


class VisitInsight(models.Model):
    # Identification attributes and database
    _name = 'visit.insight'
    _description = 'Visits'
    # Behavioral and order attributes
    _rec_name = 'partner_id'
    _order = 'check_in_datetime desc'

    def compute_visitor_count(self):
        visitor_count = self.env['visit.insight'].search_count(
            [('visitor_id', '=', self.visitor_id)])
        self.visitor_count = visitor_count

    @api.depends('check_in_datetime', 'check_out_datetime')
    def _compute_duration(self):
        for record in self:
            if record.check_in_datetime and record.check_out_datetime:
                # Calculate duration in seconds
                duration = record.check_out_datetime - record.check_in_datetime
                total_seconds = int(duration.total_seconds())

                # # Calculate hours, minutes, and seconds
                # hours = total_seconds // 3600
                # minutes = (total_seconds % 3600) // 60
                # seconds = total_seconds % 60

                # Store duration in hours as a float
                total_hours = total_seconds / 3600
                record.duration = total_hours

                # Extract the whole hours
                hours = int(total_hours)

                # Extract the minutes by multiplying the decimal part by 60
                # We use round() to avoid precision errors on floating-point numbers
                minutes = int(round((total_hours - hours) * 60))

                # Format to string "HH:MM"
                # :02d ensures that there are always two digits (e.g., 05 instead of 5)
                time_string = f"{hours:02d}:{minutes:02d}"
                record.formatted_duration = time_string

            else:
                record.duration = 0.0
                record.formatted_duration = "00:00"


    # Special fields with internal behavior
    name = fields.Char(string="Folio", required=False, copy=False,
                       readonly=True, index=True,
                       default=lambda self: _('New'))
    active = fields.Boolean(string="Active", default=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('checkin', 'CheckIn'),
        ('checkout', 'CheckOut'),
        ('cancelled', 'Cancelled')
    ], default='draft', string='Status')

    # Relational fields
    visitor_card_id = fields.Many2one('visitor.management.card',
                                   string="Visitor Card")
    partner_id = fields.Many2one('res.partner', required=True,
                                 string="Visitor name", ondelete='cascade')
    employee_id = fields.Many2one('hr.employee',
                                   string="Meeting With")
    type_visitor_identification_id = fields.Many2one('type.visitor.identification',
                                                     string="Type visitor ID",
                                                     related='partner_id.type_visitor_identification_id')
    property_ids = fields.One2many('personal.belongings',
                                   'visit_insight_ids',
                                   string="VProperty Id")
    vehicle_insight_ids = fields.One2many('vehicle.insight',
                                          'visit_insight_id', string="VVehicle Id")

    # Basic fields
    visitor_id = fields.Char(string="Visitor ID", readonly=False,
                             default=lambda self: _('New'))
    phone_no = fields.Char(string="Contact Number", readonly=False)
    mail_id = fields.Char(string="Email ID", readonly=False)
    visitor_company_name = fields.Char(string="Company name", readonly=False)
    is_company = fields.Boolean(string="It is a company", default=False)
    check_in_datetime = fields.Datetime(string="CheckIn Date", required=False,
                                        default=lambda self: fields.Datetime.now())
    check_out_datetime = fields.Datetime(string="CheckOut Date")
    purpose_of_visit = fields.Char(string="Purpose", required=True)
    duration = fields.Float(string="Duration (Hours)", compute='_compute_duration', readonly=True)
    formatted_duration = fields.Char("Duration (formatted)", compute='_compute_duration', readonly=True)
    visitor_count = fields.Integer(string="Visits", compute='compute_visitor_count', readonly=True)
    is_group = fields.Boolean(string="Group visit", default=False)
    has_car = fields.Boolean(string="Car access")
    visitor_personal_identification = fields.Char(string="ID Personal", related='partner_id.visitor_personal_identification')
    has_personal_belonging = fields.Boolean(string="Personal belonging")

    # Basic fields, related fields to fetch employee details
    meeting_with = fields.Char(string="Employee Name",
                               related='employee_id.name', required=True)
    employee_contact = fields.Char(string="Employee Contact",
                                   related='employee_id.mobile_phone')
    employee_department = fields.Char(string="Department",
                                      related='employee_id.department_id.name',
                                      required=True)
    employee_work_email = fields.Char(string="Email ID",
                                      related='employee_id.work_email',
                                      required=True)

    # Selection fields, related fields to fetch visitor cards details
    visitor_card_type = fields.Selection(string="Card type", selection=[
        ('customer', 'Customer'),
        ('student', 'Student'),
        ('supplier', 'Supplier'),
        ('visitor', 'Visitor')
    ], related='visitor_card_id.type', required=False)

    # Binary and monetary data fields
    personal_id_imagen = fields.Binary(string="Personal ID imagen face A",
                                       related='partner_id.personal_id_imagen')
    personal_id_imagen_b = fields.Binary(string="Personal ID imagen face B",
                                         related='partner_id.personal_id_imagen_b')

    # Reverse relationship to see all variants (companions or single visit)
    visit_insight_individual_ids = fields.One2many(
        'visit.insight.individual',
        'visit_insight_id',
        string="Individual visits"
    )

    @api.onchange('check_in_datetime', 'check_out_datetime')
    def _onchange_datetime(self):
        if self.check_in_datetime:
            # if not self.check_in_datetime or not self.check_out_datetime:
            self.state = 'checkin'
        else:
            self.state = 'draft'
        if self.check_out_datetime:
            # if not self.check_in_datetime or not self.check_out_datetime:
            self.state = 'checkout'

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        """Automatically fill visitor details if the visitor already exists."""
        if self.partner_id:
            existing_contact = self.env['res.partner'].browse(self.partner_id.id)
            existing_visit = self.search(
                [('partner_id', '=', self.partner_id.id)], limit=1)

            if existing_contact and existing_visit:
                # Populate fields with existing data
                self.visitor_id = existing_visit.visitor_id
                self.mail_id = existing_visit.mail_id
                self.phone_no = existing_visit.phone_no
                self.visitor_company_name = existing_visit.visitor_company_name
            else:
                # Generate a new visitor ID for a new partner
                self.visitor_id = 'New'
                self.mail_id = existing_contact.email
                self.phone_no = existing_contact.phone
                self.visitor_company_name = existing_contact.commercial_partner_id.name

    @api.model
    def create(self, values):
        # Add code here
        logger.info('********** Variables: {0}'.format(values))
        values['name'] = self.env['ir.sequence'].next_by_code(
            'sequence.visit.insight')

        # Ensure each new visit for the same visitor creates a new record,
        # even if visitor name is the same
        partner_id = values.get('partner_id')
        # Check if a visitor with the same partner_id exists
        existing_visit = self.search([('partner_id', '=', partner_id)],
                                     limit=1)
        if existing_visit:
            values['visitor_id'] = existing_visit.visitor_id
            # values['mail_id'] = existing_visit.mail_id
            # values['phone_no'] = existing_visit.phone_no
            # values['visitor_company_name'] = existing_visit.visitor_company_name
        else:
            values['visitor_id'] = self.env['ir.sequence'].next_by_code(
                'sequence.visitor.id') or 'New'

        # We created the template record
        template = super(VisitInsight, self).create(values)
        # We verify the condition: If it is NOT a group and NO variants have been passed manually
        # (This covers the case of automatic single variant creation)
        if not template.is_group and not template.visit_insight_individual_ids:
            template._create_variant_ids()
        return template

    def _create_variant_ids(self):
        """
        Generate the unique variant based on the template data.
        """
        self.ensure_one()
        vals = {
            'visit_insight_id': self.id,
            # Since it is a single visit, the "companion" is the same as the main visitor.
            'companion_name': self.partner_id.name,
            'type2_visitor_identification_id': self.type_visitor_identification_id.id,
            'visitor2_personal_identification': self.visitor_personal_identification or 'S/N',
            'visitor2_card_id': self.visitor_card_id.id
        }
        # We created the linked variant
        self.env['visit.insight.individual'].create(vals)

    def action_draft(self):
        for rec in self:
            rec.state = 'draft'

    def action_checkin(self):
        for rec in self:
            rec.state = 'checkin'

    def action_checkout(self):
        for record in self:
            record.check_out_datetime = fields.Datetime.now()
            record.state = 'checkout'

    def action_checkout1(self):
        for rec in self:
            rec.state = 'checkout'


    def action_cancel(self):
        for rec in self:
            rec.state = 'cancelled'

    def action_view_visits(self):
        # This method now correctly fetches every visit for the same visitor
        return {
            'type': 'ir.actions.act_window',
            'name': 'All Visits of Visitor',
            'view_mode': 'tree,form',
            'res_model': 'visit.insight',
            'domain': [('visitor_id', '=', self.visitor_id)],
            # This domain will fetch all visits for the same visitor
            'context': dict(self._context),
        }