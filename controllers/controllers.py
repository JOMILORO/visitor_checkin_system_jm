# -*- coding: utf-8 -*-
# from odoo import http


# class VisitorCheckinSystemJm(http.Controller):
#     @http.route('/visitor_checkin_system_jm/visitor_checkin_system_jm', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/visitor_checkin_system_jm/visitor_checkin_system_jm/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('visitor_checkin_system_jm.listing', {
#             'root': '/visitor_checkin_system_jm/visitor_checkin_system_jm',
#             'objects': http.request.env['visitor_checkin_system_jm.visitor_checkin_system_jm'].search([]),
#         })

#     @http.route('/visitor_checkin_system_jm/visitor_checkin_system_jm/objects/<model("visitor_checkin_system_jm.visitor_checkin_system_jm"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('visitor_checkin_system_jm.object', {
#             'object': obj
#         })

