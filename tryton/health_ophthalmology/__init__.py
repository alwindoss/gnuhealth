# SPDX-FileCopyrightText: 2008-2022 Luis Falcón <falcon@gnuhealth.org>
# SPDX-FileCopyrightText: 2011-2022 GNU Solidario <health@gnusolidario.org>
#
# SPDX-License-Identifier: GPL-3.0-or-later
#########################################################################
#   Hospital Management Information System (HMIS) component of the      #
#                       GNU Health project                              #
#                   https://www.gnuhealth.org                           #
#########################################################################
#                       HEALTH OPHTHALMOLOGY package                    #
#                  __init__.py: Package declaration file                #
#########################################################################

from trytond.pool import Pool
from . import health_ophthalmology


def register():
    Pool.register(
        health_ophthalmology.OphthalmologyEvaluation,
        health_ophthalmology.OphthalmologyFindings,
        module='health_ophthalmology', type_='model')
