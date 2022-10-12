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
#                  wizard_appointment_evaluation.py: wizard             #
#########################################################################
from trytond.model import ModelView
from trytond.wizard import Wizard, StateTransition, StateAction, \
    StateView, Button
from trytond.transaction import Transaction
from trytond.pool import Pool
from trytond.pyson import PYSONEncoder

from trytond.i18n import gettext

from ..exceptions import NoAppointmentSelected
__all__ = ['CreateAppointmentEvaluation']


class CreateAppointmentEvaluation(Wizard):
    'Create Appointment Evaluation'
    __name__ = 'wizard.gnuhealth.appointment.evaluation'

    start_state = 'appointment_evaluation'
    appointment_evaluation = StateAction('health.act_app_evaluation')

    def do_appointment_evaluation(self, action):

        appointment = Transaction().context.get('active_id')

        try:
            app_id = \
                Pool().get('gnuhealth.appointment').browse([appointment])[0]
        except:
            raise NoAppointmentSelected(gettext(
                'health.msg_no_appointment_selected')
                )

        patient = app_id.patient.id

        if (app_id.speciality):
            specialty = app_id.speciality.id
        else:
            specialty = None
        urgency = str(app_id.urgency)
        evaluation_type = str(app_id.appointment_type)
        visit_type = str(app_id.visit_type)

        action['pyson_domain'] = PYSONEncoder().encode([
            ('appointment', '=', appointment),
            ('patient', '=', patient),
            ('specialty', '=', specialty),
            ('urgency', '=', urgency),
            ('evaluation_type', '=', evaluation_type),
            ('visit_type', '=', visit_type),
            ])
        action['pyson_context'] = PYSONEncoder().encode({
            'appointment': appointment,
            'patient': patient,
            'specialty': specialty,
            'urgency': urgency,
            'evaluation_type': evaluation_type,
            'visit_type': visit_type,
            })

        return action, {}
