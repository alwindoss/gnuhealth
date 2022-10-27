import unittest
import trytond.tests.test_tryton
from trytond.tests.test_tryton import ModuleTestCase


class HealthServicesImagingTestCase(ModuleTestCase):
    '''
    Test Health Services module.
    '''
    module = 'health_services_imaging'


def suite():
    suite = trytond.tests.test_tryton.suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
        HealthServicesImagingTestCase))
    return suite
