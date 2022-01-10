# -*- coding: utf-8 -*-
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
import datetime
from trytond.model import ModelView, fields
from trytond.pyson import Eval, Not, Bool, PYSONEncoder, Equal, And, Or, If
from trytond.wizard import Wizard, StateTransition, StateView, Button
from trytond.transaction import Transaction
from trytond.pool import Pool


__all__ = ['RequestPatientImagingTestStart', 'RequestPatientImagingTest']


# Include services in the wizard
class RequestPatientImagingTestStart(ModelView):
    'Request Patient Imaging Test Start'
    __name__ = 'gnuhealth.patient.imaging.test.request.start'

    service = fields.Many2One(
        'gnuhealth.health_service', 'Service',
        domain=[('patient', '=', Eval('patient'))], depends=['patient'],
        states = {'readonly': Equal(Eval('state'), 'done')},
        help="Service document associated to this Imaging Request")


class RequestPatientImagingTest(Wizard):
    'Request Patient Imaging Test'
    __name__ = 'gnuhealth.patient.imaging.test.request'

    def generate_code(self, **pattern):
        Config = Pool().get('gnuhealth.sequences')
        config = Config(1)
        sequence = config.get_multivalue(
            'imaging_request_sequence', **pattern)
        if sequence:
            return sequence.get()


    def transition_request(self):
        ImagingTestRequest = Pool().get('gnuhealth.imaging.test.request')
        request_number = self.generate_code()
        imaging_tests = []
        for test in self.start.tests:
            imaging_test = {}
            imaging_test['request'] = request_number
            imaging_test['requested_test'] = test.id
            imaging_test['patient'] = self.start.patient.id
            if self.start.doctor:
                imaging_test['doctor'] = self.start.doctor.id
            if self.start.context:
                imaging_test['context'] = self.start.context.id
            imaging_test['date'] = self.start.date
            imaging_test['urgent'] = self.start.urgent
            if self.start.service:
                imaging_test['service'] = self.start.service.id

            imaging_tests.append(imaging_test)
        ImagingTestRequest.create(imaging_tests)

        return 'end'
