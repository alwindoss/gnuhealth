##############################################################################
#
#    GNU Health: The Free Health and Hospital Information System
#    Copyright (C) 2008-2022 Luis Falcon <lfalcon@gnusolidario.org>
#    Copyright (C) 2011-2022 GNU Solidario <health@gnusolidario.org>
#
#
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
from trytond.model import ModelView, fields
from trytond.pyson import Eval, Equal
from trytond.wizard import Wizard
from trytond.pool import Pool


__all__ = ['RequestPatientLabTestStart', 'RequestPatientLabTest']


# Include services in the wizard
class RequestPatientLabTestStart(ModelView):
    'Request Patient Lab Test Start'
    __name__ = 'gnuhealth.patient.lab.test.request.start'

    service = fields.Many2One(
        'gnuhealth.health_service', 'Service',
        domain=[('patient', '=', Eval('patient'))], depends=['patient'],
        states={'readonly': Equal(Eval('state'), 'done')},
        help="Service document associated to this Lab Request")


class RequestPatientLabTest(Wizard):
    'Request Patient Lab Test'
    __name__ = 'gnuhealth.patient.lab.test.request'

    def generate_code(self, **pattern):
        Config = Pool().get('gnuhealth.sequences')
        config = Config(1)
        sequence = config.get_multivalue(
            'lab_request_sequence', **pattern)
        if sequence:
            return sequence.get()

    def transition_request(self):
        PatientLabTest = Pool().get('gnuhealth.patient.lab.test')
        request_number = self.generate_code()
        lab_tests = []
        for test in self.start.tests:
            lab_test = {}
            lab_test['request'] = request_number
            lab_test['name'] = test.id
            lab_test['patient_id'] = self.start.patient.id
            if self.start.doctor:
                lab_test['doctor_id'] = self.start.doctor.id
            if self.start.context:
                lab_test['context'] = self.start.context.id
            lab_test['date'] = self.start.date
            lab_test['urgent'] = self.start.urgent

            if self.start.service:
                lab_test['service'] = self.start.service.id

            lab_tests.append(lab_test)

        PatientLabTest.create(lab_tests)

        return 'end'
