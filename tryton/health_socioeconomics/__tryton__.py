# -*- encoding: utf-8 -*-
{
    'name': 'GNU Health : Socioeconomics',
    'version': '1.4.3',
    'author': 'GNU Solidario',
    'email': 'health@gnusolidario.org',
    'website': 'http://health.gnu.org',
    'depends': [
        'health',
    ],
    'name_es_ES': 'GNU Health : Socioeconomía',
    'translation': [
        'locale/es_ES.po',
    ],
    
    'description': '''


This module takes care of the input of all the socio-economic factors that influence the health of the individual / family and society.

Among others, we include the following factors :

- Living conditions
- Educational level
- Infrastructure (electricity, sewers, ... )
- Family affection ( APGAR )
- Drug addiction 
- Hostile environment
- Teenage Pregnancy
- Working children


''',
    'description_es_ES': '''
Este módulo se encarge de ingresar y procesar los factores socio-económicos que influyen en la salud del individuo, su familia y sociedad.

Algunos aspectos que abarca :

- Condiciones de vida
- Nivel educativo
- Infraestructura (electricidad, gas, alcantarillas... )
- Afectividad familiar
- Trabajo Infantil
- Entornos hostiles
- Embarazos adolescentes
- Profesiones
- Violencia doméstica

''',

    'xml': [
        'health_socioeconomics_view.xml',
    ],
    'active': False,
}
