##############################################################################
#
#    GNU Health: The Free Health and Hospital Information System
#    Copyright (C) 2008-2022 Luis Falcon <falcon@gnuhealth.org>
#    Copyright (C) 2011-2022 GNU Solidario <health@gnusolidario.org>
#
#    The GNU Health HMIS component is part of the GNU Health project
#    www.gnuhealth.org
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
from datetime import datetime
from trytond.model import ModelView, ModelSQL, fields, Unique
from trytond.pool import Pool
from trytond.pyson import Eval, Not, Bool
from trytond.modules.health.core import get_health_professional

__all__ = [
    'PatientData', 'TestType', 'Lab',
    'GnuHealthLabTestUnits', 'GnuHealthTestCritearea',
    'GnuHealthPatientLabTest', 'PatientHealthCondition']


class PatientData(ModelSQL, ModelView):
    'Patient lab tests'
    __name__ = 'gnuhealth.patient'

    lab_test_ids = fields.One2Many(
        'gnuhealth.patient.lab.test', 'patient_id',
        'Lab Tests Required')


class TestType(ModelSQL, ModelView):
    'Type of Lab test'
    __name__ = 'gnuhealth.lab.test_type'

    name = fields.Char(
        'Test',
        help="Test type, eg X-Ray, hemogram,biopsy...", required=True,
        select=True, translate=True)
    code = fields.Char(
        'Code',
        help="Short name - code for the test", required=True, select=True)
    info = fields.Text('Description')
    product_id = fields.Many2One('product.product', 'Service', required=True)
    critearea = fields.One2Many(
        'gnuhealth.lab.test.critearea', 'test_type_id',
        'Test Cases')

    active = fields.Boolean('Active', select=True)

    @staticmethod
    def default_active():
        return True

    @classmethod
    def __setup__(cls):
        super(TestType, cls).__setup__()
        t = cls.__table__()
        cls._sql_constraints = [
            ('code_uniq', Unique(t, t.name),
             'The Lab Test code must be unique')
        ]

    @classmethod
    def check_xml_record(cls, records, values):
        return True

    @classmethod
    def search_rec_name(cls, name, clause):
        """ Search for the full name and the code """
        field = None
        for field in ('name', 'code'):
            tests = cls.search([(field,) + tuple(clause[1:])], limit=1)
            if tests:
                break
        if tests:
            return [(field,) + tuple(clause[1:])]
        return [(cls._rec_name,) + tuple(clause[1:])]


class Lab(ModelSQL, ModelView):
    'Patient Lab Test Results'
    __name__ = 'gnuhealth.lab'

    name = fields.Char('ID', help="Lab result ID", readonly=True)
    test = fields.Many2One(
        'gnuhealth.lab.test_type', 'Test type',
        help="Lab test type", required=True, select=True)
    patient = fields.Many2One(
        'gnuhealth.patient', 'Patient',
        help="Patient ID", required=True, select=True)
    pathologist = fields.Many2One(
        'gnuhealth.healthprofessional', 'Pathologist',
        help="Pathologist", select=True)
    requestor = fields.Many2One(
        'gnuhealth.healthprofessional', 'Health prof',
        help="Doctor who requested the test", select=True)
    results = fields.Text('Results')
    diagnosis = fields.Text('Diagnosis')
    critearea = fields.One2Many(
        'gnuhealth.lab.test.critearea',
        'gnuhealth_lab_id', 'Lab Test Critearea')
    date_requested = fields.DateTime(
        'Date requested', required=True, select=True)
    date_analysis = fields.DateTime('Date of the Analysis', select=True)
    request_order = fields.Integer('Order', readonly=True)

    pathology = fields.Many2One(
        'gnuhealth.pathology', 'Pathology',
        help='Pathology confirmed / associated to this lab test.')

    analytes_summary = fields.Function(
        fields.Text('Summary'), 'get_analytes_summary')

    def get_analytes_summary(self, name):
        summ = ""
        for analyte in self.critearea:
            if analyte.result or analyte.result_text:
                res = ""
                res_text = ""
                if analyte.result_text:
                    res_text = analyte.result_text
                if analyte.result:
                    res = str(analyte.result) + " "
                summ = summ + analyte.rec_name + " " + \
                    res + res_text + "\n"
        return summ

    @classmethod
    def __setup__(cls):
        super(Lab, cls).__setup__()
        t = cls.__table__()
        cls._sql_constraints = [
            ('id_uniq', Unique(t, t.name),
             'The test ID code must be unique')
        ]
        cls._order.insert(0, ('date_requested', 'DESC'))

    @staticmethod
    def default_date_requested():
        return datetime.now()

    @staticmethod
    def default_date_analysis():
        return datetime.now()

    @classmethod
    def generate_code(cls, **pattern):
        Config = Pool().get('gnuhealth.sequences')
        config = Config(1)
        sequence = config.get_multivalue(
            'lab_test_sequence', **pattern)
        if sequence:
            return sequence.get()

    @classmethod
    def create(cls, vlist):
        vlist = [x.copy() for x in vlist]
        for values in vlist:
            if not values.get('name'):
                values['name'] = cls.generate_code()

        return super(Lab, cls).create(vlist)

    @classmethod
    def search_rec_name(cls, name, clause):
        if clause[1].startswith('!') or clause[1].startswith('not '):
            bool_op = 'AND'
        else:
            bool_op = 'OR'
        return [
            bool_op,
            ('patient', ) + tuple(clause[1:]),
            ('name', ) + tuple(clause[1:]),
            ]


