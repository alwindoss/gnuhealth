# -*- encoding: utf-8 -*-
{
    'name': 'GNU Health: Gynecology and Obstetrics',  
    'version': '1.4.3',
    'author': 'GNU Solidario',
    'email': 'health@gnusolidario.org',
    'website': 'http://health.gnu.org',
    'depends': [
        'health',
    ],
    'name_es_ES': 'GNU Health : Ginecología y Obstetricia',
    'translation': [
        'locale/es_ES.po',
    ],

    'description': '''

This module includes :

- Gynecological Information
- Obstetric information 
- Perinatal Information and monitoring
- Puerperium


''',
    'description_es_ES': '''

Este módulo incluye :

- Información ginecológica
- Información Obstétrica
- Monitor e información perinatal
- Puerperio

''',

    'xml': [
        'health_gyneco_view.xml','security/access_rights.xml'
    ],
    'active': False,
}
