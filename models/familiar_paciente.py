from odoo import fields, models


class FamiliarPaciente(models.Model):
    _name = "po_pac.familiar_paciente"
    _description = 'Familiar de paciente'

    paciente_id = fields.Many2one('po_pac.paciente', string='Paciente', required=True)
    nombre_familiar = fields.Char(string='Nombre', required=True)
    parentesco_id = fields.Many2one('po_pac.parentesco_familiar', string='Parentesco', required=True)
    telefono = fields.Char(string='Teléfono')
    country_id_nacionalidad = fields.Many2one("res.country", string='Nacionalidad')
    observaciones = fields.Char(string='Observaciones')

class ParentescoFamiliar(models.Model):
    _name = "po_pac.parentesco_familiar"
    _description = 'Parentesco familiar'

    name = fields.Char(string='Nombre', required=True)
    active = fields.Boolean(string='Activo', default=True)