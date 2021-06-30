# This file is part health_dentistry module for GNU Health HMIS component
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
import json

from trytond.model import ModelView, fields
from trytond.wizard import Wizard, StateView, StateTransition, Button
from trytond.pool import Pool
from trytond.transaction import Transaction
from trytond.pyson import Eval, In
from ..health_dentistry import TOOTH_STATE

__all__ = ['SetOdontogramStart', 'SetOdontogram']


permanent = [
    '11', '12', '13', '14', '15', '16', '17', '18',
    '21', '22', '23', '24', '25', '26', '27', '28',
    '31', '32', '33', '34', '35', '36', '37', '38',
    '41', '42', '43', '44', '45', '46', '47', '48'
    ]

primary = [
    '51', '52', '53', '54', '55',
    '61', '62', '63', '64', '65',
    '71', '72', '73', '74', '75',
    '81', '82', '83', '84', '85'
    ]

permanent_surfaces = [
    ('vimdp', ['11', '12', '13', '21', '22', '23']),
    ('vomdp', ['14', '15', '16', '17', '18', '24', '25', '26', '27', '28']),
    ('vimdl', ['31', '32', '33', '41', '42', '43']),
    ('vomdl', ['34', '35', '36', '37', '38', '44', '45', '46', '47', '48'])
    ]

primary_surfaces = [
    ('vimdp', ['51', '52', '53', '61', '62', '63']),
    ('vomdp', ['54', '55', '64', '65']),
    ('vimdl', ['71', '72', '73', '81', '82', '83']),
    ('vomdl', ['74', '75', '84', '85'])
    ]


def tooth_surface(label, help, tooth):
    return fields.Boolean(label, help=help,
                          states={'readonly': ~In(Eval(tooth), ['D', 'F'])},
                          depends=[tooth])


