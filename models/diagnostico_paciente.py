from odoo import fields, models, api


class DiagnosticoPaciente(models.Model):
    _name = 'po_pac.diagnostico_paciente'
    _description = 'Diagnóstico Paciente'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'fecha_diagnostico desc'

    name = fields.Char(string='Nombre', compute='compute_name')
    paciente_id = fields.Many2one('po_pac.paciente', string='Paciente', required=True, tracking=True)
    fecha_diagnostico = fields.Date(string='Fecha de diagnóstico', required=True, tracking=True)
    diagnostico_cie_10_id = fields.Many2one('po_pac.diagnostico_cie_10', string='Diagnóstico', required=True, tracking=True)
    localizacion_diagnostico_id = fields.Many2one('po_pac.localizacion_diagnostico', string='Localización', required=True, tracking=True)
    base_diagnostico_id = fields.Many2one('po_pac.base_diagnostico', string='Base', required=True, tracking=True)
    primarios_multiples = fields.Selection(string='Primarios múltiples', selection=[('Si', 'Si'), ('No', 'No'), ('Se ignora', 'Se ignora')], required=True, tracking=True)
    estadio_diagnostico_id = fields.Many2one('po_pac.estadio_diagnostico', string='Estadío', tracking=True)
    t_diagnostico_id = fields.Many2one('po_pac.t_diagnostico', string='T', tracking=True)
    n_diagnostico_id = fields.Many2one('po_pac.n_diagnostico', string='N', tracking=True)
    m_diagnostico_id = fields.Many2one('po_pac.m_diagnostico', string='M', tracking=True)
    anatomia_patologica = fields.Selection(string='Anatomía Patológica', selection=[('Si','Si'),('No','No')], required=True, tracking=True)
    principal = fields.Boolean(string='Principal', tracking=True)

    @api.model_create_multi
    def create(self, vals):
        diagnostico_paciente = super(DiagnosticoPaciente, self).create(vals)

        if diagnostico_paciente.principal:
            diagnostico_paciente.set_principal_unico()

        return diagnostico_paciente

    def write(self, vals):
        res = super(DiagnosticoPaciente, self).write(vals)

        if vals.get('principal'):
            self.set_principal_unico()

        return res

    def compute_name(self):
        for diagnostico_paciente in self:
            if diagnostico_paciente.diagnostico_cie_10_id:
                name = diagnostico_paciente.diagnostico_cie_10_id.name
                diagnostico_paciente.name = name
            else:
                diagnostico_paciente.name = ''

    def set_principal_unico(self):
        for diagnostico in self:
            if diagnostico.principal:
                #Busca si hay algún otro principal y lo marca en false
                diagnosticos_principales = self.search([('paciente_id', '=', diagnostico.paciente_id.id), ('principal', '=', True), ('id', '!=', diagnostico.id)])
                if diagnosticos_principales:
                    diagnosticos_principales.write({'principal': False})


class LocalizacionDiagnostico(models.Model):
    _name = 'po_pac.localizacion_diagnostico'
    _description = 'Localización de diagnóstico'

    name = fields.Char(string='Nombre', required=True)
    active = fields.Boolean(string='Activo', default=True)

class BaseDiagnostico(models.Model):
    _name = 'po_pac.base_diagnostico'
    _description = 'Base de diagnóstico'

    name = fields.Char(string='Nombre', required=True)
    active = fields.Boolean(string='Activo', default=True)

class EstadioDiagnostico(models.Model):
    _name = 'po_pac.estadio_diagnostico'
    _description = 'Estadío de diagnóstico'

    name = fields.Char(string='Nombre', required=True)
    active = fields.Boolean(string='Activo', default=True)

class TDiagnostico(models.Model):
    _name = 'po_pac.t_diagnostico'
    _description = 'T de diagnóstico'

    name = fields.Char(string='Nombre', required=True)
    active = fields.Boolean(string='Activo', default=True)

class NDiagnostico(models.Model):
    _name = 'po_pac.n_diagnostico'
    _description = 'N de diagnóstico'

    name = fields.Char(string='Nombre', required=True)
    active = fields.Boolean(string='Activo', default=True)

class MDiagnostico(models.Model):
    _name = 'po_pac.m_diagnostico'
    _description = 'M de diagnóstico'

    name = fields.Char(string='Nombre', required=True)
    active = fields.Boolean(string='Activo', default=True)
