# -*- encoding: utf-8 -*-
{
    'name': 'GNU Health - QR Codes : Add QR code identification',
    'name_es_ES': 'GNU Health - QR Codes: Integra Identificación QR (Quick Recognition)',
    'version': '1.4.4',
    'author': 'GNU Solidario',
    'email': 'health@gnusolidario.org',
    'website': 'http://health.gnu.org/',
    'description': '''
This module adds QR (Quick Recognition) codes to GNU Health objects, like patient and newborns
''',
    'depends': [
        'health',
        'health_pediatrics',
    ],
    'xml': [
        'health_qrcodes_view.xml',
        'health_qrcodes_report.xml',
    ],
    'translation': [
        'locale/es_ES.po', 'locale/it.po'
    ],
}
