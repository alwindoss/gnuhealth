##############################################################################
#
#    GNU Health. Hospital Information System (HIS) component.
#
#                       ***  Dentistry Package  ***
#
#    Copyright (C) 2020-2021 National University of Entre Rios (UNER)
#    School of Engineering <saludpublica@ingenieria.uner.edu.ar>
#    Copyright (C) 2020 Mario Puntin <mario@silix.com.ar>
#    Copyright (C) 2020-2022 GNU Solidario <health@gnusolidario.org>
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
import json
from datetime import date
from collections import defaultdict

from trytond.model import ModelView, ModelSQL, fields, Unique
from trytond.pyson import Eval, Equal
from trytond.pool import PoolMeta

from trytond.modules.health.core import get_health_professional

__all__ = ['PatientData', 'DentistryTreatment', 'DentistryProcedure',
           'TreatmentProcedure']


TOOTH_STATE = [
    ('', ''),
    ('D', 'Decayed'),
    ('M', 'Missing'),
    ('F', 'Filled'),
    ('E', 'For Extraction'),
    ]

STATE_LEGENDS = {
    '': '      ',
    'D': '  *  ',
    'M': '  X  ',
    'F': '  #  ',
    'E': '  =  '
    }

TEETH = [
    ('11', '11'), ('12', '12'), ('13', '13'), ('14', '14'),
    ('15', '15'), ('16', '16'), ('17', '17'), ('18', '18'),
    ('21', '21'), ('22', '22'), ('23', '23'), ('24', '24'),
    ('25', '25'), ('26', '26'), ('27', '27'), ('28', '28'),
    ('31', '31'), ('32', '32'), ('33', '33'), ('34', '34'),
    ('35', '35'), ('36', '36'), ('37', '37'), ('38', '38'),
    ('41', '41'), ('42', '42'), ('43', '43'), ('44', '44'),
    ('45', '45'), ('46', '46'), ('47', '47'), ('48', '48'),
    ('51', '51'), ('52', '52'), ('53', '53'), ('54', '54'), ('55', '55'),
    ('61', '61'), ('62', '62'), ('63', '63'), ('64', '64'), ('65', '65'),
    ('71', '71'), ('72', '72'), ('73', '73'), ('74', '74'), ('75', '75'),
    ('81', '81'), ('82', '82'), ('83', '83'), ('84', '84'), ('85', '85'),
    ]

TREATMENT_TEETH = TEETH + [(None, '')]


class PatientData (metaclass=PoolMeta):
    __name__ = 'gnuhealth.patient'

    dentistry_treatments = fields.One2Many(
        'gnuhealth.dentistry.treatment',
        'patient', 'Treatment', readonly=True)
    dental_schema = fields.Text('Dental Schema')
    dental_schema_primary = fields.Text('Primary Schema')
    teeth1 = fields.Function(fields.Char('Quadrant 1'), 'get_status')
    teeth2 = fields.Function(fields.Char('Quadrant 2'), 'get_status')
    teeth3 = fields.Function(fields.Char('Quadrant 3'), 'get_status')
    teeth4 = fields.Function(fields.Char('Quadrant 4'), 'get_status')
    use_primary_schema = fields.Boolean('Primary Schema',
                                        help='Use Primary Schema')
    teeth5 = fields.Function(fields.Char('Quadrant 5'), 'get_status_primary')
    teeth6 = fields.Function(fields.Char('Quadrant 6'), 'get_status_primary')
    teeth7 = fields.Function(fields.Char('Quadrant 7'), 'get_status_primary')
    teeth8 = fields.Function(fields.Char('Quadrant 8'), 'get_status_primary')
    dmft_index = fields.Function(fields.Integer('DMFT Index'),
                                 'get_dmft_index')
    dmft_index_primary = fields.Function(
        fields.Integer('dmft index', help='dmft index for primary teeth',
                       states={'invisible': ~Eval('use_primary_schema')}),
        'get_dmft_index_primary')

    @classmethod
    def __setup__(cls):
        super(PatientData, cls).__setup__()
        cls._buttons.update({
                'set_odontogram_wizard': {
                    'readonly': Eval('deceased'),
                    },
                })

    @classmethod
    def view_attributes(cls):
        attributes = super(PatientData, cls).view_attributes()
        attributes.extend([
            ('///group[@id="dental_main_info"]/'
                'group[@id="dental_schema_primary"]',
             'states', {'invisible': ~Eval('use_primary_schema')})
            ])
        return attributes

    @staticmethod
    def default_use_primary_schema():
        return False

    @fields.depends('dental_schema')
    def get_status(self, name=None):
        if not self.dental_schema:
            return ''
        quad = name[5:]
        teeth = json.loads(self.dental_schema)
        res = ''
        loop = list(range(1, 9)) if quad in ['2', '3'] \
            else list(range(8, 0, -1))
        for i in loop:
            res += ' ' * 6 + quad + str(i) + ':' + \
                STATE_LEGENDS[teeth[quad + str(i)]['ts']]
        return res

    @fields.depends('dental_schema_primary')
    def get_status_primary(self, name=None):
        if not self.dental_schema_primary:
            return ''
        quad = name[5:]
        teeth = json.loads(self.dental_schema_primary)
        res = ' ' * 24
        loop = list(range(1, 6)) if quad in ['6', '7'] \
            else list(range(5, 0, -1))
        for i in loop:
            res += ' ' * 6 + quad + str(i) + ':' + \
                STATE_LEGENDS[teeth[quad + str(i)]['ts']]
        return res

    @fields.depends('dental_schema')
    def get_dmft_index(self, name=None):
        if not self.dental_schema:
            return None
        teeth = json.loads(self.dental_schema)
        res = 0
        quadrant = ['1', '2', '3', '4']
        tooth = ['1', '2', '3', '4', '5', '6', '7', '8']
        for q in quadrant:
            for t in tooth:
                if teeth[q + t]['ts'] in ['D', 'M', 'F']:
                    res += 1
        return res

    @fields.depends('dental_schema_primary')
    def get_dmft_index_primary(self, name=None):
        if not self.dental_schema_primary:
            return None
        teeth = json.loads(self.dental_schema_primary)
        res = 0
        quadrant = ['5', '6', '7', '8']
        tooth = ['1', '2', '3', '4', '5']
        for q in quadrant:
            for t in tooth:
                if teeth[q + t]['ts'] in ['D', 'M', 'F']:
                    res += 1
        return res

    @classmethod
    @ModelView.button_action('health_dentistry.wizard_set_odontogram')
    def set_odontogram_wizard(cls, patients):
        pass


