# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import timedelta, datetime
import random


class Proveedor(models.Model):
    _name = 'jll_cornercookie.proveedor'
    _description = 'Proveedores de Materias Primas'

    name = fields.Char('Código de Proveedor',compute='_crear_codigo')
    nombre = fields.Char('Nombre', required=True)
    dni = fields.Char('CIF/NIF/DNI', size=9, required=True)
    telefono = fields.Char('Teléfono de contacto', size=9, required=True)
    autonomo = fields.Boolean('¿Es autonomo?', default=False)
    id_pedidos = fields.One2many('jll_cornercookie.pedido','id_proveedor',string='Pedidos')
    
    @api.depends()
    def _crear_codigo(self):
        for proveedor in self:
            proveedor.name = str(proveedor.nombre[0:3])+str(proveedor.dni[-3:])

class PedidoMateriaPrima(models.Model):
    _name = 'jll_cornercookie.pedido_materiaprima'
    _description = 'Pedidos de Materias Primas'
    
    id_materiaprima = fields.Many2one('jll_cornercookie.materiaprima', string='Materia Prima')
    id_pedido = fields.Many2one('jll_cornercookie.pedido', string='Pedido')
    cantidad = fields.Integer('Cantidad')

class Pedido(models.Model):
    _name = 'jll_cornercookie.pedido'
    _description = 'Pedidos de Materias Primas'
    
    name = fields.Char('Código de Pedido', compute='_crear_codigo')
    fecha_pedido = fields.Datetime('Fecha de Pedido', readonly=True, default=lambda self: fields.datetime.now())
    id_proveedor = fields.Many2one('jll_cornercookie.proveedor', string='Proveedor', required=True)
    pedidos_materiasprimas = fields.One2many('jll_cornercookie.pedido_materiaprima', 'id_pedido', string='Materias Primas')
            
    @api.depends('fecha_pedido')
    def _crear_codigo(self):
        for pedido in self:
            pedido.name =  str(pedido.fecha_pedido.strftime("%d/%m/%Y")) + '-' + str(pedido.id_proveedor.name)

            
class MateriaPrima(models.Model):
    _name = 'jll_cornercookie.materiaprima'
    _description = 'Materias primas que se van a usar para realizar las galletas'
    _rec_name = 'nombre'
    
    nombre = fields.Char('Nombre', required=True)
    medida = fields.Selection(selection=[("M", "Metros"), ("G", "Gramos"), ("U", "Unidades")])
    cantidad_disponible = fields.Integer('Cantidad disponible', compute='_cantidades')
    pedidos_asociados = fields.Many2many('jll_cornercookie.pedido', string='Pedidos asociados')
    pedido_materiaprima_ids = fields.One2many('jll_cornercookie.pedido_materiaprima', 'id_materiaprima', string='Pedidos de Materia Prima')
            
    @api.depends('pedido_materiaprima_ids.cantidad')
    def _cantidades(self):
        for materiaprima in self:
            materiaprima.cantidad_disponible = sum(materiaprima.pedido_materiaprima_ids.mapped('cantidad'))

class Producto(models.Model):
    _name = 'jll_cornercookie.producto'
    _description = 'Productos que vamos a fabricar'
    
    name = fields.Char('Nombre', store=True)

    precio = fields.Monetary('Precio por unidad',currency_field='currency_id')
    precio_total = fields.Monetary('Precio total',compute='_precio_total', store=True, currency_field='currency_id')
    currency_id = fields.Many2one('res.currency', string='Moneda', default=lambda self: self.env.company.currency_id)
    cantidad = fields.Integer('Cantidad disponible')
    id_horneadas = fields.One2many('jll_cornercookie.hornada','id_producto',string='Horneadas asociadas')
    id_procesos = fields.Many2many('jll_cornercookie.proceso',string='Procesos que se necesitan')
    ean = fields.Char('Código EAN', size=13)

    @api.model
    def _generate_unique_ean(self):
        return ''.join([str(random.randint(0, 9)) for _ in range(13)])

    @api.model
    def create(self, vals):
        if not vals.get('ean'):  # Si no se proporciona un EAN, genera uno único
            vals['ean'] = self._generate_unique_ean()
            while self.env['jll_cornercookie.producto'].search_count([('ean', '=', vals['ean'])]) > 0:
                vals['ean'] = self._generate_unique_ean()  # Genera otro EAN si ya existe uno igual
        return super(Producto, self).create(vals)
            
    @api.depends('precio','cantidad')
    def _precio_total(self):
        for producto in self:
            producto.precio_total = producto.precio*producto.cantidad

class Hornada(models.Model):
    _name = 'jll_cornercookie.hornada'
    _description = 'Hornadas del producto'
    
    name = fields.Char('Código Hornada',compute='_crear_codigo')
    cantidad = fields.Integer('Cantidad de producto producido')
    fecha_creacion = fields.Datetime('Fecha de Horneación',readonly=True, default=lambda self: fields.datetime.now())
    fecha_caducidad = fields.Date('Fecha de Caducidad',compute='_calcular_fecha_caducidad')
    id_producto = fields.Many2one('jll_cornercookie.producto',string='Producto')
    
    @api.depends('fecha_creacion')
    def _crear_codigo(self):
        for hornada in self:
            hornada.name =  str(hornada.fecha_creacion.strftime("%d/%m/%Y|%H:%M:%S")) + '-' + str(hornada.id_producto.name)

    @api.depends('fecha_creacion')
    def _calcular_fecha_caducidad(self):
        for caducidad in self:
            caducidad.fecha_caducidad = caducidad.fecha_creacion.date()
            caducidad.fecha_caducidad += timedelta(days=1461)

class Proceso(models.Model):
    _name = 'jll_cornercookie.proceso'
    _description = 'Proceso para realizar los productos'
    
    name = fields.Char('Código del proceso')
    tipo = fields.Selection(selection=[("Mix","Mixto"),("Man","Manual"),("Maq","Maquinaria")])
    tiempo = fields.Float(string='Tiempo (horas)', digits=(6, 2))
    id_productos = fields.Many2many('jll_cornercookie.producto',string='Productos en los que se usa')
    id_maquinaria = fields.Many2one('jll_cornercookie.maquinaria',string='Maquina disponible')

class Maquinaria(models.Model):
    _name = 'jll_cornercookie.maquinaria'
    _description = 'Maquinaria de la empresa'
    
    name = fields.Char('Código de Máquina',compute='_crear_codigo', help='Código autogenerado, primerors 3 caracteres de nombre, modelo y fabricante.')
    nombre = fields.Char('Nombre de maquinaria')
    modelo = fields.Char('Modelo')
    cantidad = fields.Char('Cantidad de maquinaria disponible',help='Número de maquinas de las que disponemos')
    fabricante = fields.Char('Fabricante',help='Nombre del fabricante')
    id_procesos = fields.One2many('jll_cornercookie.proceso','id_maquinaria',string='Procesos disponibles')
    
    @api.depends()
    def _crear_codigo(self):
        for maquinaria in self:
            maquinaria.name = str(maquinaria.nombre[:3])+'-'+str(maquinaria.modelo[:3])+'-'+str(maquinaria.fabricante[:3])