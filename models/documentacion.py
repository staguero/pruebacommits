from odoo import api, fields, models
from odoo.exceptions import ValidationError
from datetime import datetime
import pytz
import base64

class Documentacion(models.Model):
    _name = "po_pac.documentacion"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Documentación'
    _rec_name = 'tipo_documentacion_id'

    tipo_documentacion_id = fields.Many2one('po_pac.tipo_documentacion', string='Tipo', required=True, tracking=True)
    fecha_vencimiento = fields.Date(string='Fecha de vencimiento', tracking=True)
    archivo_adjunto = fields.Binary(string="Documento Adjunto", attachment=True)
    archivo_adjunto_nombre = fields.Char(string="Nombre adjunto")
    observaciones = fields.Text(string="Observaciones")
    active = fields.Boolean(string='Activo', default=True)
    link_archivo = fields.Char(string='Link de archivo')

    paciente_id = fields.Many2one('po_pac.paciente', string='Paciente')

    @api.model
    def create(self, vals_list):
        documentacion_creada = super(Documentacion, self).create(vals_list)
        documentacion_creada.publicar_archivo_como_nota()

        if not documentacion_creada.archivo_adjunto and not documentacion_creada.link_archivo:
            raise ValidationError('Debe cargar el archivo como adjunto o como link.')

        return documentacion_creada

    def write(self, vals):
        super(Documentacion, self).write(vals)
        self.publicar_archivo_como_nota()

        if not self.archivo_adjunto and not self.link_archivo:
            raise ValidationError('Debe cargar el archivo como adjunto o como link.')

        return

    def publicar_archivo_como_nota(self):
        # Adjunta el archivo y lo pone como una nota para que quede el historial
        contenido_nota = 'Se agregó un nuevo archivo adjunto'
        if self.link_archivo:
            contenido_nota += ' - Link: ' + self.link_archivo
        nota_publicada = self.message_post(body=contenido_nota)
        nota_publicada.date = datetime.now(pytz.timezone('utc')).strftime("%Y-%m-%d %H:%M:%S")

        if self.archivo_adjunto:
            adjunto = self.env['ir.attachment'].create({
                'name': self.archivo_adjunto_nombre,
                'datas': self.archivo_adjunto,
            })

            nota_publicada.attachment_ids = [[6, False, [adjunto.id]]]



class TipoDocumentacion(models.Model):
    _name = "po_pac.tipo_documentacion"
    _description = 'Tipo de documentación'

    name = fields.Char(string='Nombre', required=True)
    active = fields.Boolean(string='Activo', default=True)