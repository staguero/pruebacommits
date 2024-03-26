from odoo import api, fields, models
from odoo.exceptions import ValidationError

from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta

class Paciente(models.Model):
    _name = 'po_pac.paciente'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _inherits = {"res.partner": "partner_id"}
    _descripcion = 'Paciente'
    _order = 'apellido'

    partner_id = fields.Many2one('res.partner', string='Contacto')
    #@TODO crear un formulario de cambio de estado para no hacerlo desde la barra de estado. Este formulario debe pedir el nuevo estado y observaciones
    estado = fields.Selection(string='Estado', selection=[
        ('Pendiente', 'Pendiente'),
        ('Urgencia', 'Urgencia'),
        ('Activo', 'Activo'),
        ('Suspendido', 'Suspendido'),
        ('Rechazado', 'Rechazado'),
        ('Fallecido', 'Fallecido'),
    ], default='Pendiente', tracking=True)
    es_urgencia = fields.Boolean(string='Es urgencia')
    motivo_urgencia = fields.Char(string='Motivo de urgencia')
    observaciones_cambio_estado = fields.Char(string='Observaciones de cambio de estado')
    nombre = fields.Char(string='Nombre de pila', required=True)
    apellido = fields.Char(string='Apellido', required=True)
    tipo_documento = fields.Selection(string="Tipo documento", selection=[
        ('DNI', 'DNI'),
        ('LE', 'LE'),
        ('LC', 'LC'),
        ('CE', 'CE'),
        ('PAS', 'PAS'),
        ('CI', 'CI')
    ], required=True, tracking=True)
    numero_documento = fields.Integer(string='Número documento', required=True, default='', tracking=True)
    cuil_cuit = fields.Char(string='CUIL/CUIT')
    fecha_nacimiento = fields.Date(string='Fecha de nacimiento', tracking=True)
    edad = fields.Integer(string='Edad', compute='compute_edad', store=True)
    sexo_biologico = fields.Selection(string="Sexo biológico", selection=[('Femenino', 'Femenino'), ('Masculino', 'Masculino')])
    sexo_civil = fields.Selection(string="Sexo civil", selection=[
        ('Femenino', 'Femenino'),
        ('Masculino', 'Masculino'),
        ('No binario', 'No binario'),
        ('No especificado', 'No especificado'),
        ('Otro', 'Otro')
    ], tracking=True)
    estado_civil = fields.Selection(string="Estado civil", selection=[
        ('Soltero/a', 'Soltero/a'),
        ('Casado/a', 'Casado/a'),
        ('Viudo/a', 'Viudo/a'),
        ('Separado/a', 'Separado/a'),
        ('Divorciado/a', 'Divorciado/a'),
        ('No especificado', 'No especificado')
    ], tracking=True)
    fecha_obito = fields.Date(string='Fecha de óbito', tracking=True)
    profesion_id = fields.Many2one('po_pac.profesion', string='Profesión')

    #Obra social
    obra_social_id = fields.Many2one('po_pac.obra_social', string='Obra social')
    obra_social_nro_afiliado = fields.Char(string='N° de afiliado')
    obra_social_observaciones = fields.Char(string='Obra social - Observaciones')

    #Dirección
    zip = fields.Char(string='Código postal')
    state_id = fields.Many2one("res.country.state", string='Provincia', ondelete='restrict', domain="[('country_id', '=?', country_id)]")
    departamento_id = fields.Many2one("po_pac.departamento", string='Departamento', domain="[('state_id', '=?', state_id)]")
    localidad_id = fields.Many2one("po_pac.localidad", string='Localidad', domain="[('departamento_id', '=?', departamento_id)]")
    direccion = fields.Char('Dirección')

    #Dirección de residencia
    misma_direccion_residencia = fields.Boolean('Misma dirección de residencia')
    zip_residencia = fields.Char(string='Código postal de residencia')
    country_id_residencia = fields.Many2one("res.country", string='País de residencia')
    state_id_residencia = fields.Many2one("res.country.state", string='Provincia de residencia', ondelete='restrict', domain="[('country_id', '=?', country_id_residencia)]")
    departamento_id_residencia = fields.Many2one("po_pac.departamento", string='Departamento de residencia', domain="[('state_id', '=?', state_id_residencia)]")
    localidad_id_residencia = fields.Many2one("po_pac.localidad", string='Localidad de residencia', domain="[('departamento_id', '=?', departamento_id_residencia)]")
    direccion_residencia = fields.Char('Dirección de residencia')

    #Nacimiento
    country_id_nacimiento = fields.Many2one("res.country", string='País de nacimiento')
    state_id_nacimiento = fields.Many2one("res.country.state", string='Provincia de nacimiento', ondelete='restrict', domain="[('country_id', '=?', country_id_nacimiento)]")
    tipo_residencia = fields.Selection(string="Tipo de residencia", selection=[
        ('Argentino naturalizado', 'Argentino naturalizado'),
        ('Residente precario', 'Residente precario'),
        ('Residente con DNI', 'Residente con DNI')
    ])

    documentacion_ids = fields.One2many('po_pac.documentacion', 'paciente_id', string='Documentación')
    informe_social_ids = fields.One2many('po_pac.informe_social', 'paciente_id', string='Informes sociales')
    familiar_paciente_ids = fields.One2many('po_pac.familiar_paciente', 'paciente_id', string='Familiares')
    historial_estado_paciente_ids = fields.One2many('po_pac.historial_estado_paciente', 'paciente_id', string='Historial de estados')
    diagnostico_paciente_ids = fields.One2many('po_pac.diagnostico_paciente', 'paciente_id', string='Diagnósticos')
    fuente_paciente_ids = fields.One2many('po_pac.fuente_paciente', 'paciente_id', string='Fuentes')
    trayectoria_sistema_salud_ids = fields.One2many('po_pac.trayectoria_sistema_salud', 'paciente_id', string='Trayectoria en sistema de salud')

    def create(self, vals):
        # Si es urgencia lo cambia a estado Urgencia
        if vals.get('es_urgencia'):
            vals['estado'] = 'Urgencia'

        paciente = super(Paciente, self).create(vals)

        paciente.validar_tipo_residencia()

        #Guarda historial de estado
        paciente.set_historial_estado()

        paciente.set_estado_paciente_segun_obra_social()

        return paciente

    def write(self, vals):
        res = super(Paciente, self).write(vals)

        # self.validar_tipo_residencia()

        #Guarda historial de estado
        if vals.get('estado'):
            self.set_historial_estado(vals.get('observaciones_cambio_estado'))

        if vals.get('obra_social_id'):
            self.set_estado_paciente_segun_obra_social()

        return res

    def set_historial_estado(self, observaciones=False):
        for paciente in self:
            #Busca el último historial de estado y en caso de que no tenga fecha hasta se la establece
            estado_anterior = self.env['po_pac.historial_estado_paciente'].search([('paciente_id', '=', paciente.id)], order='fecha_desde desc', limit=1)
            if estado_anterior:
                estado_anterior.fecha_hasta = datetime.now()
            #Crea el nuevo historial
            self.env['po_pac.historial_estado_paciente'].create({
                'paciente_id': paciente.id,
                'estado': paciente.estado,
                'fecha_desde': datetime.now(),
                'observaciones': observaciones if observaciones else '',
                'user_id': self.env.uid,
            })

    #Cambia el estado del paciente a rechazado o suspendido si la obra social tiene marcado el check de suspende adhesion
    def set_estado_paciente_segun_obra_social(self):
        for paciente in self:
            if paciente.obra_social_id.suspende_adhesion:
                contenido_nota = False
                if paciente.estado == 'Pendiente':
                    paciente.write({
                        'estado': 'Rechazado',
                        'observaciones_cambio_estado': 'Cambio de estado automático a Rechazado por obra social ' + paciente.obra_social_id.name
                    })
                    contenido_nota = 'Se realizó un cambio de estado automático a Rechazado debido a que el paciente tiene obra social ' + paciente.obra_social_id.name

                elif paciente.estado == 'Activo':
                    paciente.write({
                        'estado': 'Suspendido',
                        'observaciones_cambio_estado': 'Cambio de estado automático a Suspendido por obra social ' + paciente.obra_social_id.name
                    })
                    contenido_nota = 'Se realizó un cambio de estado automático a Suspendido debido a que el paciente tiene obra social ' + paciente.obra_social_id.name

                if contenido_nota:
                    paciente.message_post(body=contenido_nota)


    @api.onchange('nombre', 'apellido')
    def set_full_name(self):
        for paciente in self:
            if paciente.apellido:
                paciente.apellido = paciente.apellido
            if paciente.nombre and paciente.apellido:
                paciente.name = paciente.nombre + ' ' + paciente.apellido
            else:
                paciente.name = ''

    def validar_tipo_residencia(self):
        #Si el pais de nacimiento NO es Argentina, se pide como obligatorio el tipo de residencia
        for paciente in self:
            if paciente.country_id_nacimiento and paciente.country_id_nacimiento.code != 'AR' and not paciente.tipo_residencia:
                raise ValidationError('Si el país de nacimiento es distinto de Argentina se debe ingresar el tipo de residencia.')

    #@TODO crear acción planificada para recalcular las edades a medida que pasa el tiempo
    @api.depends('fecha_nacimiento')
    def compute_edad(self):
        for paciente in self:
            if paciente.fecha_nacimiento:
                diferencia = relativedelta(date.today(), paciente.fecha_nacimiento)
                paciente.edad = int(diferencia.years)
            else:
                paciente.edad = 0

    #Cuando establece el código postal, busca una localidad con ese codigo y en caso de encontrarla setea País, Provincia, Dpto y Localidad
    @api.onchange('zip')
    def set_direccion_from_zip(self):
        for rec in self:
            if rec.zip:
                localidad = self.env['po_pac.localidad'].search([('codigo_postal', '=', rec.zip)], limit=1)
                if localidad:
                    rec.localidad_id = localidad.id
                    rec.departamento_id = localidad.departamento_id.id
                    rec.state_id = localidad.departamento_id.state_id.id
                    rec.country_id = localidad.departamento_id.state_id.country_id

    #Cuando establece el código postal de residencia, busca una localidad con ese codigo y en caso de encontrarla setea País, Provincia, Dpto y Localidad (de residencia)
    @api.onchange('zip_residencia')
    def set_direccion_residencia_from_zip(self):
        for rec in self:
            if rec.zip_residencia:
                localidad = self.env['po_pac.localidad'].search([('codigo_postal', '=', rec.zip_residencia)], limit=1)
                if localidad:
                    rec.localidad_id_residencia = localidad.id
                    rec.departamento_id_residencia = localidad.departamento_id.id
                    rec.state_id_residencia = localidad.departamento_id.state_id.id
                    rec.country_id_residencia = localidad.departamento_id.state_id.country_id

    #En caso de marcar el check "misma_direccion_residencia" completa la dirección de residencia copiando los datos de la dirección
    @api.onchange('misma_direccion_residencia')
    def set_direccion_residencia_from_direccion(self):
        for rec in self:
            if rec.misma_direccion_residencia:
                rec.direccion_residencia = rec.direccion
                rec.zip_residencia = rec.zip
                rec.localidad_id_residencia = rec.localidad_id.id
                rec.departamento_id_residencia = rec.departamento_id.id
                rec.state_id_residencia = rec.state_id.id
                rec.country_id_residencia = rec.country_id.id
            else:
                rec.direccion_residencia = False
                rec.zip_residencia = False
                rec.localidad_id_residencia = False
                rec.departamento_id_residencia = False
                rec.state_id_residencia = False
                rec.country_id_residencia = False

    #Acción planificada que suspende a pacientes que lleven más de 30 días en estado Urgencia
    def suspender_pacientes_en_estado_urgencia(self):
        fecha_actual_menos_30_dias = datetime.now() - timedelta(days=30)
        historiales_estado_paciente_en_urgencia = self.env['po_pac.historial_estado_paciente'].search([
            ('paciente_id.estado', '=', 'Urgencia'),
            ('estado', '=', 'Urgencia'),
            ('fecha_desde', '<', fecha_actual_menos_30_dias),
            ('fecha_hasta', '=', False)
        ])

        for historial in historiales_estado_paciente_en_urgencia:
            historial.paciente_id.write({
                'estado': 'Urgencia',
                'es_urgencia': False
            })
            historial.paciente_id.message_post(body='Paciente suspendido automáticamente por llevar más de 30 días en estado Urgencia.')


