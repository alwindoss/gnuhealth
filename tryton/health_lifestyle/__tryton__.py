# -*- encoding: utf-8 -*-
{
    'name': 'GNU Health: Lifestyle',
    'version': '1.4.3',
    'author': 'GNU Solidario',
    'email': 'health@gnusolidario.org',
    'website': 'http://health.gnu.org',
    'depends': [
        'health',
    ],
    'name_es_ES': 'GNU Health : Estilos de vida',
    'translation': [
        'locale/es_ES.po',
    ],

    'description': '''

Gathers information about the habits and sexuality of the patient

- Eating habits and diets
- Sleep patterns
- Recreational drugs database from NIDA
- Henningfield drug ratings
- Drug / alcohol addictions
- Physical activity (workout / excercise )
- Sexuality and sexual behaviour
- Home and child safety




''',
    'description_es_ES': '''
Guarda información de los hábitos y sexualidad del paciente

- Dietas y hábitos alimenticios
- Ejercicio físico
- Adicciones
- Drogras recreacionales (Base de datos de NIDA)
- Score de Henningfield de drogas
- Patrones del sueño
- Sexualidad y hábitos sexuales
- Seguridad en el hogar y vial

''',



    'xml': [
        'health_lifestyle_view.xml',
        'data/recreational_drugs.xml',
        'security/access_rights.xml'
    ],
    'active': False,
}
