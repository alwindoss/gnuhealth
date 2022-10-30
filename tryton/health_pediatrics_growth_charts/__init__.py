# SPDX-FileCopyrightText: 2008-2022 Luis Falcón <falcon@gnuhealth.org>
# SPDX-FileCopyrightText: 2013 Sebastian Marro <smarro@thymbra.com>
# SPDX-FileCopyrightText: 2011-2022 GNU Solidario <health@gnusolidario.org>
#
# SPDX-License-Identifier: GPL-3.0-or-later
#########################################################################
#   Hospital Management Information System (HMIS) component of the      #
#                       GNU Health project                              #
#                   https://www.gnuhealth.org                           #
#########################################################################
#                 HEALTH PEDIATRICS_GROWTH_CHARTS package               #
#                  __init__.py: Package declaration file                #
#########################################################################

from trytond.pool import Pool
from .import health_pediatrics_growth_charts 


def register():
    Pool.register(
        health_pediatrics_growth_charts.PatientEvaluation,
        module='health_pediatrics_growth_charts', type_='model')
