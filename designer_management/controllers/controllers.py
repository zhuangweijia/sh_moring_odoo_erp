# -*- coding: utf-8 -*-
# from odoo import http


# class DesignerManagement(http.Controller):
#     @http.route('/designer_management/designer_management/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/designer_management/designer_management/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('designer_management.listing', {
#             'root': '/designer_management/designer_management',
#             'objects': http.request.env['designer_management.designer_management'].search([]),
#         })

#     @http.route('/designer_management/designer_management/objects/<model("designer_management.designer_management"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('designer_management.object', {
#             'object': obj
#         })
