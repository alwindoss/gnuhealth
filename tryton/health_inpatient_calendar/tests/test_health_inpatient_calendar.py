# SPDX-FileCopyrightText: 2008-2022 Luis Falcón <falcon@gnuhealth.org>
# SPDX-FileCopyrightText: 2011-2022 GNU Solidario <health@gnusolidario.org>
#
# SPDX-License-Identifier: GPL-3.0-or-later

#########################################################################
#   Hospital Management Information System (HMIS) component of the      #
#                       GNU Health project                              #
#                   https://www.gnuhealth.org                           #
#########################################################################
#                HEALTH INPATIENT CALENDAR package                      #
#         test_health_inpatient_calendar.py main test module            #
#########################################################################
import unittest
import trytond.tests.test_tryton
from trytond.tests.test_tryton import ModuleTestCase


class HealthInpatientCalendarTestCase(ModuleTestCase):
    '''
    Test Health Inpatient Calendar module.
    '''
    module = 'health_inpatient_calendar'


def suite():
    suite = trytond.tests.test_tryton.suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
        HealthInpatientCalendarTestCase))
    return suite
