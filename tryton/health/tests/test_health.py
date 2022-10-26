# SPDX-FileCopyrightText: 2008-2022 Luis Falcón <falcon@gnuhealth.org>
# SPDX-FileCopyrightText: 2011-2022 GNU Solidario <health@gnusolidario.org>
#
# SPDX-License-Identifier: GPL-3.0-or-later

#########################################################################
#   Hospital Management Information System (HMIS) component of the      #
#                       GNU Health project                              #
#                   https://www.gnuhealth.org                           #
#########################################################################
#                           HEALTH package                              #
#                test_health.py health unittest file                    #
#########################################################################
import unittest
import trytond.tests.test_tryton
from trytond.tests.test_tryton import ModuleTestCase


class HealthTestCase(ModuleTestCase):
    '''
    Test Health module.
    '''
    module = 'health'


def suite():
    suite = trytond.tests.test_tryton.suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
        HealthTestCase))
    return suite
