# SPDX-FileCopyrightText: 2008-2022 Luis Falcón <falcon@gnuhealth.org>
# SPDX-FileCopyrightText: 2011-2022 GNU Solidario <health@gnusolidario.org>
#
# SPDX-License-Identifier: GPL-3.0-or-later
#########################################################################

from datetime import date
from trytond.model import ModelView, fields
from trytond.wizard import Wizard, StateView, StateAction, Button

__all__ = ['SummaryReportStart', 'SummaryReport']


class SummaryReportStart(ModelView):
    'Summary Report Start'
    __name__ = 'gnuhealth.summary.report.open.start'

    institution = fields.Many2One(
        'gnuhealth.institution', 'Institution',)

    start_date = fields.Date("Start")
    end_date = fields.Date("End")

    demographics = fields.Boolean("Demographics")
    patient_evaluations = fields.Boolean("Evaluations")

    @staticmethod
    def default_start_date():
        return date.today()

    @staticmethod
    def default_end_date():
        return date.today()

    @staticmethod
    def default_demographics():
        return True


class SummaryReport(Wizard):
    'Open Institution Summary Report'
    __name__ = 'gnuhealth.summary.report.open'

    start = StateView(
        'gnuhealth.summary.report.open.start',
        'health_reporting.summary_report_open_start_view_form', [
            Button('Cancel', 'end', 'tryton-cancel'),
            Button('Open', 'open_', 'tryton-ok', default=True),
            ])

    open_ = StateAction('health_reporting.report_summary_information')

    def fill_data(self):
        return {
            'institution': (self.start.institution.id
                            if self.start.institution else None),
            'start_date': self.start.start_date,
            'end_date': self.start.end_date,
            'demographics': self.start.demographics,
            'patient_evaluations': self.start.patient_evaluations,
        }

    def do_open_(self, action):
        return action, self.fill_data()

    def transition_open_(self):
        return 'end'
