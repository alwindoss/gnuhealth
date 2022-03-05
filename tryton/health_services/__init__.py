# -*- coding: utf-8 -*-
##############################################################################
#
#    GNU Health: The Free Health and Hospital Information System
#    Copyright (C) 2008-2022 Luis Falcon <lfalcon@gnusolidario.org>
#    Copyright (C) 2011-2022 GNU Solidario <health@gnusolidario.org>
#
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    The GNU Health HMIS component is part of the GNU Health project
#    www.gnuhealth.org
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

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
