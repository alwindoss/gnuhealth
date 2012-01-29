# -*- encoding: utf-8 -*-
{
    'name': 'GNU Health : Genetics',
    'version': '1.4.3',
    'author': 'GNU Solidario',
    'email': 'health@gnusolidario.org',
    'website': 'http://health.gnu.org',
    'category': 'Generic Modules/Others',
    'depends': [
        'health',
    ],
    'name_es_ES': 'GNU Health : Genética',
    'translation': [
        'locale/es_ES.po',
    ],
    
    'description': '''

Family history and genetic risks

The module includes hereditary risks, family history and genetic disorders.

In this module we include the NCBI and GeneCards information, more than 4200 genes associated to diseases


''',
    'description_es_ES': '''

Riesgos genéticos e historial familiar
Family history and genetic risks
Incluye desórdenes genéticos y genes patológicos ("disease genes"), con una base de más de 4200 de la NCBI y GeneCards.

''',

    'xml': [
        'health_genetics_view.xml',
        'data/disease_genes.xml','security/access_rights.xml'
    ],
    'active': False,
}
