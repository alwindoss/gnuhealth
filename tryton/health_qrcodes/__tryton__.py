# -*- encoding: utf-8 -*-
{

	'name' : 'GNU Health - QR Codes : Add QR code identification',  
    'version': '1.4.3',
	'author' : 'GNU Solidario',
	'email' : 'health@gnusolidario.org',
	'website' : "http://health.gnu.org",
    'depends' : ['health', 'health_pediatrics'],
    'name_es_ES': 'GNU Health - QR Codes: Integra Identificación QR (Quick Recognition) ',
    'translation': [
        'locale/es_ES.po',
    ],

	"xml" : ["health_qrcodes_view.xml","health_qrcodes_report.xml"],

	'description' : """
This module adds QR (Quick Recognition) codes to GNU Health objects, like patient and newborns
"""


}
