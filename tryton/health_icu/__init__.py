# SPDX-FileCopyrightText: 2020 Luis Falcón <falcon@gnuhealth.org>
# SPDX-FileCopyrightText: 2011-2022 GNU Solidario <health@gnusolidario.org>
#
# SPDX-License-Identifier: GPL-3.0-or-later
#########################################################################
#   Hospital Management Information System (HMIS) component of the      #
#                       GNU Health project                              #
#                   https://www.gnuhealth.org                           #
#########################################################################
#                         HEALTH ICU package                            #
#              __init__.py: Package declaration file                    #
#########################################################################

from trytond.pool import Pool
from . import health_icu


def register():
    Pool.register(
        health_icu.InpatientRegistration,
        health_icu.InpatientIcu,
        health_icu.Glasgow,
        health_icu.ApacheII,
        health_icu.MechanicalVentilation,
        health_icu.ChestDrainageAssessment,
        health_icu.PatientRounding,
        module='health_icu', type_='model')