class DentistryTreatment(ModelSQL, ModelView):
    'Dentistry Treatment'
    __name__ = 'gnuhealth.dentistry.treatment'

    STATES = {'readonly': Eval('state') == 'done'}

    patient = fields.Many2One('gnuhealth.patient', 'Patient', required=True)
    treatment_date = fields.Date('Date', states=STATES)
    healthprof = fields.Many2One('gnuhealth.healthprofessional',
                                 'Health Prof', help="Health professional",
                                 states=STATES)
    procedures = fields.One2Many('gnuhealth.dentistry.treatment.procedure',
                                 'treatment', 'Procedures', states=STATES)
    notes = fields.Text('Notes', help="Extra Information", states=STATES)
    procedures_info = fields.Function(fields.Char("Procedures info"),
                                      'get_procedures_info')
    signed_by = fields.Many2One(
        'gnuhealth.healthprofessional',
        'Signed by', readonly=True,
        states={'invisible': Equal(Eval('state'),
                                   'pending')},
        help="Health Professional that finished the treatment")
    state = fields.Selection([
        ('pending', 'Pending'),
        ('done', 'Done'),
        ], 'State', readonly=True, sort=False)
    state_string = state.translated('state')

    @classmethod
    def __setup__(cls):
        super(DentistryTreatment, cls).__setup__()
        cls._order.insert(0, ('id', 'DESC'))
        cls._buttons.update({
            'load_procedure': {
                'readonly': ~Eval('state').in_(['pending']),
                },
            'set_odontogram': {
                'readonly': ~Eval('state').in_(['pending']),
                    },
            'end_treatment': {
                'invisible': Equal(Eval('state'), 'done')
                },
            })

    @classmethod
    @ModelView.button_action('health_dentistry.load_procedure')
    def load_procedure(cls, treatments):
        pass

    @classmethod
    @ModelView.button_action('health_dentistry.wizard_set_odontogram')
    def set_odontogram(cls, treatments):
        pass

    @staticmethod
    def default_treatment_date():
        return date.today()

    @staticmethod
    def default_state():
        return 'pending'

    @staticmethod
    def default_healthprof():
        return get_health_professional()

    @classmethod
    def get_procedures_info(cls, treatments, names):
        result = {
            'procedures_info': {}
            }
        for t in treatments:
            data = defaultdict(list)
            info = []
            for p in t.procedures:
                data[p.procedure.code].append(p.tooth if p.tooth else '')
            for k, v in data.items():
                info.append(k + ' (' + ', '.join(v) + ')')
            result['procedures_info'][t.id] = ', '.join(info)
        return result

    @classmethod
    @ModelView.button
    def end_treatment(cls, treatments):
        signing_hp = get_health_professional()
        cls.write(treatments, {
            'state': 'done',
            'signed_by': signing_hp,
            })


class DentistryProcedure(ModelSQL, ModelView):
    'Dentistry Procedure'
    __name__ = 'gnuhealth.dentistry.procedure'

    name = fields.Char('Procedure', required=True, translate=True)
    code = fields.Char(
        'Code', required=True, translate=True,
        help='Please use CAPITAL LETTERS and no spaces')

    @classmethod
    def __setup__(cls):
        t = cls.__table__()
        cls._sql_constraints = [
            ('name_uniq', Unique(t, t.name),
                'The Procedure must be unique !'),
            ('code_uniq', Unique(t, t.code),
                'The CODE must be unique !'),
        ]
        super(DentistryProcedure, cls).__setup__()


class TreatmentProcedure(ModelSQL, ModelView):
    'Treatment Procedure'
    __name__ = 'gnuhealth.dentistry.treatment.procedure'

    treatment = fields.Many2One('gnuhealth.dentistry.treatment', 'Treatment',
                                required=True)
    tooth = fields.Selection(TREATMENT_TEETH, 'Tooth')
    procedure = fields.Many2One('gnuhealth.dentistry.procedure', 'Procedure',
                                required=True)
    root = fields.Boolean('Root')
    occlusal = fields.Boolean('Occlusal')
    vestibular = fields.Boolean('Vestibular')
    lingual = fields.Boolean('Lingual')
    mesial = fields.Boolean('Mesial')
    distal = fields.Boolean('Distal')

    @classmethod
    def __setup__(cls):
        super(TreatmentProcedure, cls).__setup__()
        cls._order.insert(0, ('procedure', 'ASC'))
        cls._order.insert(1, ('tooth', 'ASC'))
