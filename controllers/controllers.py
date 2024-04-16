# -*- coding: utf-8 -*-
# from odoo import http


# class JllCornercookie(http.Controller):
#     @http.route('/jll_cornercookie/jll_cornercookie', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/jll_cornercookie/jll_cornercookie/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('jll_cornercookie.listing', {
#             'root': '/jll_cornercookie/jll_cornercookie',
#             'objects': http.request.env['jll_cornercookie.jll_cornercookie'].search([]),
#         })

#     @http.route('/jll_cornercookie/jll_cornercookie/objects/<model("jll_cornercookie.jll_cornercookie"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('jll_cornercookie.object', {
#             'object': obj
#         })
