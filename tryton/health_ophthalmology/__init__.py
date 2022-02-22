from trytond.pool import Pool
from . import health_ophthalmology

def register():
    Pool.register(
        health_ophthalmology.OphthalmologyEvaluation,
        health_ophthalmology.OphthalmologyFindings,    
        module='health_ophthalmology', type_='model')