class SetOdontogramStart(ModelView):
    'Set Odontogram Start'
    __name__ = 'gnuhealth.dentistry.set.odontogram.start'

    include_primary = fields.Boolean('Include Primary')
    t11 = fields.Selection(TOOTH_STATE, '11', sort=False)
    v11 = tooth_surface('V', 'Vestibular', 't11')
    i11 = tooth_surface('I', 'Incisal', 't11')
    m11 = tooth_surface('M', 'Mesial', 't11')
    d11 = tooth_surface('D', 'Distal', 't11')
    p11 = tooth_surface('P', 'Palatine', 't11')
    t12 = fields.Selection(TOOTH_STATE, '12', sort=False)
    v12 = tooth_surface('V', 'Vestibular', 't12')
    i12 = tooth_surface('I', 'Incisal', 't12')
    m12 = tooth_surface('M', 'Mesial', 't12')
    d12 = tooth_surface('D', 'Distal', 't12')
    p12 = tooth_surface('P', 'Palatine', 't12')
    t13 = fields.Selection(TOOTH_STATE, '13', sort=False)
    v13 = tooth_surface('V', 'Vestibular', 't13')
    i13 = tooth_surface('I', 'Incisal', 't13')
    m13 = tooth_surface('M', 'Mesial', 't13')
    d13 = tooth_surface('D', 'Distal', 't13')
    p13 = tooth_surface('P', 'Palatine', 't13')
    t14 = fields.Selection(TOOTH_STATE, '14', sort=False)
    v14 = tooth_surface('V', 'Vestibular', 't14')
    o14 = tooth_surface('O', 'Occlusal', 't14')
    m14 = tooth_surface('M', 'Mesial', 't14')
    d14 = tooth_surface('D', 'Distal', 't14')
    p14 = tooth_surface('P', 'Palatine', 't14')
    t15 = fields.Selection(TOOTH_STATE, '15', sort=False)
    v15 = tooth_surface('V', 'Vestibular', 't15')
    o15 = tooth_surface('O', 'Occlusal', 't15')
    m15 = tooth_surface('M', 'Mesial', 't15')
    d15 = tooth_surface('D', 'Distal', 't15')
    p15 = tooth_surface('P', 'Palatine', 't15')
    t16 = fields.Selection(TOOTH_STATE, '16', sort=False)
    v16 = tooth_surface('V', 'Vestibular', 't16')
    o16 = tooth_surface('O', 'Occlusal', 't16')
    m16 = tooth_surface('M', 'Mesial', 't16')
    d16 = tooth_surface('D', 'Distal', 't16')
    p16 = tooth_surface('P', 'Palatine', 't16')
    t17 = fields.Selection(TOOTH_STATE, '17', sort=False)
    v17 = tooth_surface('V', 'Vestibular', 't17')
    o17 = tooth_surface('O', 'Occlusal', 't17')
    m17 = tooth_surface('M', 'Mesial', 't17')
    d17 = tooth_surface('D', 'Distal', 't17')
    p17 = tooth_surface('P', 'Palatine', 't17')
    t18 = fields.Selection(TOOTH_STATE, '18', sort=False)
    v18 = tooth_surface('V', 'Vestibular', 't18')
    o18 = tooth_surface('O', 'Occlusal', 't18')
    m18 = tooth_surface('M', 'Mesial', 't18')
    d18 = tooth_surface('D', 'Distal', 't18')
    p18 = tooth_surface('P', 'Palatine', 't18')
    t21 = fields.Selection(TOOTH_STATE, '21', sort=False)
    v21 = tooth_surface('V', 'Vestibular', 't21')
    i21 = tooth_surface('I', 'Incisal', 't21')
    m21 = tooth_surface('M', 'Mesial', 't21')
    d21 = tooth_surface('D', 'Distal', 't21')
    p21 = tooth_surface('P', 'Palatine', 't21')
    t22 = fields.Selection(TOOTH_STATE, '22', sort=False)
    v22 = tooth_surface('V', 'Vestibular', 't22')
    i22 = tooth_surface('I', 'Incisal', 't22')
    m22 = tooth_surface('M', 'Mesial', 't22')
    d22 = tooth_surface('D', 'Distal', 't22')
    p22 = tooth_surface('P', 'Palatine', 't22')
    t23 = fields.Selection(TOOTH_STATE, '23', sort=False)
    v23 = tooth_surface('V', 'Vestibular', 't23')
    i23 = tooth_surface('I', 'Incisal', 't23')
    m23 = tooth_surface('M', 'Mesial', 't23')
    d23 = tooth_surface('D', 'Distal', 't23')
    p23 = tooth_surface('P', 'Palatine', 't23')
    t24 = fields.Selection(TOOTH_STATE, '24', sort=False)
    v24 = tooth_surface('V', 'Vestibular', 't24')
    o24 = tooth_surface('O', 'Occlusal', 't24')
    m24 = tooth_surface('M', 'Mesial', 't24')
    d24 = tooth_surface('D', 'Distal', 't24')
    p24 = tooth_surface('P', 'Palatine', 't24')
    t25 = fields.Selection(TOOTH_STATE, '25', sort=False)
    v25 = tooth_surface('V', 'Vestibular', 't25')
    o25 = tooth_surface('O', 'Occlusal', 't25')
    m25 = tooth_surface('M', 'Mesial', 't25')
    d25 = tooth_surface('D', 'Distal', 't25')
    p25 = tooth_surface('P', 'Palatine', 't25')
    t26 = fields.Selection(TOOTH_STATE, '26', sort=False)
    v26 = tooth_surface('V', 'Vestibular', 't26')
    o26 = tooth_surface('O', 'Occlusal', 't26')
    m26 = tooth_surface('M', 'Mesial', 't26')
    d26 = tooth_surface('D', 'Distal', 't26')
    p26 = tooth_surface('P', 'Palatine', 't26')
    t27 = fields.Selection(TOOTH_STATE, '27', sort=False)
    v27 = tooth_surface('V', 'Vestibular', 't27')
    o27 = tooth_surface('O', 'Occlusal', 't27')
    m27 = tooth_surface('M', 'Mesial', 't27')
    d27 = tooth_surface('D', 'Distal', 't27')
    p27 = tooth_surface('P', 'Palatine', 't27')
    t28 = fields.Selection(TOOTH_STATE, '28', sort=False)
    v28 = tooth_surface('V', 'Vestibular', 't28')
    o28 = tooth_surface('O', 'Occlusal', 't28')
    m28 = tooth_surface('M', 'Mesial', 't28')
    d28 = tooth_surface('D', 'Distal', 't28')
    p28 = tooth_surface('P', 'Palatine', 't28')
    t31 = fields.Selection(TOOTH_STATE, '31', sort=False)
    v31 = tooth_surface('V', 'Vestibular', 't31')
    i31 = tooth_surface('I', 'Incisal', 't31')
    m31 = tooth_surface('M', 'Mesial', 't31')
    d31 = tooth_surface('D', 'Distal', 't31')
    l31 = tooth_surface('L', 'Lingual', 't31')
    t32 = fields.Selection(TOOTH_STATE, '32', sort=False)
    v32 = tooth_surface('V', 'Vestibular', 't32')
    i32 = tooth_surface('I', 'Incisal', 't32')
    m32 = tooth_surface('M', 'Mesial', 't32')
    d32 = tooth_surface('D', 'Distal', 't32')
    l32 = tooth_surface('L', 'Lingual', 't32')
    t33 = fields.Selection(TOOTH_STATE, '33', sort=False)
    v33 = tooth_surface('V', 'Vestibular', 't33')
    i33 = tooth_surface('I', 'Incisal', 't33')
    m33 = tooth_surface('M', 'Mesial', 't33')
    d33 = tooth_surface('D', 'Distal', 't33')
    l33 = tooth_surface('L', 'Lingual', 't33')
    t34 = fields.Selection(TOOTH_STATE, '34', sort=False)
    v34 = tooth_surface('V', 'Vestibular', 't34')
    o34 = tooth_surface('O', 'Occlusal', 't34')
    m34 = tooth_surface('M', 'Mesial', 't34')
    d34 = tooth_surface('D', 'Distal', 't34')
    l34 = tooth_surface('L', 'Lingual', 't34')
    t35 = fields.Selection(TOOTH_STATE, '35', sort=False)
    v35 = tooth_surface('V', 'Vestibular', 't35')
    o35 = tooth_surface('O', 'Occlusal', 't35')
    m35 = tooth_surface('M', 'Mesial', 't35')
    d35 = tooth_surface('D', 'Distal', 't35')
    l35 = tooth_surface('L', 'Lingual', 't35')
    t36 = fields.Selection(TOOTH_STATE, '36', sort=False)
    v36 = tooth_surface('V', 'Vestibular', 't36')
    o36 = tooth_surface('O', 'Occlusal', 't36')
    m36 = tooth_surface('M', 'Mesial', 't36')
    d36 = tooth_surface('D', 'Distal', 't36')
    l36 = tooth_surface('L', 'Lingual', 't36')
    t37 = fields.Selection(TOOTH_STATE, '37', sort=False)
    v37 = tooth_surface('V', 'Vestibular', 't37')
    o37 = tooth_surface('O', 'Occlusal', 't37')
    m37 = tooth_surface('M', 'Mesial', 't37')
    d37 = tooth_surface('D', 'Distal', 't37')
    l37 = tooth_surface('L', 'Lingual', 't37')
    t38 = fields.Selection(TOOTH_STATE, '38', sort=False)
    v38 = tooth_surface('V', 'Vestibular', 't38')
    o38 = tooth_surface('O', 'Occlusal', 't38')
    m38 = tooth_surface('M', 'Mesial', 't38')
    d38 = tooth_surface('D', 'Distal', 't38')
    l38 = tooth_surface('L', 'Lingual', 't38')
    t41 = fields.Selection(TOOTH_STATE, '41', sort=False)
    v41 = tooth_surface('V', 'Vestibular', 't41')
    i41 = tooth_surface('I', 'Incisal', 't41')
    m41 = tooth_surface('M', 'Mesial', 't41')
    d41 = tooth_surface('D', 'Distal', 't41')
    l41 = tooth_surface('L', 'Lingual', 't41')
    t42 = fields.Selection(TOOTH_STATE, '42', sort=False)
    v42 = tooth_surface('V', 'Vestibular', 't42')
    i42 = tooth_surface('I', 'Incisal', 't42')
    m42 = tooth_surface('M', 'Mesial', 't42')
    d42 = tooth_surface('D', 'Distal', 't42')
    l42 = tooth_surface('L', 'Lingual', 't42')
    t43 = fields.Selection(TOOTH_STATE, '43', sort=False)
    v43 = tooth_surface('V', 'Vestibular', 't43')
    i43 = tooth_surface('I', 'Incisal', 't43')
    m43 = tooth_surface('M', 'Mesial', 't43')
    d43 = tooth_surface('D', 'Distal', 't43')
    l43 = tooth_surface('L', 'Lingual', 't43')
    t44 = fields.Selection(TOOTH_STATE, '44', sort=False)
    v44 = tooth_surface('V', 'Vestibular', 't44')
    o44 = tooth_surface('O', 'Occlusal', 't44')
    m44 = tooth_surface('M', 'Mesial', 't44')
    d44 = tooth_surface('D', 'Distal', 't44')
    l44 = tooth_surface('L', 'Lingual', 't44')
    t45 = fields.Selection(TOOTH_STATE, '45', sort=False)
    v45 = tooth_surface('V', 'Vestibular', 't45')
    o45 = tooth_surface('O', 'Occlusal', 't45')
    m45 = tooth_surface('M', 'Mesial', 't45')
    d45 = tooth_surface('D', 'Distal', 't45')
    l45 = tooth_surface('L', 'Lingual', 't45')
    t46 = fields.Selection(TOOTH_STATE, '46', sort=False)
    v46 = tooth_surface('V', 'Vestibular', 't46')
    o46 = tooth_surface('O', 'Occlusal', 't46')
    m46 = tooth_surface('M', 'Mesial', 't46')
    d46 = tooth_surface('D', 'Distal', 't46')
    l46 = tooth_surface('L', 'Lingual', 't46')
    t47 = fields.Selection(TOOTH_STATE, '47', sort=False)
    v47 = tooth_surface('V', 'Vestibular', 't47')
    o47 = tooth_surface('O', 'Occlusal', 't47')
    m47 = tooth_surface('M', 'Mesial', 't47')
    d47 = tooth_surface('D', 'Distal', 't47')
    l47 = tooth_surface('L', 'Lingual', 't47')
    t48 = fields.Selection(TOOTH_STATE, '48', sort=False)
    v48 = tooth_surface('V', 'Vestibular', 't48')
    o48 = tooth_surface('O', 'Occlusal', 't48')
    m48 = tooth_surface('M', 'Mesial', 't48')
    d48 = tooth_surface('D', 'Distal', 't48')
    l48 = tooth_surface('L', 'Lingual', 't48')
    t51 = fields.Selection(TOOTH_STATE, '51', sort=False)
    v51 = tooth_surface('V', 'Vestibular', 't51')
    i51 = tooth_surface('I', 'Incisal', 't51')
    m51 = tooth_surface('M', 'Mesial', 't51')
    d51 = tooth_surface('D', 'Distal', 't51')
    p51 = tooth_surface('P', 'Palatine', 't51')
    t52 = fields.Selection(TOOTH_STATE, '52', sort=False)
    v52 = tooth_surface('V', 'Vestibular', 't52')
    i52 = tooth_surface('I', 'Incisal', 't52')
    m52 = tooth_surface('M', 'Mesial', 't52')
    d52 = tooth_surface('D', 'Distal', 't52')
    p52 = tooth_surface('P', 'Palatine', 't52')
    t53 = fields.Selection(TOOTH_STATE, '53', sort=False)
    v53 = tooth_surface('V', 'Vestibular', 't53')
    i53 = tooth_surface('I', 'Incisal', 't53')
    m53 = tooth_surface('M', 'Mesial', 't53')
    d53 = tooth_surface('D', 'Distal', 't53')
    p53 = tooth_surface('P', 'Palatine', 't53')
    t54 = fields.Selection(TOOTH_STATE, '54', sort=False)
    v54 = tooth_surface('V', 'Vestibular', 't54')
    o54 = tooth_surface('O', 'Occlusal', 't54')
    m54 = tooth_surface('M', 'Mesial', 't54')
    d54 = tooth_surface('D', 'Distal', 't54')
    p54 = tooth_surface('P', 'Palatine', 't54')
    t55 = fields.Selection(TOOTH_STATE, '55', sort=False)
    v55 = tooth_surface('V', 'Vestibular', 't55')
    o55 = tooth_surface('O', 'Occlusal', 't55')
    m55 = tooth_surface('M', 'Mesial', 't55')
    d55 = tooth_surface('D', 'Distal', 't55')
    p55 = tooth_surface('P', 'Palatine', 't55')
    t61 = fields.Selection(TOOTH_STATE, '61', sort=False)
    v61 = tooth_surface('V', 'Vestibular', 't61')
    i61 = tooth_surface('I', 'Incisal', 't61')
    m61 = tooth_surface('M', 'Mesial', 't61')
    d61 = tooth_surface('D', 'Distal', 't61')
    p61 = tooth_surface('P', 'Palatine', 't61')
    t62 = fields.Selection(TOOTH_STATE, '62', sort=False)
    v62 = tooth_surface('V', 'Vestibular', 't62')
    i62 = tooth_surface('I', 'Incisal', 't62')
    m62 = tooth_surface('M', 'Mesial', 't62')
    d62 = tooth_surface('D', 'Distal', 't62')
    p62 = tooth_surface('P', 'Palatine', 't62')
    t63 = fields.Selection(TOOTH_STATE, '63', sort=False)
    v63 = tooth_surface('V', 'Vestibular', 't63')
    i63 = tooth_surface('I', 'Incisal', 't63')
    m63 = tooth_surface('M', 'Mesial', 't63')
    d63 = tooth_surface('D', 'Distal', 't63')
    p63 = tooth_surface('P', 'Palatine', 't63')
    t64 = fields.Selection(TOOTH_STATE, '64', sort=False)
    v64 = tooth_surface('V', 'Vestibular', 't64')
    o64 = tooth_surface('O', 'Occlusal', 't64')
    m64 = tooth_surface('M', 'Mesial', 't64')
    d64 = tooth_surface('D', 'Distal', 't64')
    p64 = tooth_surface('P', 'Palatine', 't64')
    t65 = fields.Selection(TOOTH_STATE, '65', sort=False)
    v65 = tooth_surface('V', 'Vestibular', 't65')
    o65 = tooth_surface('O', 'Occlusal', 't65')
    m65 = tooth_surface('M', 'Mesial', 't65')
    d65 = tooth_surface('D', 'Distal', 't65')
    p65 = tooth_surface('P', 'Palatine', 't65')
    t71 = fields.Selection(TOOTH_STATE, '71', sort=False)
    v71 = tooth_surface('V', 'Vestibular', 't71')
    i71 = tooth_surface('I', 'Incisal', 't71')
    m71 = tooth_surface('M', 'Mesial', 't71')
    d71 = tooth_surface('D', 'Distal', 't71')
    l71 = tooth_surface('L', 'Lingual', 't71')
    t72 = fields.Selection(TOOTH_STATE, '72', sort=False)
    v72 = tooth_surface('V', 'Vestibular', 't72')
    i72 = tooth_surface('I', 'Incisal', 't72')
    m72 = tooth_surface('M', 'Mesial', 't72')
    d72 = tooth_surface('D', 'Distal', 't72')
    l72 = tooth_surface('L', 'Lingual', 't72')
    t73 = fields.Selection(TOOTH_STATE, '73', sort=False)
    v73 = tooth_surface('V', 'Vestibular', 't73')
    i73 = tooth_surface('I', 'Incisal', 't73')
    m73 = tooth_surface('M', 'Mesial', 't73')
    d73 = tooth_surface('D', 'Distal', 't73')
    l73 = tooth_surface('L', 'Lingual', 't73')
    t74 = fields.Selection(TOOTH_STATE, '74', sort=False)
    v74 = tooth_surface('V', 'Vestibular', 't74')
    o74 = tooth_surface('O', 'Occlusal', 't74')
    m74 = tooth_surface('M', 'Mesial', 't74')
    d74 = tooth_surface('D', 'Distal', 't74')
    l74 = tooth_surface('L', 'Lingual', 't74')
    t75 = fields.Selection(TOOTH_STATE, '75', sort=False)
    v75 = tooth_surface('V', 'Vestibular', 't75')
    o75 = tooth_surface('O', 'Occlusal', 't75')
    m75 = tooth_surface('M', 'Mesial', 't75')
    d75 = tooth_surface('D', 'Distal', 't75')
    l75 = tooth_surface('L', 'Lingual', 't75')
    t81 = fields.Selection(TOOTH_STATE, '81', sort=False)
    v81 = tooth_surface('V', 'Vestibular', 't81')
    i81 = tooth_surface('I', 'Incisal', 't81')
    m81 = tooth_surface('M', 'Mesial', 't81')
    d81 = tooth_surface('D', 'Distal', 't81')
    l81 = tooth_surface('L', 'Lingual', 't81')
    t82 = fields.Selection(TOOTH_STATE, '82', sort=False)
    v82 = tooth_surface('V', 'Vestibular', 't82')
    i82 = tooth_surface('I', 'Incisal', 't82')
    m82 = tooth_surface('M', 'Mesial', 't82')
    d82 = tooth_surface('D', 'Distal', 't82')
    l82 = tooth_surface('L', 'Lingual', 't82')
    t83 = fields.Selection(TOOTH_STATE, '83', sort=False)
    v83 = tooth_surface('V', 'Vestibular', 't83')
    i83 = tooth_surface('I', 'Incisal', 't83')
    m83 = tooth_surface('M', 'Mesial', 't83')
    d83 = tooth_surface('D', 'Distal', 't83')
    l83 = tooth_surface('L', 'Lingual', 't83')
    t84 = fields.Selection(TOOTH_STATE, '84', sort=False)
    v84 = tooth_surface('V', 'Vestibular', 't84')
    o84 = tooth_surface('O', 'Occlusal', 't84')
    m84 = tooth_surface('M', 'Mesial', 't84')
    d84 = tooth_surface('D', 'Distal', 't84')
    l84 = tooth_surface('L', 'Lingual', 't84')
    t85 = fields.Selection(TOOTH_STATE, '85', sort=False)
    v85 = tooth_surface('V', 'Vestibular', 't85')
    o85 = tooth_surface('O', 'Occlusal', 't85')
    m85 = tooth_surface('M', 'Mesial', 't85')
    d85 = tooth_surface('D', 'Distal', 't85')
    l85 = tooth_surface('L', 'Lingual', 't85')

    @classmethod
    def view_attributes(cls):
        return super(SetOdontogramStart, cls).view_attributes() + [
            ('//page[@id="primary"]', 'states', {
                    'invisible': ~Eval('include_primary'),
                    })]


