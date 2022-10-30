#!/usr/bin/env python

# SPDX-FileCopyrightText: 2008-2022 Luis Falcón <falcon@gnuhealth.org>
# SPDX-FileCopyrightText: 2011-2022 GNU Solidario <health@gnusolidario.org>
#
# SPDX-License-Identifier: GPL-3.0-or-later
#########################################################################
#   Hospital Management Information System (HMIS) component of the      #
#                       GNU Health project                              #
#                   https://www.gnuhealth.org                           #
#########################################################################
#                      HEALTH SURGERY package                           #
#               __init__.py: Package declaration file                   #
#########################################################################

from trytond.pool import Pool
from . import health_surgery
from . import report
from . import sequences


def register():
    Pool.register(
        sequences.GnuHealthSequences,
        sequences.SurgeryCodeSequence,
        health_surgery.RCRI,
        health_surgery.Surgery,
        health_surgery.Operation,
        health_surgery.SurgerySupply,
        health_surgery.PatientData,
        health_surgery.SurgeryTeam,
        health_surgery.SurgeryComplication,
        health_surgery.PreOperativeAssessment,
        health_surgery.SurgeryProtocol,
        health_surgery.SurgeryDrain,
        health_surgery.PatientEvaluation,
        module='health_surgery', type_='model')
    Pool.register(
        report.SurgeryReport,
        module='health_surgery', type_='report')
