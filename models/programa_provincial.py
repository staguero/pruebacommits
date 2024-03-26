from odoo import api, fields, models
from odoo.exceptions import ValidationError


class ProgramaProvincial(models.Model):
    _name = 'po_pac.programa_provincial'
    _descripcion = 'Programa Provincial'
    name = fields.Char(string='Nombre del Programa', required=True, tracking=True)
    active = fields.Boolean(string='Activo', default=True, tracking=True)

    def create(self, vals):
        programa_provincial = super(ProgramaProvincial, self).create(vals)
        programa_provincial.validar_existencia()
        return programa_provincial

    def validar_existencia(self):
            #Si el registro ya existe no puede crearse otro con el mismo nombre
            for programa_provincial in self:
                if programa_provincial.name and self.search_count([('name', '=', programa_provincial.name)]) > 1:
                    raise ValidationError('Ya existe un programa provincial con el nombre ingresado.')