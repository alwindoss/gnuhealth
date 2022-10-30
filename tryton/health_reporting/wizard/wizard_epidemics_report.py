# SPDX-FileCopyrightText: 2008-2022 Luis Falcón <falcon@gnuhealth.org>
# SPDX-FileCopyrightText: 2011-2022 GNU Solidario <health@gnusolidario.org>
#
# SPDX-License-Identifier: GPL-3.0-or-later
#########################################################################

from datetime import date
from trytond.model import ModelView, fields
from trytond.wizard import Wizard, StateView, StateAction, Button
from dateutil.relativedelta import relativedelta

__all__ = ['EpidemicsReportStart', 'EpidemicsReport']


class EpidemicsReportStart(ModelView):
    'Epidemics Report Start'
    __name__ = 'gnuhealth.epidemics.report.open.start'

    health_condition = fields.Many2One(
        'gnuhealth.pathology', 'Condition', required=True)

    start_date = fields.Date("Start")
    end_date = fields.Date("End")

    demographics = fields.Boolean("Demographics")

    @staticmethod
    def default_start_date():
        return date.today() - relativedelta(days=7)

    @staticmethod
    def default_end_date():
        return date.today()

    @staticmethod
    def default_demographics():
        return True


class EpidemicsReport(Wizard):
    'Open Institution Epidemics Report'
    __name__ = 'gnuhealth.epidemics.report.open'

    start = StateView(
        'gnuhealth.epidemics.report.open.start',
        'health_reporting.epidemics_report_open_start_view_form', [
            Button('Cancel', 'end', 'tryton-cancel'),
            Button('Open', 'open_', 'tryton-ok', default=True),
            ])

    open_ = StateAction('health_reporting.report_epidemics_information')

    def fill_data(self):
        return {
            'health_condition': (
                self.start.health_condition.id
                if self.start.health_condition else None),
            'start_date': self.start.start_date,
            'end_date': self.start.end_date,
            'demographics': self.start.demographics,
        }

    def do_open_(self, action):
        return action, self.fill_data()

    def transition_open_(self):
        return 'end'
