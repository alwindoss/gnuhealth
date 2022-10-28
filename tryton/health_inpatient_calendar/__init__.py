# SPDX-FileCopyrightText: 2008-2022 Luis Falcón <falcon@gnuhealth.org>
# SPDX-FileCopyrightText: 2011-2022 GNU Solidario <health@gnusolidario.org>
# SPDX-FileCopyrightText: 2011-2012 Sebastian Marro <smarro@thymbra.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later
#########################################################################
#   Hospital Management Information System (HMIS) component of the      #
#                       GNU Health project                              #
#                   https://www.gnuhealth.org                           #
#########################################################################
#                  HEALTH INPATIENT CALENDAR PACKAGE                    #
#                __init__.py: Package declaration file                  #
#########################################################################


from trytond.pool import Pool
from . import health_inpatient_calendar


def register():
    Pool.register(
        health_inpatient_calendar.HospitalBed,
        health_inpatient_calendar.InpatientRegistration,
        module='health_inpatient_calendar', type_='model')
