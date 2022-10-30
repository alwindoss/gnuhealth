# SPDX-FileCopyrightText: 2008-2022 Luis Falcón <falcon@gnuhealth.org>
# SPDX-FileCopyrightText: 2011-2022 GNU Solidario <health@gnusolidario.org>
#
# SPDX-License-Identifier: GPL-3.0-or-later
#########################################################################
#   Hospital Management Information System (HMIS) component of the      #
#                       GNU Health project                              #
#                   https://www.gnuhealth.org                           #
#########################################################################
#                        HEALTH PEDIATRICS package                      #
#                  __init__.py: Package declaration file                #
#########################################################################

from trytond.pool import Pool
from . import health_pediatrics


def register():
    Pool.register(
        health_pediatrics.Newborn,
        health_pediatrics.NeonatalApgar,
        health_pediatrics.NeonatalMedication,
        health_pediatrics.NeonatalCongenitalDiseases,
        health_pediatrics.PediatricSymptomsChecklist,
        module='health_pediatrics', type_='model')
