# SPDX-FileCopyrightText: 2008-2022 Luis Falcón <falcon@gnuhealth.org>
# SPDX-FileCopyrightText: 2011-2022 GNU Solidario <health@gnusolidario.org>
#
# SPDX-License-Identifier: GPL-3.0-or-later
#########################################################################
#   Hospital Management Information System (HMIS) component of the      #
#                       GNU Health project                              #
#                   https://www.gnuhealth.org                           #
#########################################################################
#                           HEALTH package                              #
#              wizard_check_immunization_status.py: wizard              #
#########################################################################
from trytond.wizard import Wizard, StateView, Button, StateAction
from trytond.model import ModelView, fields
from trytond.transaction import Transaction

__all__ = ['CheckImmunizationStatusInit', 'CheckImmunizationStatus']


class CheckImmunizationStatusInit(ModelView):
    'Check Immunization Status Init'
    __name__ = 'gnuhealth.check_immunization_status.init'
    immunization_schedule = fields.Many2One(
        "gnuhealth.immunization_schedule", "Schedule",
        required=True)


class CheckImmunizationStatus(Wizard):
    'Check Immunization Status'
    __name__ = 'gnuhealth.check_immunization_status'

    start = StateView(
        'gnuhealth.check_immunization_status.init',
        'health.view_check_immunization_status', [
         Button('Cancel', 'end', 'tryton-cancel'),
         Button('Immunization Status', 'check_immunization_status',
                'tryton-ok', True),
            ])
    check_immunization_status = StateAction(
        'health.report_immunization_status')

    def do_check_immunization_status(self, action):
        return action, self.get_info()

    def get_info(self):

        return {
            'patient_id': Transaction().context.get('active_id'),
            'immunization_schedule_id': self.start.immunization_schedule.id
            }

    def transition_check_immunization_status(self):
        return 'end'
