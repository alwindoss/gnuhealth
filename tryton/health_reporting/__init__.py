##############################################################################
#
#    GNU Health: The Free Health and Hospital Information System
#    Copyright (C) 2011-2014 Sebastian Marro <smarro@gnusolidario.org>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
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
