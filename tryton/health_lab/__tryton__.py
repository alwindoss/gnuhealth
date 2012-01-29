# -*- encoding: utf-8 -*-
{
    'name': 'GNU Health: Laboratory',
    'version': '1.4.3',
    'author': 'GNU Solidario',
    'email': 'health@gnusolidario.org',
    'website': 'http://health.gnu.org',
    'depends': [
        'health',
    ],

    'name_es_ES': 'GNU Health : Laboratorio',
    'translation': [
        'locale/es_ES.po',
    ],

    'description': '''

This modules includes lab tests: Values, reports and PoS.


''',

    'description_es_ES': '''

Módulo con la funcionalidad de laboratorio.

''',

    'xml': [
        'health_lab_view.xml',
        'health_lab_report.xml',
        'data/health_lab_sequences.xml',
        'data/lab_test_data.xml',
        'wizard/create_lab_test.xml',
        'security/access_rights.xml',
    ],
}
