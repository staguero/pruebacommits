from odoo import fields, models, api


class DiagnosticoCIE10(models.Model):
    _name = 'po_pac.diagnostico_cie_10'
    _description = 'Diagnóstico CIE10'
    _sql_constraints = [('def_codigo_unique', 'unique(codigo)', 'Ya existe un Diagnóstico CIE10 con el código especificado.')]

    name = fields.Char(string="Nombre", required=True)
    codigo = fields.Char(string="Código", required=True)
    active = fields.Boolean(string='Activo', default=True)
