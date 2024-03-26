from odoo import api, fields, models
from datetime import datetime


class InformeSocial(models.Model):
    _name = "po_pac.informe_social"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Informe social'

    paciente_id = fields.Many2one('po_pac.paciente', string='Paciente', required=True, tracking=True)
    estado = fields.Selection(string='Estado', selection=[
        ('Borrador', 'Borrador'),
        ('Pendiente de revisión', 'Pendiente de revisión'),
        ('Aprobado', 'Aprobado'),
        ('Rechazado', 'Rechazado'),
    ], default='Borrador', tracking=True)
    #create_date
    #write_date
    #create_uid
    #write_uid

    #Datos de aprobación
    fecha_aprobacion = fields.Date(string='Fecha de aprobación')
    user_id_aprobador = fields.Many2one('res.users', string='Usuario que aprobó')

    #Datos de rechazo
    fecha_rechazo = fields.Date(string='Fecha de rechazo')
    user_id_rechazador = fields.Many2one('res.users', string='Usuario que rechazó')
    motivo_rechazo = fields.Text(string='Motivo de rechazo')

    #Datos de salud
    internado = fields.Selection(string='Internado', selection=[
        ('Si', 'Si'),
        ('No', 'No')
    ])
    sala_internacion = fields.Char(string='Sala de internación')
    cama_internacion = fields.Char(string='Cama de internación')
    diagnostico = fields.Text(string='Diagnóstico')
    prestaciones = fields.Text(string='Prestaciones')
    antecedentes = fields.Text(string='Antecedentes')
    tratamientos_pendientes = fields.Text(string='Tratamientos pendientes')
    participacion_otro_programa_provincial = fields.Boolean('Participación en otro programa provincial')
    otro_programa_provincial = fields.Many2many('po_pac.programa_provincial', string="Otros programas provinciales")
    #Situación familiar
    composicion_familiar = fields.Selection(string='Composición familiar', selection=[
        ('Si', 'Si'),
        ('No', 'No')
    ])
    cantidad_hijos = fields.Integer(string='Cantidad de hijos')
    tipo_vinculo_familiar = fields.Selection(string='Tipo de vinculo familiar', selection=[
        ('Claro', 'Claro'),
        ('Débil', 'Débil'),
        ('Conflictivo', 'Conflictivo'),
        ('Aglutinado', 'Aglutinado'),
    ])

    #Situación económica
    descripcion_situacion_economica = fields.Text(string='Descripción situación económica')

    # Situación habitacional
    tipo_vivienda = fields.Selection(string='Tipo de vivienda', selection=[
        ('Propia', 'Propia'),
        ('En alquiler', 'En alquiler'),
        ('En usufructo', 'En usufructo'),
        ('Prestada', 'Prestada'),
        ('Otro', 'Otro'),
    ])
    cantidad_habitaciones_vivienda = fields.Integer(string='Cantidad de habitaciones de vivienda')
    tipo_construccion_vivienda = fields.Selection(string='Tipo de construcción de vivienda', selection=[
        ('De material', 'De material'),
        ('De adobe', 'De adobe'),
        ('De madera', 'De madera'),
        ('De chapa', 'De chapa'),
        ('Otro', 'Otro'),
    ])
    servicios_basicos_vivienda = fields.Selection(string='Servicios básicos de vivienda', selection=[
        ('Si', 'Si'),
        ('No', 'No')
    ])
    tipo_ubicacion_vivienda = fields.Selection(string='Tipo de ubicación de vivienda', selection=[
        ('Rural', 'Rural'),
        ('Semi Rural', 'Semi Rural'),
        ('Urbana', 'Urbana'),
    ])
    banio_vivienda = fields.Selection(string='Baño de vivienda', selection=[
        ('Si', 'Si'),
        ('No', 'No')
    ])

    #Diagnóstico social
    descripcion_diagnostico_social = fields.Text(string='Descripción diagnóstico social')

    #Campos del paciente
    paciente_tipo_documento = fields.Selection(related='paciente_id.tipo_documento', readonly=False)
    paciente_numero_documento = fields.Integer(related='paciente_id.numero_documento', readonly=False)
    paciente_fuente_paciente_ids = fields.One2many(related='paciente_id.fuente_paciente_ids')
    paciente_diagnostico_paciente_ids = fields.One2many(related='paciente_id.diagnostico_paciente_ids', string='Diagnósticos CIE10')
    paciente_cuil_cuit = fields.Char(related='paciente_id.cuil_cuit', readonly=False)
    paciente_fecha_nacimiento = fields.Date(related='paciente_id.fecha_nacimiento', readonly=False)
    paciente_edad = fields.Integer(related='paciente_id.edad')
    paciente_country_id_nacimiento = fields.Many2one(related='paciente_id.country_id_nacimiento', readonly=False)
    paciente_state_id_nacimiento = fields.Many2one(related='paciente_id.state_id_nacimiento', readonly=False, domain="[('country_id', '=?', paciente_country_id_nacimiento)]")
    paciente_tipo_residencia = fields.Selection(related='paciente_id.tipo_residencia', readonly=False)
    paciente_zip = fields.Char(related='paciente_id.zip', readonly=False)
    paciente_country_id = fields.Many2one(related='paciente_id.country_id', readonly=False)
    paciente_state_id = fields.Many2one(related='paciente_id.state_id', readonly=False, domain="[('country_id', '=?', paciente_country_id)]")
    paciente_departamento_id = fields.Many2one(related='paciente_id.departamento_id', readonly=False, domain="[('state_id', '=?', paciente_state_id)]")
    paciente_localidad_id = fields.Many2one(related='paciente_id.localidad_id', readonly=False, domain="[('departamento_id', '=?', paciente_departamento_id)]")
    paciente_direccion = fields.Char(related='paciente_id.direccion', readonly=False)
    paciente_estado_civil = fields.Selection(related='paciente_id.estado_civil', readonly=False)
    paciente_obra_social_id = fields.Many2one(related='paciente_id.obra_social_id', readonly=False)
    paciente_mobile = fields.Char(related='paciente_id.mobile', readonly=False)
    paciente_profesion_id = fields.Many2one(related='paciente_id.profesion_id', readonly=False)

    def pasar_a_pendiente_revision(self):
        if self.estado == 'Borrador':
            self.estado = 'Pendiente de revisión'

    def pasar_a_borrador(self):
        if self.estado == 'Pendiente de revisión':
            self.estado = 'Borrador'

    def pasar_a_aprobado(self):
        if self.estado == 'Pendiente de revisión':
            self.write({
                'estado': 'Aprobado',
                'user_id_aprobador': self.env.uid,
                'fecha_aprobacion': datetime.now()
            })

    def pasar_a_rechazado(self, motivo_rechazo):
        if self.estado == 'Pendiente de revisión':
            self.write({
                'estado': 'Rechazado',
                'user_id_rechazador': self.env.uid,
                'fecha_rechazo': datetime.now(),
                'motivo_rechazo': motivo_rechazo
            })

            self.paciente_id.estado = 'Rechazado'


class RechazarInformeSocial(models.TransientModel):
    _name = 'po_pac.rechazar_informe_social'
    _description = 'Rechazar informe social'

    motivo_rechazo = fields.Text(string='Motivo de rechazo', required=True)

    def guardar_y_cerrar(self):
        informe_social = self.env['po_pac.informe_social'].search([('id', '=', self._context.get('active_id'))])
        if informe_social:
            informe_social.pasar_a_rechazado(self.motivo_rechazo)

        return {'type': 'ir.actions.act_window_close'}

