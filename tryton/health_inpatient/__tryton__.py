# -*- encoding: utf-8 -*-
{
    'name': 'GNU Health: Inpatient administration',
    'version': '1.4.3',
    'author': 'GNU Solidario',
    'email': 'health@gnusolidario.org',
    'website': 'http://health.gnu.org',
    'depends': [
        'health',
    ],
    'name_es_ES': 'GNU Health : Hospitalización',
    'translation': [
        'locale/es_ES.po',
    ],

    'description': '''
This module will hold all the processes related to Inpatient (Patient hospitalization and bed assignment )

- Patient Registration
- Bed reservation
- Hospitalization
- Nursing Plan
- Discharge Plan
- Reporting

''',

    'description_es_ES': '''
Contiene los procesos relacionados a la internación (Hospitalización y asignación de camas )

- Registro del paciente
- Reserva de camas
- Hospitalización
- Plan de enfermería
- Plan para después del alta
- Reportes

''',

    'xml': [
        'health_inpatient_view.xml','data/health_inpatient_sequence.xml',
        'security/access_rights.xml'
    ],
    'active': False,
}
