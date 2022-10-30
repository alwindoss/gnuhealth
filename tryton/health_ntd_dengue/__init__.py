# SPDX-FileCopyrightText: 2008-2022 Luis Falcón <falcon@gnuhealth.org>
# SPDX-FileCopyrightText: 2011-2022 GNU Solidario <health@gnusolidario.org>
#
# SPDX-License-Identifier: GPL-3.0-or-later
#########################################################################
#   Hospital Management Information System (HMIS) component of the      #
#                       GNU Health project                              #
#                   https://www.gnuhealth.org                           #
#########################################################################
#                      HEALTH NTD_DENGUE package                        #
#              __init__.py: Package declaration file                    #
#########################################################################

from trytond.pool import Pool
from . import health_ntd_dengue
from . import sequences


def register():
    Pool.register(
        health_ntd_dengue.DengueDUSurvey,
        sequences.GnuHealthSequences,
        sequences.DengueDUSurveySequence,
        module='health_ntd_dengue', type_='model')
