# -*- encoding: utf-8 -*-
{
    'name': 'GNU Health: Surgery',
    'version': '1.4.3',
    'author': 'GNU Solidario',
    'email': 'health@gnusolidario.org',
    'website': 'http://health.gnu.org',
    'depends': [
        'health',
    ],
    'name_es_ES': 'GNU Health : Cirugía',
    'translation': [
        'locale/es_ES.po',
    ],

    'description': '''

Basic Surgery Module for GNU Health

If you want to include standard codings for procedures, please install 
corresponding module, like ICD10-PCS

''',

    'description_es_ES': '''
Módulo básico que cirugía para GNU Health

Si quiere incluir códigos de procedimientos, por favor instale algún módulo
con la funcionalidad específica, como gnuhealth_ICD10-PCS
''',

    'xml': [
        'health_surgery_view.xml',
        'security/access_rights.xml'
    ],
    'active': False,
}
