#!/usr/bin/env python

import sys, os
DIR = os.path.abspath(os.path.normpath(os.path.join(__file__,
    '..', '..', '..', '..', '..', 'trytond')))
if os.path.isdir(DIR):
    sys.path.insert(0, os.path.dirname(DIR))

import unittest
import trytond.tests.test_tryton
from trytond.tests.test_tryton import test_view


class MedicalGeneticsTestCase(unittest.TestCase):
    '''
    Test MedicalGenetics module.
    '''

    def setUp(self):
        trytond.tests.test_tryton.install_module('health_genetics')

    def test0005views(self):
        '''
        Test views.
        '''
        test_view('health_genetics')

def suite():
    suite = trytond.tests.test_tryton.suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
        MedicalGeneticsTestCase))
    return suite

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())