class SetOdontogram(Wizard):
    'Set Odontogram'
    __name__ = 'gnuhealth.dentistry.set.odontogram'

    start = StateView('gnuhealth.dentistry.set.odontogram.start',
                      'health_dentistry.set_odontogram_start_view_form',
                      [Button('Cancel', 'end', 'tryton-cancel'),
                       Button('Set', 'set_', 'tryton-ok', default=True)])
    set_ = StateTransition()

    def default_start(self, fields):
        pool = Pool()
        Patient = Pool().get('gnuhealth.patient')
        Treatment = pool.get('gnuhealth.dentistry.treatment')

        patient_id = Transaction().context.get('active_id')
        # Check if wizard called from treatment
        active_model = Transaction().context.get('active_model')
        if active_model == 'gnuhealth.dentistry.treatment':
            patient_id = Treatment.browse(
                [Transaction().context.get('active_id')])[0].patient

        if not patient_id:
            return {}
        res = {
            'include_primary': False,
            't11': '', 't12': '', 't13': '', 't14': '',
            't15': '', 't16': '', 't17': '', 't18': '',
            't21': '', 't22': '', 't23': '', 't24': '',
            't25': '', 't26': '', 't27': '', 't28': '',
            't31': '', 't32': '', 't33': '', 't34': '',
            't35': '', 't36': '', 't37': '', 't38': '',
            't41': '', 't42': '', 't43': '', 't44': '',
            't45': '', 't46': '', 't47': '', 't48': '',
            't51': '', 't52': '', 't53': '', 't54': '', 't55': '',
            't61': '', 't62': '', 't63': '', 't64': '', 't65': '',
            't71': '', 't72': '', 't73': '', 't74': '', 't75': '',
            't81': '', 't82': '', 't83': '', 't84': '', 't85': '',
            }
        patient = Patient.browse([patient_id])
        if patient:
            if patient[0].use_primary_schema:
                res.update({'include_primary': True})
            if patient[0].dental_schema:
                teeth = json.loads(patient[0].dental_schema)
                for t in permanent:
                    res['t' + t] = teeth[t]['ts']
                for ps in permanent_surfaces:
                    for i in range(0, 5):
                        for t in ps[1]:
                            value = teeth[t].get(ps[0][i], False)
                            res[ps[0][i] + t] = True if value else False

            if patient[0].dental_schema_primary:
                teeth = json.loads(patient[0].dental_schema_primary)
                for t in primary:
                    res['t' + t] = teeth[t]['ts']
                for ps in primary_surfaces:
                    for i in range(0, 5):
                        for t in ps[1]:
                            value = teeth[t].get(ps[0][i], False)
                            res[ps[0][i] + t] = True if value else False

        return res

    def transition_set_(self):
        pool = Pool()
        Patient = Pool().get('gnuhealth.patient')
        Treatment = pool.get('gnuhealth.dentistry.treatment')

        patient_id = Transaction().context.get('active_id')
        # Check if wizard called from treatment
        active_model = Transaction().context.get('active_model')
        if active_model == 'gnuhealth.dentistry.treatment':
            patient_id = Treatment.browse(
                [Transaction().context.get('active_id')])[0].patient

        if not patient_id:
            return 'end'

        data = {}
        for t in permanent:
            data[t] = {'ts': getattr(self.start, 't' + t)}
        for ps in permanent_surfaces:
            for i in range(0, 5):
                for t in ps[1]:
                    value = getattr(self.start, ps[0][i] + t, None)
                    if value and data[t]['ts'] in ['D', 'F']:
                        data[t].update({ps[0][i]: 'x'})

        primary_data = {}
        for t in primary:
            primary_data[t] = {'ts': getattr(self.start, 't' + t)}
        for ps in primary_surfaces:
            for i in range(0, 5):
                for t in ps[1]:
                    value = getattr(self.start, ps[0][i] + t, None)
                    if value and primary_data[t]['ts'] in ['D', 'F']:
                        primary_data[t].update({ps[0][i]: 'x'})

        dental_schema = json.dumps(data)
        dental_schema_primary = json.dumps(primary_data)
        patient = Patient(patient_id)
        patient.dental_schema = dental_schema
        patient.dental_schema_primary = dental_schema_primary
        Patient.save([patient])
        return 'end'
