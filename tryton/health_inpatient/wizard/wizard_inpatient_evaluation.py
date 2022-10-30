# SPDX-FileCopyrightText: 2008-2022 Luis Falcón <falcon@gnuhealth.org>
# SPDX-FileCopyrightText: 2011-2022 GNU Solidario <health@gnusolidario.org>
#
# SPDX-License-Identifier: GPL-3.0-or-later

from trytond.model import ModelView
from trytond.wizard import Wizard, StateTransition, StateAction, StateView, Button
from trytond.transaction import Transaction
from trytond.pool import Pool
from trytond.pyson import PYSONEncoder

from ..exceptions import NoRecordSelected

__all__ = ['CreateInpatientEvaluation']

class CreateInpatientEvaluation(Wizard):
    'Create Inpatient Evaluation'
    __name__ = 'wizard.gnuhealth.inpatient.evaluation'
  
    start_state = 'inpatient_evaluation'
    inpatient_evaluation = StateAction('health_inpatient.act_inpatient_evaluation')

    def do_inpatient_evaluation(self, action):
      
        inpatient_registration = Transaction().context.get('active_id')

        try:
            reg_id = \
                Pool().get('gnuhealth.inpatient.registration').browse([inpatient_registration])[0]
        except:
            raise NoRecordSelected(
                gettext('health_inpatient.msg_no_record_selected'))

        patient = reg_id.patient.id

        
        action['pyson_domain'] = PYSONEncoder().encode([
            ('patient', '=', patient),
            ('inpatient_registration_code', '=', reg_id.id),
            ('evaluation_type', '=', 'inpatient'),
            ])
        action['pyson_context'] = PYSONEncoder().encode({
            'patient': patient,
            'inpatient_registration_code': reg_id.id,
            'evaluation_type': 'inpatient',
            })
            
        return action, {}
        