class GnuHealthLabTestUnits(ModelSQL, ModelView):
    'Lab Test Units'
    __name__ = 'gnuhealth.lab.test.units'

    name = fields.Char('Unit', select=True)
    code = fields.Char('Code', select=True)

    @classmethod
    def __setup__(cls):
        super(GnuHealthLabTestUnits, cls).__setup__()
        t = cls.__table__()
        cls._sql_constraints = [
            ('name_uniq', Unique(t, t.name),
             'The Unit name must be unique')
        ]

    @classmethod
    def check_xml_record(cls, records, values):
        return True


class GnuHealthTestCritearea(ModelSQL, ModelView):
    'Lab Test Critearea'
    __name__ = 'gnuhealth.lab.test.critearea'

    name = fields.Char(
        'Analyte', required=True, select=True,
        translate=True)
    excluded = fields.Boolean(
        'Excluded', help='Select this option when'
        ' this analyte is excluded from the test')
    result = fields.Float('Value')
    result_text = fields.Char(
        'Result - Text', help='Non-numeric results. For '
        'example qualitative values, morphological, colors ...')
    remarks = fields.Char('Remarks')
    normal_range = fields.Text('Reference')
    lower_limit = fields.Float('Lower Limit')
    upper_limit = fields.Float('Upper Limit')
    warning = fields.Boolean(
        'Warn', help='Warns the patient about this '
        ' analyte result'
        ' It is useful to contextualize the result to each patient status '
        ' like age, sex, comorbidities, ...')
    units = fields.Many2One('gnuhealth.lab.test.units', 'Units')
    test_type_id = fields.Many2One(
        'gnuhealth.lab.test_type', 'Test type',
        select=True)
    gnuhealth_lab_id = fields.Many2One(
        'gnuhealth.lab', 'Test Cases',
        select=True)
    sequence = fields.Integer('Sequence')

    # Show the warning icon if warning is active on the analyte line
    lab_warning_icon = fields.Function(fields.Char(
        'Lab Warning Icon'),
        'get_lab_warning_icon')

    def get_lab_warning_icon(self, name):
        if (self.warning):
            return 'gnuhealth-warning'

    @classmethod
    def __setup__(cls):
        super(GnuHealthTestCritearea, cls).__setup__()
        cls._order.insert(0, ('sequence', 'ASC'))

    @staticmethod
    def default_sequence():
        return 1

    @staticmethod
    def default_excluded():
        return False

    @fields.depends('result', 'lower_limit', 'upper_limit')
    def on_change_with_warning(self):
        if (self.result and self.lower_limit):
            if (self.result < self.lower_limit):
                return True

        if (self.result and self.upper_limit):
            if (self.result > self.upper_limit):
                return True

    @classmethod
    def check_xml_record(cls, records, values):
        return True


class GnuHealthPatientLabTest(ModelSQL, ModelView):
    'Lab Test Request'
    __name__ = 'gnuhealth.patient.lab.test'

    name = fields.Many2One(
        'gnuhealth.lab.test_type', 'Test Type',
        required=True, select=True)
    date = fields.DateTime('Date', select=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('tested', 'Tested'),
        ('ordered', 'Ordered'),
        ('cancel', 'Cancel'),
        ], 'State', readonly=True, select=True)
    patient_id = fields.Many2One(
        'gnuhealth.patient', 'Patient', required=True,
        select=True)
    doctor_id = fields.Many2One(
        'gnuhealth.healthprofessional', 'Health prof.',
        help="Health professional who requests the lab test.", select=True)
    context = fields.Many2One(
        'gnuhealth.pathology', 'Context',
        help="Health context for this order. It can be a suspected or"
             " existing health condition, a regular health checkup, ...",
             select=True)
    request = fields.Integer('Order', readonly=True)
    urgent = fields.Boolean('Urgent')

    @classmethod
    def __setup__(cls):
        super(GnuHealthPatientLabTest, cls).__setup__()
        cls._order.insert(0, ('date', 'DESC'))
        cls._order.insert(1, ('request', 'DESC'))
        cls._order.insert(2, ('name', 'ASC'))

    @staticmethod
    def default_date():
        return datetime.now()

    @staticmethod
    def default_state():
        return 'draft'

    @staticmethod
    def default_doctor_id():
        return get_health_professional()

    @classmethod
    def generate_code(cls, **pattern):
        Config = Pool().get('gnuhealth.sequences')
        config = Config(1)
        sequence = config.get_multivalue(
            'lab_request_sequence', **pattern)
        if sequence:
            return sequence.get()

    @classmethod
    def create(cls, vlist):
        vlist = [x.copy() for x in vlist]
        for values in vlist:
            if not values.get('name'):
                values['name'] = cls.generate_code()

        return super(GnuHealthPatientLabTest, cls).create(vlist)

    @classmethod
    def copy(cls, tests, default=None):
        if default is None:
            default = {}
        default = default.copy()
        default['request'] = None
        default['date'] = cls.default_date()
        return super(GnuHealthPatientLabTest, cls).copy(
            tests, default=default)


class PatientHealthCondition(ModelSQL, ModelView):
    'Patient Conditions History'
    __name__ = 'gnuhealth.patient.disease'

    # Adds lab confirmed and the link to the test to the
    # Patient health Condition

    lab_confirmed = fields.Boolean(
        'Lab Confirmed', help='Confirmed by'
        ' laboratory test')

    lab_test = fields.Many2One(
        'gnuhealth.lab', 'Lab Test',
        domain=[('patient', '=', Eval('name'))], depends=['name'],
        states={'invisible': Not(Bool(Eval('lab_confirmed')))},
        help='Lab test that confirmed the condition')
