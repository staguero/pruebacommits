# -*- coding: utf-8 -*-
{
    'name': "Programa Oncológico - Pacientes",
    'summary': 'Módulo de pacientes para Programa oncológico',
    'author': "Hexium Software Factory",
    'website': "https://hexium.com.ar",
    'category': 'Uncategorized',
    'version': '1.0',
    'installable': True,
    'application': True,


    # any module necessary for this one to work correctly
    'depends': ['base', 'contacts'],

    # always loaded
    'data': [
        'data/ir.module.category.csv',
        'data/ir_cron_data.xml',
        'security/res.groups.xml',
        'security/ir.model.access.csv',
        'views/paciente_views.xml',
        'views/obra_social_views.xml',
        'views/profesional_medico_views.xml',
        'views/especialidad_medica_views.xml',
        'views/documentacion_views.xml',
        'views/diagnostico_cie_10_views.xml',
        'views/diagnostico_paciente_views.xml',
        'views/fuente_paciente_views.xml',
        'views/hospital_views.xml',
        'views/informe_social_views.xml',
        'views/menu.xml',
    ],
}





