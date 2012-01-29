# -*- encoding: utf-8 -*-
{
    'name': 'GNU Health: Pediatrics',
    'version': '1.4.3',
    'author': 'GNU Solidario',
    'email': 'health@gnusolidario.org',
    'website': 'http://health.gnu.org',
    'depends': [
        'health',
    ],

    'name_es_ES': 'GNU Health : Pediatría',
    'translation': [
        'locale/es_ES.po',
    ],

    'description': '''
	
	This module takes has the functionality for pediatric patients :
	
	- Neonatal : from birth to 1 week .
	- Infancy : 1 week to 1 year
	- Toddler and early childhood : 1 to 5 years of age
	- Late childhood : 6 to 12 years of age
	
	This module focuses on the basic pediatric evaluation, making emphasis in the nutritional, growth and development of the infant and child.
''',

    'description_es_ES': '''

Cubre la funcionalidad principal para pacientes pediátricos :

- Neonatología ( desde el nacimiento a 1 semana de vida )
- Infancia : 1 semana a 1 año
- Comienza a Gatear and niñez temprana : 1 a 5 años
- Niñez : 6 a 12 años

Nos focalizamos en la evaluación pediátrica básica, haciendo énfasis en el desarrollo nutricional y crecimiento del niño.

''',
    'xml': [
        'health_pediatrics_view.xml',
        'health_pediatrics_report.xml',
        'security/access_rights.xml'
    ],
    'active': False,
}
