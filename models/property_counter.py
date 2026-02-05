# -*- coding: utf-8 -*-
import logging
from odoo import fields, models, _, api

logger = logging.getLogger(__name__)


class PropertyCounter(models.Model):
    # Identification attributes and database
    _name = 'property.counter'
    _description = 'Property Counter'
    # Behavioral and order attributes
    _rec_name = 'employee_name_id'

    # Special fields with internal behavior
    name = fields.Char(string="Folio", required=False, copy=False,
                       readonly=True, index=True,
                       default=lambda self: _('New'))
    active = fields.Boolean(string="Active", default=True)

    # Relational fields
    employee_name_id = fields.Many2one('hr.employee',
                                       string="Employee Name", required=True)
    belongings_ids = fields.One2many('personal.belongings',
                                     'property_counter_id',
                                     string="Property ID")

    # Basic fields
    employee_mobile_phone = fields.Char(string="Employee Contact",
                                   related='employee_name_id.mobile_phone')
    employee_department_name = fields.Char(string="Department",
                             related='employee_name_id.department_id.name',
                             required=True)
    employee_work_email = fields.Char(string="Email ID",
                          related='employee_name_id.work_email',
                          required=True)
    date = fields.Date(string="Date", required=True,
                       default=lambda self: fields.Datetime.now())

    @api.model
    def create(self, values):
        # Add code here
        logger.info('********** Variables: {0}'.format(values))
        values['name'] = self.env['ir.sequence'].next_by_code(
            'sequence.property.counter')
        return super(PropertyCounter, self).create(values)


class PersonalBelongings(models.Model):
    # Identification attributes and database
    _name = 'personal.belongings'
    _description = 'Personal Belongings'

    # Relational fields
    visit_insight_ids = fields.Many2one('visit.insight',
                                        string="Property ID", ondelete='cascade')
    property_counter_id = fields.Many2one('property.counter',
                                          string="Property ID", ondelete='cascade')
    # Basic fields
    property_name = fields.Char(string="Property Name")
    property_count = fields.Integer(string="Property Count")

    # Selection fields
    permission = fields.Selection([
        ('allowed', 'Allowed'),
        ('not_allowed', 'Not Allowed')
    ], default='allowed', string='Permission')