# SPDX-FileCopyrightText: 2008-2022 Luis Falcón <falcon@gnuhealth.org>
# SPDX-FileCopyrightText: 2011-2022 GNU Solidario <health@gnusolidario.org>
#
# SPDX-License-Identifier: GPL-3.0-or-later
#########################################################################
#   Hospital Management Information System (HMIS) component of the      #
#                       GNU Health project                              #
#                   https://www.gnuhealth.org                           #
#########################################################################
#                       HEALTH GYNECO package                           #
#              __init__.py: Package declaration file                    #
#########################################################################
from trytond.pool import Pool
from . import health_gyneco


def register():
    Pool.register(
        health_gyneco.PatientPregnancy,
        health_gyneco.PrenatalEvaluation,
        health_gyneco.PuerperiumMonitor,
        health_gyneco.Perinatal,
        health_gyneco.PerinatalMonitor,
        health_gyneco.GnuHealthPatient,
        health_gyneco.PatientMenstrualHistory,
        health_gyneco.PatientMammographyHistory,
        health_gyneco.PatientPAPHistory,
        health_gyneco.PatientColposcopyHistory,
        module='health_gyneco', type_='model')
