# SPDX-FileCopyrightText: 2008-2022 Luis Falcón <falcon@gnuhealth.org>
# SPDX-FileCopyrightText: 2011-2022 GNU Solidario <health@gnusolidario.org>
#
# SPDX-License-Identifier: GPL-3.0-or-later
#########################################################################
#   Hospital Management Information System (HMIS) component of the      #
#                       GNU Health project                              #
#                   https://www.gnuhealth.org                           #
#########################################################################
#                        HEALTH CALENDAR package                        #
#                __init__.py: Package declaration file                  #
#########################################################################

from trytond.pool import Pool
from .health_calendar import *
from .wizard import *


def register():
    Pool.register(
        User,
        Appointment,
        CreateAppointmentStart,
        module='health_calendar', type_='model')
    Pool.register(
        CreateAppointment,
        module='health_calendar', type_='wizard')
