# SPDX-FileCopyrightText: 2008-2022 Luis Falcón <falcon@gnuhealth.org>
# SPDX-FileCopyrightText: 2011-2022 GNU Solidario <health@gnusolidario.org>
#
# SPDX-License-Identifier: GPL-3.0-or-later
#########################################################################
#   Hospital Management Information System (HMIS) component of the      #
#                       GNU Health project                              #
#                   https://www.gnuhealth.org                           #
#########################################################################
#                      HEALTH SERVICES LAB package                      #
#                 __init__.py: Package declaration file                 #
#########################################################################

from trytond.pool import Pool
from . import health_services_lab
from . import wizard


def register():
    Pool.register(
        health_services_lab.PatientLabTestRequest,
        wizard.wizard_health_services.RequestPatientLabTestStart,
        module='health_services_lab', type_='model')
    Pool.register(
        wizard.wizard_health_services.RequestPatientLabTest,
        module='health_services_lab', type_='wizard')
