# SPDX-FileCopyrightText: 2008-2022 Luis Falcón <falcon@gnuhealth.org>
# SPDX-FileCopyrightText: 2011-2022 GNU Solidario <health@gnusolidario.org>
#
# SPDX-License-Identifier: GPL-3.0-or-later
#########################################################################
#   Hospital Management Information System (HMIS) component of the      #
#                       GNU Health project                              #
#                   https://www.gnuhealth.org                           #
#########################################################################
#                         HEALTH QR_CODES PACKAGE                       #
#                  __init__.py: Package declaration file                #
#########################################################################

from trytond.pool import Pool
from .import health_qrcodes


def register():
    Pool.register(
        health_qrcodes.Patient,
        health_qrcodes.Appointment,
        health_qrcodes.Newborn,
        health_qrcodes.LabTest,
        module='health_qrcodes', type_='model')
