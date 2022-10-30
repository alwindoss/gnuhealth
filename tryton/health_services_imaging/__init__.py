# SPDX-FileCopyrightText: 2008-2022 Luis Falcón <falcon@gnuhealth.org>
# SPDX-FileCopyrightText: 2011-2022 GNU Solidario <health@gnusolidario.org>
#
# SPDX-License-Identifier: GPL-3.0-or-later
#########################################################################
#   Hospital Management Information System (HMIS) component of the      #
#                       GNU Health project                              #
#                   https://www.gnuhealth.org                           #
#########################################################################
#                     HEALTH SERVICES IMAGING package                   #
#                 __init__.py: Package declaration file                 #
#########################################################################

from trytond.pool import Pool
from . import health_services_imaging
from . import wizard


def register():
    Pool.register(
    health_services_imaging.ImagingTestRequest,
	wizard.RequestPatientImagingTestStart,
        module='health_services_imaging', type_='model')
    Pool.register(
        wizard.RequestPatientImagingTest,
        module='health_services_imaging', type_='wizard')
