# -*- encoding: utf-8 -*-
{

	'name' : 'GNU Health: International Classification of Diseases .- ICD-10',  
    'version': '1.4.0',
	'author' : 'GNU Solidario',
	"website" : "http://health.gnu.org",
	'email' : 'health@gnusolidario.org',
	'depends' : ['health'],
    'name_es_ES': 'GNU Health : Clasificación Internacional de Enfermedades .- CIE-10',
	'description' : '''
World Health Organization - International Classification of Diseases for GNU HEALTH - 10th revision
''',

	'description_es_ES' : '''
Organización Mundial de la Salud - Clasificación Internacional de Enfermedades - Revisión 10' 
''',
	"xml" : ["data/disease_categories.xml","data/diseases.xml"],
# Uncomment the following line and comment the previous one to enable Spanish CIE-10
#	"xml" : ["data/disease_categories_es.xml","data/diseases_es.xml"],
	"active": False 
}
