# -*- coding: utf-8 -*-

import logging
from odoo import models, fields, _, api

logger = logging.getLogger(__name__)


class VisitorManagementCard(models.Model):
    # Identification attributes and database
     _name = 'visitor.management.card'
     _description = 'Visitor access card'

     # Special fields with internal behavior
     name = fields.Char(string="Folio", required=False, copy=False,
                        readonly=True, index=True,
                        default=lambda self: _('New'))
     active = fields.Boolean(string="Active", default=True)

     # Selection fields
     type = fields.Selection(string="Card type", selection=[
         ('customer', 'Customer'),
         ('student', 'Student'),
         ('supplier', 'Supplier'),
         ('visitor', 'Visitor')
     ], required=True, default='visitor', copy=True)

     # Basic fields
     note = fields.Text(string="Comment", required=False, copy=True)

     @api.model
     def create(self, values):
         # Add code here
         logger.info('********** Variables: {0}'.format(values))
         values['name'] = self.env['ir.sequence'].next_by_code(
             'sequence.visitor.management.card')
         return super(VisitorManagementCard, self).create(values)