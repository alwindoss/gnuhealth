# -*- encoding: utf-8 -*-
{

    'name' : 'GNU Health : Installer',  
    'version' : '1.0',
    'author' : 'GNU Solidario',
    'email' : 'health@gnusolidario.org',
    'website' : "http://health.gnu.org",
    'category' : 'Generic Modules/Others',
    'depends' : ['medical','medical_socioeconomics','medical_lifestyle',
		'medical_genetics','medical_icd10','medical_gyneco',
		'medical_pediatrics','medical_surgery','medical_lab',
        'medical_inpatient'],
    'name_es_ES': 'GNU Health : Perfil de Instalación estándar',
   
    'description' : """


Profile for Main Modules.
- Core
- Socioeconomics
- Lifestyle
- Genetics
- Surgery
- Laboratory
- Pediatrics
- ICD-10 Coding
- Gynecology and Obstetrics
- Inpatient

We don't include in the main installation the following modules :
- ICD-10-PCS (Surgical Procedures)
- Invoicing (Billing)

You can install these two manually.


""",

    'description_es_ES': 
'''
Perfil de Instalación de la functionalidad estándar

- Núcleo
- Socioeconomía
- Estilos de vida
- Genetica
- Cirugía
- Laboratorio
- Pediatría 
- ICD-10 
- Ginecología y Obstetricia
- Hospitalización

Los módulos :

- ICD-10-PCS (Procedimientos quirúrgicos
- Facturación (Billing)

No están en el perfil de instalación estándar, pero sí en el sistema.
Si lo desea, los puede instalar a posteriori.
''',

    'xml': [],
    "active": False 
}
