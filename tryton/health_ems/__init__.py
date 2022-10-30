# SPDX-FileCopyrightText: 2008-2022 Luis Falcón <falcon@gnuhealth.org>
# SPDX-FileCopyrightText: 2011-2022 GNU Solidario <health@gnusolidario.org>
#
# SPDX-License-Identifier: GPL-3.0-or-later

#########################################################################
#   Hospital Management Information System (HMIS) component of the      #
#                       GNU Health project                              #
#                   https://www.gnuhealth.org                           #
#########################################################################
#                       HEALTH EMS package                              #
#             __init__.py: Package declaration file                     #
#########################################################################

from trytond.pool import Pool
from . import health_ems
from . import sequences


def register():
    Pool.register(
        sequences.GnuHealthSequences,
        sequences.SupportRequestSequence,
        health_ems.Ambulance,
        health_ems.SupportRequest,
        health_ems.AmbulanceSupport,
        health_ems.AmbulanceHealthProfessional,
        health_ems.SupportRequestLog,
        module='health_ems', type_='model')