class Localidad(models.Model):
    _name = "po_pac.localidad"
    _description = 'Localidad'

    name = fields.Char(string='Nombre', required=True)
    departamento_id = fields.Many2one("po_pac.departamento", string='Departamento')
    active = fields.Boolean(string='Activo', default=True)
    codigo_postal = fields.Char(string='CP')


class Departamento(models.Model):
    _name = "po_pac.departamento"
    _description = 'Departamento'

    name = fields.Char(string='Nombre', required=True)
    state_id = fields.Many2one("res.country.state", string='Provincia')
    active = fields.Boolean(string='Activo', default=True)

class Profesion(models.Model):
    _name = "po_pac.profesion"
    _description = 'Profesión'

    name = fields.Char(string='Nombre', required=True)
    active = fields.Boolean(string='Activo', default=True)

class ServicioSalud(models.Model):
    _name = "po_pac.servicio_salud"
    _description = 'Servicio de salud'

    name = fields.Char(string='Nombre', required=True)
    active = fields.Boolean(string='Activo', default=True)

class TrayectoriaSistemaSalud(models.Model):
    _name = "po_pac.trayectoria_sistema_salud"
    _description = 'Trayectoria en sistema de salud'

    paciente_id = fields.Many2one('po_pac.paciente', string='Paciente', required=True)
    atencion_primera_vez = fields.Selection(string='Atención por 1ra vez', selection=[
        ('Si', 'Si'),
        ('No', 'No')
    ], required=True)
    hospital_id = fields.Many2one('po_pac.hospital', string='Hospital', required=True)
    servicio_salud_id = fields.Many2one('po_pac.servicio_salud', string='Servicio', required=True)
    profesional_medico_id = fields.Many2one('po_pac.profesional_medico', string='Profesional médico', required=True)
    fecha_pedido_estudios = fields.Date(string='Fecha de pedido de estudios')
    fecha_estudios = fields.Date(string='Fecha de estudios')
    dificultad_obtener_turno = fields.Selection(string='Dificultad p/ obtener turno', selection=[
        ('Alta', 'Alta'),
        ('Media', 'Media'),
        ('Baja', 'Baja'),
    ])
    pedido_de_tratamiento = fields.Selection(string='Pedido de tratamiento', selection=[ ('Si', 'Si'), ('No', 'No') ], required=True)
    vulnerabilidad_social = fields.Selection(string='Vulnerabilidad social', selection=[ ('Alta', 'Alta'), ('Media', 'Media'), ('Baja', 'Baja') ], required=True)

