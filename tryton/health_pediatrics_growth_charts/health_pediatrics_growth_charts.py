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
#                 HEALTH PEDIATRICS_GROWTH_CHARTS package               #
#              health_pediatrics_growth_charts.py: main module          #
#########################################################################

from dateutil.relativedelta import relativedelta
from trytond.model import fields
from trytond.pool import PoolMeta

__all__ = ['PatientEvaluation']
__metaclass__ = PoolMeta


class PatientEvaluation(metaclass=PoolMeta):
    __name__ = 'gnuhealth.patient.evaluation'

    age_months = fields.Function(
        fields.Integer('Patient Age in Months'),
        'get_patient_age_months')

    def get_patient_age_months(self, name):
        if self.patient:
            if self.patient.dob:
                delta = relativedelta(self.evaluation_start, self.patient.dob)
                return delta.years * 12 + delta.months
        return None
