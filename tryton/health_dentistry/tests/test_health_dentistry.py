import unittest
import trytond.tests.test_tryton
from trytond.tests.test_tryton import ModuleTestCase


class HealthDentistryTestCase(ModuleTestCase):
    '''
    Test Health Dentistry module.
    '''
    module = 'health_dentistry'


def suite():
    suite = trytond.tests.test_tryton.suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
        HealthDentistryTestCase))
    return suite
