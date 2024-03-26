from odoo import api, fields, models
from odoo.exceptions import ValidationError
from odoo.osv import expression


class ProfesionalMedico(models.Model):
    _name = 'po_pac.profesional_medico'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _descripcion = 'Profesional médico'

    name = fields.Char(string='Nombre', required=True, tracking=True)
    matricula = fields.Integer(string='Matrícula', required=True, tracking=True)
    especialidad_id = fields.Many2one('po_pac.especialidad_medica', string='Especialidad', required=True, tracking=True)
    active = fields.Boolean(string='Activo', default=True, tracking=True)

    # Cambia el método de busqueda para que también busque por matrícula
    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, order=None):
        args = args or []
        if operator == 'ilike' and not (name or '').strip():
            domain = []
            retorno = self._search(expression.AND([domain, args]), limit=limit, order=order)
        else:
            try:
                domain = ['|', ('name', 'ilike', name), ('matricula', '=', name)]
                retorno = self._search(expression.AND([domain, args]), limit=limit, order=order)
            except:
                domain = [('name', 'ilike', name)]
                retorno = self._search(expression.AND([domain, args]), limit=limit, order=order)
        return retorno


class EspecialidadMedica(models.Model):
    _name = 'po_pac.especialidad_medica'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _descripcion = 'Especialidad médica'

    name = fields.Char(string='Nombre', required=True, tracking=True)
    active = fields.Boolean(string='Activo', default=True, tracking=True)