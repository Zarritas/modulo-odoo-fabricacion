# -*- coding: utf-8 -*-

from odoo import models, fields, api


class proveedor(models.Model):
    _name = 'jll_cornercookie.proveedor'
    _description = 'Proveedores de Materias Primas'

    name = fields.Char('Código de Proveedor',compute='_crear_codigo')
    nombre = fields.Char('Nombre', required=True)
    dni = fields.Char('CIF/NIF/DNI', size=9, required=True)
    telefono = fields.Char('Teléfono de contacto', size=9, required=True)
    autonomo = fields.Boolean('¿Es autonomo?', default=False)
    id_pedidos = fields.Many2one('jll_cornercookie.pedido',string='Pedidos')
    
    @api.depends()
    def _crear_codigo(self):
        for proveedor in self:
            proveedor.name = str(proveedor.nombre[0:3])+str(proveedor.dni[-3:])
            
class pedido(models.Model):
    _name = 'jll_cornercookie.pedido'
    _description = 'Pedidos de Materias Primas'
    
    name = fields.Char('Código de Pedido')
    fechapedido = fields.Date('Fecha de pedido', default=fields.Date.today())
    id_proveedor = fields.One2many('jll_cornercookie.proveedor','id_pedidos',string='Proveedor')
    id_materias_primas = fields.Many2many('jll.cornercookie.materiaprima','Contenido del pedido')
    
class materiaprima(models.Model):
    _name = 'jll.cornercookie.materiaprima'
    _description = 'Materias primas qe se va a usar para realizar las galletas'
    
    name = fields.Char('Código de Materia Prima')
    nombre = fields.Char('Nombre', required=True)
    medida = fields.Selection(selection=[("M","Metros"),("G","Gramos"),("U","Unidades")])
    cantidad_disponible = fields.Integer('Cantidad disponible')
    id_pedidos = fields.Many2many('jll_cornercookie.pedido','Pedidos asociados')
    
class producto(models.Model):
    _name = 'jll.cornercookie.producto'
    _description = 'Productos que vamos a vender'
    
    name = fields.Char('Código del producto')
    precio = fields.Float('Precio por unidad')
    cantidad = fields.Integer('Cantidad disponible')
    ean = fields.Char('Código EAN', required=True)
    id_horneadas = fields.Many2one('jll.cornercookie.hornada','Horneadas asociadas')
    id_procesos = fields.Many2many('jll_cornercookie.proceso','Procesos que se necesitan')
    
class hornada(models.Model):
    _name = 'jll.cornercookie.hornada'
    _description = 'Hornadas del producto'
    
    name = fields.Char('Código Hornada',required=True)
    cantidad = fields.Integer('Cantidad de producto producido')
    fecha_caducidad = fields.Date('Fecha de Caducidad')
    id_producto = fields.One2many('jll.cornercookie.producto','id_horneadas','Producto')
    
class proceso(models.Model):
    _name = 'jll_cornercookie.proceso'
    _description = 'Proceso para realizar los productos'
    
    name = fields.Char('Código del proceso')
    tipo = fields.Selection(selection=[("Mix","Mixto"),("Man","Manual"),("Maq","Maquinaria")])
    id_productos = fields.Many2many('jll.cornercookie.producto','Productos en los que se usa')
    id_maquinaria = fields.One2many('jll_cornercookie.maquinaria','id_procesos','Maquina disponible')
    
class maquinaria(models.Model):
    _name = 'jll_cornercookie.maquinaria'
    _description = 'Maquinaria de la empresa'
    
    name = fields.Char('Código de Máquina')
    nombre = fields.Char('Nombre de maquinaria')
    modelo = fields.Char('Modelo')
    cantidad = fields.Char('Cantidad de maquinaria disponible')
    fabricante = fields.Char('Fabricante')
    id_procesos = fields.Many2one('jll_cornercookie.proceso','Procesos disponibles')