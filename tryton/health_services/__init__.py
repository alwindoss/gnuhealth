# SPDX-FileCopyrightText: 2008-2022 Luis Falcón <falcon@gnuhealth.org>
# SPDX-FileCopyrightText: 2011-2022 GNU Solidario <health@gnusolidario.org>
#
# SPDX-License-Identifier: GPL-3.0-or-later
#########################################################################
#   Hospital Management Information System (HMIS) component of the      #
#                       GNU Health project                              #
#                   https://www.gnuhealth.org                           #
#########################################################################
#                          HEALTH SERVICES package                      #
#                 __init__.py: Package declaration file                 #
#########################################################################

from trytond.pool import Pool
from . import sequences
from . import health_services
from . import wizard
from . import invoice


def register():
    Pool.register(
        sequences.GnuHealthSequences,
        sequences.HealthServiceSequence,
        health_services.HealthService,
        health_services.HealthServiceLine,
        wizard.CreateServiceInvoiceInit,
        invoice.Invoice,
        invoice.InvoiceLine,
        health_services.PatientPrescriptionOrder,
        health_services.PatientEvaluation,
        module='health_services', type_='model')
    Pool.register(
        wizard.CreateServiceInvoice,
        module='health_services', type_='wizard')
