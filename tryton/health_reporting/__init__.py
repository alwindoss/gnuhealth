# SPDX-FileCopyrightText: 2008-2022 Luis Falcón <falcon@gnuhealth.org>
# SPDX-FileCopyrightText: 2011-2014 Sebastian Marro <smarro@thymbra.com>
# SPDX-FileCopyrightText: 2011-2022 GNU Solidario <health@gnusolidario.org>
#
# SPDX-License-Identifier: GPL-3.0-or-later
#########################################################################
#   Hospital Management Information System (HMIS) component of the      #
#                       GNU Health project                              #
#                   https://www.gnuhealth.org                           #
#########################################################################
#                         HEALTH REPORTING package                      #
#                 __init__.py: Package declaration file                 #
#########################################################################

from trytond.pool import Pool
from . import wizard
from . import report


def register():
    Pool.register(
        wizard.wizard_top_diseases.TopDiseases,
        wizard.wizard_top_diseases.OpenTopDiseasesStart,
        wizard.wizard_evaluations.OpenEvaluationsStart,
        wizard.wizard_summary_report.SummaryReportStart,
        wizard.wizard_evaluations.EvaluationsDoctor,
        wizard.wizard_evaluations.EvaluationsSpecialty,
        wizard.wizard_evaluations.EvaluationsSector,
        wizard.wizard_epidemics_report.EpidemicsReportStart,
        module='health_reporting', type_='model')
    Pool.register(
        wizard.wizard_top_diseases.OpenTopDiseases,
        wizard.wizard_evaluations.OpenEvaluations,
        wizard.wizard_summary_report.SummaryReport,
        wizard.wizard_epidemics_report.EpidemicsReport,
        module='health_reporting', type_='wizard')

    Pool.register(
        report.summary_report.InstitutionSummaryReport,
        report.epidemics_report.InstitutionEpidemicsReport,
        module='health_reporting', type_='report')
