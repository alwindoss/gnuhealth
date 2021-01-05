from trytond.model import ModelView, fields
from trytond.wizard import Wizard, StateView, StateTransition, Button
from trytond.pool import Pool
from trytond.transaction import Transaction
from trytond.pyson import Eval

__all__ = ['LoadProcedureStart', 'LoadProcedure']


class LoadProcedureStart(ModelView):
    'Load Procedure Start'
    __name__ = 'gnuhealth.dentistry.load.procedure.start'

    procedure = fields.Many2One('gnuhealth.dentistry.procedure',
                                'Procedure', required=True)
    root = fields.Boolean('Root')
    occlusal = fields.Boolean('Occlusal')
    vestibular = fields.Boolean('Vestibular')
    lingual = fields.Boolean('Lingual')
    mesial = fields.Boolean('Mesial')
    distal = fields.Boolean('Distal')
    include_primary = fields.Boolean('Include Primary')
    tooth11 = fields.Boolean('11')
    tooth12 = fields.Boolean('12')
    tooth13 = fields.Boolean('13')
    tooth14 = fields.Boolean('14')
    tooth15 = fields.Boolean('15')
    tooth16 = fields.Boolean('16')
    tooth17 = fields.Boolean('17')
    tooth18 = fields.Boolean('18')
    tooth21 = fields.Boolean('21')
    tooth22 = fields.Boolean('22')
    tooth23 = fields.Boolean('23')
    tooth24 = fields.Boolean('24')
    tooth25 = fields.Boolean('25')
    tooth26 = fields.Boolean('26')
    tooth27 = fields.Boolean('27')
    tooth28 = fields.Boolean('28')
    tooth31 = fields.Boolean('31')
    tooth32 = fields.Boolean('32')
    tooth33 = fields.Boolean('33')
    tooth34 = fields.Boolean('34')
    tooth35 = fields.Boolean('35')
    tooth36 = fields.Boolean('36')
    tooth37 = fields.Boolean('37')
    tooth38 = fields.Boolean('38')
    tooth41 = fields.Boolean('41')
    tooth42 = fields.Boolean('42')
    tooth43 = fields.Boolean('43')
    tooth44 = fields.Boolean('44')
    tooth45 = fields.Boolean('45')
    tooth46 = fields.Boolean('46')
    tooth47 = fields.Boolean('47')
    tooth48 = fields.Boolean('48')
    tooth51 = fields.Boolean('51')
    tooth52 = fields.Boolean('52')
    tooth53 = fields.Boolean('53')
    tooth54 = fields.Boolean('54')
    tooth55 = fields.Boolean('55')
    tooth61 = fields.Boolean('61')
    tooth62 = fields.Boolean('62')
    tooth63 = fields.Boolean('63')
    tooth64 = fields.Boolean('64')
    tooth65 = fields.Boolean('65')
    tooth71 = fields.Boolean('71')
    tooth72 = fields.Boolean('72')
    tooth73 = fields.Boolean('73')
    tooth74 = fields.Boolean('74')
    tooth75 = fields.Boolean('75')
    tooth81 = fields.Boolean('81')
    tooth82 = fields.Boolean('82')
    tooth83 = fields.Boolean('83')
    tooth84 = fields.Boolean('84')
    tooth85 = fields.Boolean('85')

    @classmethod
    def view_attributes(cls):
        return super(LoadProcedureStart, cls).view_attributes() + [
            ('//group[@id="primary"]', 'states', {
                    'invisible': ~Eval('include_primary'),
                    })]


class LoadProcedure(Wizard):
    'Load Units'
    __name__ = 'gnuhealth.dentistry.load.procedure'

    start = StateView('gnuhealth.dentistry.load.procedure.start',
                      'health_dentistry.load_procedure_start_view_form',
                      [Button('Cancel', 'end', 'tryton-cancel'),
                       Button('Load', 'load', 'tryton-ok', default=True)])
    load = StateTransition()

    def default_start(self, fields):
        pool = Pool()
        Treatment = pool.get('gnuhealth.dentistry.treatment')

        res = {'include_primary': False}
        treatment_id = Transaction().context.get('active_id')
        if not treatment_id:
            return res
        treatment = Treatment.browse([treatment_id])
        if treatment and treatment[0].patient.use_primary_schema:
            res = {'include_primary': True}
        return res

    def transition_load(self):
        pool = Pool()
        Procedure = pool.get('gnuhealth.dentistry.treatment.procedure')

        teeth = [
            '11', '12', '13', '14', '15', '16', '17', '18',
            '21', '22', '23', '24', '25', '26', '27', '28',
            '31', '32', '33', '34', '35', '36', '37', '38',
            '41', '42', '43', '44', '45', '46', '47', '48',
            '51', '52', '53', '54', '55'
            '61', '62', '63', '64', '65'
            '71', '72', '73', '74', '75'
            '81', '82', '83', '84', '85',
            ]
        procedures = []
        no_tooth = True
        for number in teeth:
            if getattr(self.start, 'tooth' + number, False):
                no_tooth = False
                data = {
                    'treatment': Transaction().context['active_id'],
                    'tooth': number,
                    'procedure': self.start.procedure,
                    'root': self.start.root,
                    'occlusal': self.start.occlusal,
                    'vestibular': self.start.vestibular,
                    'lingual': self.start.lingual,
                    'mesial': self.start.mesial,
                    'distal': self.start.distal,
                    }
                procedures.append(data)
        if no_tooth is True and self.start.procedure:
            data = {
                'treatment': Transaction().context['active_id'],
                'procedure': self.start.procedure,
                }
            procedures.append(data)

        Procedure.create(procedures)
        return 'end'
