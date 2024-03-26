from odoo import fields, models, api


class FuentePaciente(models.Model):
    _name = 'po_pac.fuente_paciente'
    _description = 'Fuente Paciente'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Nombre', compute='compute_name')
    paciente_id = fields.Many2one('po_pac.paciente', string='Paciente', required=True, tracking=True)
    hospital_id_fuente = fields.Many2one('po_pac.hospital', string='Fuente (hospital)', required=True, tracking=True)
    profesional_medico_id = fields.Many2one('po_pac.profesional_medico', string='Profesional tratante', required=True, tracking=True)
    especialidad_medica_id = fields.Many2one('po_pac.especialidad_medica', string='Especialidad')
    fuente_activa = fields.Boolean(string='Fuente activa')
    observaciones = fields.Char(string='Observaciones')

    def compute_name(self):
        for fuente_paciente in self:
            if fuente_paciente.hospital_id_fuente and fuente_paciente.profesional_medico_id:
                name = fuente_paciente.hospital_id_fuente.name + ' - ' + fuente_paciente.profesional_medico_id.name
                if fuente_paciente.fuente_activa:
                    name += ' (Activa)'

                fuente_paciente.name = name
            else:
                fuente_paciente.name = ''

    def create(self, vals):
        fuentes_creadas = super(FuentePaciente, self).create(vals)

        for fuente in fuentes_creadas:
            fuente.set_fuente_activa_unica()

        return fuentes_creadas

    def write(self, vals):
        res = super(FuentePaciente, self).write(vals)

        if vals.get('fuente_activa'):
            self.set_fuente_activa_unica()

        return res

    def set_fuente_activa_unica(self):
        for fuente in self:
            if fuente.fuente_activa:
                #Busca si hay alguna otra activa y la marca en false
                fuentes_activas = self.search([('paciente_id', '=', fuente.paciente_id.id), ('fuente_activa', '=', True), ('id', '!=', fuente.id)])
                if fuentes_activas:
                    fuentes_activas.write({'fuente_activa': False})

    @api.onchange('profesional_medico_id')
    def set_especialidad_by_profesional_medico(self):
        for fuente in self:
            if fuente.profesional_medico_id and fuente.profesional_medico_id.especialidad_id:
                fuente.especialidad_medica_id = fuente.profesional_medico_id.especialidad_id.id

class Hospital(models.Model):
    _name = 'po_pac.hospital'
    _description = 'Hospital'

    name = fields.Char(string='Nombre', required=True)
    active = fields.Boolean(string='Activo', default=True)
