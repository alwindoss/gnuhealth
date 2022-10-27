# SPDX-FileCopyrightText: 2012-2017 Cédric Krier
# SPDX-FileCopyrightText: 2017-2022 GNU Solidario <health@gnusolidario.org>
# SPDX-FileCopyrightText: 2017-2022 Luis Falcon <falcon@gnuhealth.org>
#
# SPDX-License-Identifier: GPL-3.0-or-later

# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.
import unittest
import trytond.tests.test_tryton
from trytond.tests.test_tryton import ModuleTestCase


class WebdavTestCase(ModuleTestCase):
    'Test Webdav module'
    module = 'webdav'


def suite():
    suite = trytond.tests.test_tryton.suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
            WebdavTestCase))
    return suite
