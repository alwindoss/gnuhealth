# SPDX-FileCopyrightText: 2009-2013 Bertrand Chenal
# SPDX-FileCopyrightText: 2009-2016 B2CK
# SPDX-FileCopyrightText: 2009-2016 Cédric Krier
# SPDX-FileCopyrightText: 2016-2022 Luis Falcon <falcon@gnuhealth.org>
#
# SPDX-License-Identifier: GPL-3.0-or-later

import unittest
import trytond.tests.test_tryton
from trytond.tests.test_tryton import ModuleTestCase


class CalendarTestCase(ModuleTestCase):
    'Test Calendar module'
    module = 'health_caldav'


def suite():
    suite = trytond.tests.test_tryton.suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
        CalendarTestCase))
    return suite
