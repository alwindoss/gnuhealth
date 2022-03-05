##############################################################################
#
#    GNU Health: The Free Health and Hospital Information System
#    Copyright (C) 2008-2022 Luis Falcon <falcon@gnuhealth.org>
#    Copyright (C) 2011-2022 GNU Solidario <health@gnusolidario.org>
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
