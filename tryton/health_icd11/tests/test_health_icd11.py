import unittest
import trytond.tests.test_tryton
from trytond.tests.test_tryton import ModuleTestCase


class HealthICD11TestCase(ModuleTestCase):
    '''
    Test Health ICD11 package.
    '''
    module = 'health_icd11'


def suite():
    suite = trytond.tests.test_tryton.suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
        HealthICD11TestCase))
    return suite
