# coding=utf-8

#    Copyright (C) 2008-2011  Luis Falcon

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

from datetime import datetime
from trytond.model import ModelView, ModelSQL, fields
from trytond.transaction import Transaction


class PatientData(ModelSQL, ModelView):
    'Patient lab tests'
    _name = 'gnuhealth.patient'
    _description = __doc__

    lab_test_ids = fields.One2Many('gnuhealth.patient.lab.test', 'patient_id',
        'Lab Tests Required')

PatientData()


class TestType(ModelSQL, ModelView):
    'Type of Lab test'
    _name = 'gnuhealth.test_type'
    _description = __doc__

    name = fields.Char('Test', 
        help="Test type, eg X-Ray, hemogram,biopsy...", select="1")
    code = fields.Char('Code', 
        help="Short name - code for the test", select="2")
    info = fields.Text('Description')
    product_id = fields.Many2One('product.product', 'Service', required=True)
    critearea = fields.One2Many('gnuhealth.lab.test.critearea', 'test_type_id',
        'Test Cases')

    def __init__(self):
        super(TestType, self).__init__()
        self._sql_constraints = [
            ('code_uniq', 'unique(name)', 'The Lab Test code must be unique'),
        ]

TestType()


class Lab(ModelSQL, ModelView):
    'Lab Test'
    _name = 'gnuhealth.lab'
    _description = __doc__

    name = fields.Char('ID', help="Lab result ID")
    test = fields.Many2One('gnuhealth.test_type', 'Test type',
        help="Lab test type", select="1")
    patient = fields.Many2One('gnuhealth.patient', 'Patient',
     help="Patient ID", select="1")
    pathologist = fields.Many2One('gnuhealth.physician', 'Pathologist',
        help="Pathologist", select="2")
    requestor = fields.Many2One('gnuhealth.physician', 'Physician',
        help="Doctor who requested the test", select="2")
    results = fields.Text('Results')
    diagnosis = fields.Text('Diagnosis')
    critearea = fields.One2Many('gnuhealth.lab.test.critearea', 'gnuhealth_lab_id',
        'Test Cases')
    date_requested = fields.DateTime('Date requested', select="1")
    date_analysis = fields.DateTime('Date of the Analysis', select="1")

    def __init__(self):
        super(Lab, self).__init__()
        self._sql_constraints += [
            ('id_uniq', 'unique (name)', 'The test ID code must be unique'),
        ]

    def default_date_requested(self):
        return datetime.now()

    def default_analysis(self):
        return datetime.now()

    def default_name(self):
        sequence_obj = self.pool.get('ir.sequence')
        return sequence_obj.get('gnuhealth.lab')

Lab()


class GnuHealthLabTestUnits(ModelSQL, ModelView):
    'Lab Test Units'
    _name = 'gnuhealth.lab.test.units'
    _description = __doc__

    name = fields.Char('Unit', select="1")
    code = fields.Char('Code', select="1")

    def __init__(self):
        super(GnuHealthLabTestUnits, self).__init__()
        self._sql_constraints = [
            ('name_uniq', 'unique(name)', 'The Unit name must be unique'),
        ]

GnuHealthLabTestUnits()


class GnuHealthTestCritearea(ModelSQL, ModelView):
    'Lab Test Critearea'
    _name = 'gnuhealth.lab.test.critearea'
    _description = __doc__

    name = fields.Char('Test', select="1")
    result = fields.Text('Result')
    normal_range = fields.Text('Normal Range')
    lower_limit = fields.Float ('Lower Limit')
    upper_limit = fields.Float ('Upper Limit')
    units = fields.Many2One('gnuhealth.lab.test.units', 'Units')
    test_type_id = fields.Many2One('gnuhealth.test_type', 'Test type',
     select="2")
    gnuhealth_lab_id = fields.Many2One('gnuhealth.lab', 'Test Cases', select="2")
    sequence = fields.Integer('Sequence')

    def __init__(self):
        super(GnuHealthTestCritearea, self).__init__()
        self._order.insert(0, ('sequence', 'ASC'))

    def default_sequence(self):
        return 1

GnuHealthTestCritearea()


class GnuHealthPatientLabTest(ModelSQL, ModelView):
    'Patient Lab Test'
    _name = 'gnuhealth.patient.lab.test'
    _description = __doc__

    name = fields.Many2One('gnuhealth.test_type', 'Test Type', required=True,
     select="1")
    date = fields.DateTime('Date', select="2")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('tested', 'Tested'),
        ('cancel', 'Cancel'),
        ], 'State', readonly=True, select="1")
    patient_id = fields.Many2One('gnuhealth.patient', 'Patient', required=True,
     select="1")
    doctor_id = fields.Many2One('gnuhealth.physician', 'Doctor',
        help="Doctor who Request the lab test.", select="1")

    def default_date(self):
        return datetime.now()

    def default_state(self):
        return 'draft'

    def default_doctor_id(self):
        user_obj = self.pool.get('res.user')
        user = user_obj.browse(Transaction().user)
        uid = int(user.id)

        party_id = self.pool.get('party.party').search([
                ('internal_user', '=', uid)])
        if party_id:
            dr_id = self.pool.get('gnuhealth.physician').search([
                    ('name', '=', party_id[0])])
            if dr_id:
                return dr_id[0]
            else:
                raise Exception('There is no physician defined ' \
                                'for current user.')
        else:
            return False

GnuHealthPatientLabTest()
