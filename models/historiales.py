from odoo import api, fields, models


class HistorialEstadoPaciente(models.Model):
    _name = "po_pac.historial_estado_paciente"
    _description = 'Historial de estados de paciente'
    _order = 'fecha_hasta desc'

    paciente_id = fields.Many2one('po_pac.paciente', string='Paciente')
    estado = fields.Char(string='Estado')
    fecha_desde = fields.Date(string='Fecha desde')
    fecha_hasta = fields.Date(string='Fecha hasta')
    user_id = fields.Many2one('res.users', string='Usuario')
    observaciones = fields.Char(string='Observaciones')
