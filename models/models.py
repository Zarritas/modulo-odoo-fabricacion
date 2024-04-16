# -*- coding: utf-8 -*-

from odoo import models, fields, api


class proveedor(models.Model):
    _name = 'jll_cornercookie.proveedor'
    _description = 'Proveedores de Materias Primas'

    name = fields.Char('Código de Proveedor')
    nombre = fields.Char('Nombre', required=True)
    dni = fields.Char('CIF/NIF/DNI', size=9, required=True)
    telefono = fields.Integer('Teléfono de contacto', size=9, required=True)
    autonomo = fields.Boolean('¿Es autonomo?', default=False)
    id_pedidos = fields.Many2one('jll_cornercookie.pedido',string='Pedidos')
    
class pedido(models.Model):
    _name = 'jll_cornercookie.pedido'
    _description = 'Pedidos de Materias Primas'
    
    name = fields.Char('Código de Pedido')
    fechapedido = fields.Date('Fecha de pedido', default=fields.Date.today())
    id_proveedor = fields.One2many('jll_cornercookie.proveedor','id_pedidos',string='Proveedor')