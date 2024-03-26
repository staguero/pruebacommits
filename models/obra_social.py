from odoo import api, fields, models
from odoo.exceptions import ValidationError


class ObraSocial(models.Model):
    _name = 'po_pac.obra_social'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _descripcion = 'Obra social'

    name = fields.Char(string='Nombre', required=True, tracking=True)
    active = fields.Boolean(string='Activo', default=True, tracking=True)
    suspende_adhesion = fields.Boolean(string='Suspende o rechaza adhesión', default=True)