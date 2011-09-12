#!/usr/bin/env python

import sys, os
DIR = os.path.abspath(os.path.normpath(os.path.join(__file__,
    '..', '..', '..', '..', '..', 'trytond')))
if os.path.isdir(DIR):
    sys.path.insert(0, os.path.dirname(DIR))

import unittest
import trytond.tests.test_tryton
from trytond.tests.test_tryton import test_view


class MedicalLifestyleTestCase(unittest.TestCase):
    '''
    Test MedicalLifestyle module.
    '''

    def setUp(self):
        trytond.tests.test_tryton.install_module('medical_lifestyle')

    def test0005views(self):
        '''
        Test views.
        '''
        test_view('medical_lifestyle')

def suite():
    suite = trytond.tests.test_tryton.suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
        MedicalLifestyleTestCase))
    return suite

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())
