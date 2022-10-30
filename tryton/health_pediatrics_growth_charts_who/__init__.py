# SPDX-FileCopyrightText: 2008-2022 Luis Falcón <falcon@gnuhealth.org>
# SPDX-FileCopyrightText: 2013 Sebastian Marro <smarro@thymbra.com>
# SPDX-FileCopyrightText: 2011-2022 GNU Solidario <health@gnusolidario.org>
#
# SPDX-License-Identifier: GPL-3.0-or-later
#########################################################################
#   Hospital Management Information System (HMIS) component of the      #
#                       GNU Health project                              #
#                   https://www.gnuhealth.org                           #
#########################################################################
#                 HEALTH PEDIATRICS_GROWTH_CHARTS_WHO package           #
#                  __init__.py: Package declaration file                #
#########################################################################
from trytond.pool import Pool
from . import health_pediatrics_growth_charts_who
from . import wizard
from . import report


def register():
    Pool.register(
        health_pediatrics_growth_charts_who.PediatricsGrowthChartsWHO,
        wizard.wizard_health_pediatrics_growth_charts_who.
        OpenPediatricsGrowthChartsWHOReportStart,
        module='health_pediatrics_growth_charts_who', type_='model')
    Pool.register(
        wizard.wizard_health_pediatrics_growth_charts_who.
        OpenPediatricsGrowthChartsWHOReport,
        module='health_pediatrics_growth_charts_who', type_='wizard')
    Pool.register(
        report.report_health_pediatrics_growth_charts_who.
        PediatricsGrowthChartsWHOReport,
        report.report_health_pediatrics_growth_charts_who.
        WeightForAge,
        report.report_health_pediatrics_growth_charts_who.
        LengthHeightForAge,
        report.report_health_pediatrics_growth_charts_who.
        BMIForAge,
        module='health_pediatrics_growth_charts_who', type_='report')
