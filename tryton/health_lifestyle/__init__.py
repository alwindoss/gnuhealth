# SPDX-FileCopyrightText: 2008-2022 Luis Falcón <falcon@gnuhealth.org>
# SPDX-FileCopyrightText: 2011-2022 GNU Solidario <health@gnusolidario.org>
#
# SPDX-License-Identifier: GPL-3.0-or-later
#########################################################################
#   Hospital Management Information System (HMIS) component of the      #
#                       GNU Health project                              #
#                   https://www.gnuhealth.org                           #
#########################################################################
#                      HEALTH LIFESTYLE package                         #
#              __init__.py: Package declaration file                    #
#########################################################################

from trytond.pool import Pool
from . import health_lifestyle


def register():
    Pool.register(
        health_lifestyle.VegetarianTypes,
        health_lifestyle.DietBelief,
        health_lifestyle.DrugsRecreational,
        health_lifestyle.PatientRecreationalDrugs,
        health_lifestyle.PatientCAGE,
        health_lifestyle.MedicalPatient,
        module='health_lifestyle', type_='model')
