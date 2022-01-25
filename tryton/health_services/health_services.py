##############################################################################
#
#    GNU Health: The Free Health and Hospital Information System
#    Copyright (C) 2008-2022 Luis Falcon <lfalcon@gnusolidario.org>
#    Copyright (C) 2011-2022 GNU Solidario <health@gnusolidario.org>
#
#    Copyright (C) 2011  Adrián Bernardi, Mario Puntin (health_invoice)
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
from trytond.model import ModelView, ModelSQL, fields, Unique
from trytond.transaction import Transaction
from trytond.pyson import Eval, Equal
from trytond.pool import Pool
from trytond.i18n import gettext
from trytond.modules.health.core import get_institution

from .exceptions import (
    ServiceAlreadyInvoiced, NoServiceAssociated, NoProductAssociated,
    )


__all__ = ['HealthService', 'HealthServiceLine', 'PatientPrescriptionOrder']


class HealthService(ModelSQL, ModelView):
    'Health Service'
    __name__ = 'gnuhealth.health_service'

    STATES = {'readonly': Eval('state') == 'invoiced'}

    name = fields.Char('ID', readonly=True)
    desc = fields.Char('Description')
    patient = fields.Many2One(
        'gnuhealth.patient',
        'Patient', required=True,
        states=STATES)
    institution = fields.Many2One('gnuhealth.institution', 'Institution')
    company = fields.Many2One('company.company', 'Company')

    service_date = fields.Date('Date')
    service_line = fields.One2Many(
        'gnuhealth.health_service.line',
        'name', 'Service Line', help="Service Line")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('invoiced', 'Invoiced'),
        ], 'State', readonly=True)
    invoice_to = fields.Many2One('party.party', 'Invoice to')

    @classmethod
    def __setup__(cls):
        super(HealthService, cls).__setup__()

        t = cls.__table__()
        cls._sql_constraints = [
            ('name_unique', Unique(t, t.name),
                'The Service ID must be unique'),
            ]
        cls._buttons.update({
            'button_set_to_draft': {
                'invisible': Equal(Eval('state'), 'draft')}
            })

        cls._order.insert(0, ('state', 'ASC'))
        cls._order.insert(1, ('name', 'DESC'))

    @staticmethod
    def default_state():
        return 'draft'

    @staticmethod
    def default_company():
        return Transaction().context.get('company')

    @staticmethod
    def default_service_date():
        return datetime.date.today()

    @staticmethod
    def default_institution():
        return get_institution()

    @classmethod
    @ModelView.button
    def button_set_to_draft(cls, services):
        cls.write(services, {'state': 'draft'})

    @classmethod
    def generate_code(cls, **pattern):
        Config = Pool().get('gnuhealth.sequences')
        config = Config(1)
        sequence = config.get_multivalue(
            'health_service_sequence', **pattern)
        if sequence:
            return sequence.get()

    @classmethod
    def create(cls, vlist):
        vlist = [x.copy() for x in vlist]
        for values in vlist:
            if not values.get('name'):
                values['name'] = cls.generate_code()
        return super(HealthService, cls).create(vlist)


class HealthServiceLine(ModelSQL, ModelView):
    'Health Service'
    __name__ = 'gnuhealth.health_service.line'

    name = fields.Many2One(
        'gnuhealth.health_service', 'Service',
        readonly=True)
    desc = fields.Char('Description', required=True)
    appointment = fields.Many2One(
        'gnuhealth.appointment', 'Appointment',
        help='Enter or select the date / ID of the appointment related to'
        ' this evaluation')
    to_invoice = fields.Boolean('Invoice')
    product = fields.Many2One('product.product', 'Product', required=True)
    qty = fields.Integer('Qty')
    from_date = fields.Date('From')
    to_date = fields.Date('To')
    action_required = fields.Boolean(
        'Action required', help='This optional field'
        ' is used in the context of validation'
        ' on the service line. Mark it if there'
        ' is any administrative or other type'
        ' that needs action')

    remarks = fields.Char('Remarks')

    @staticmethod
    def default_qty():
        return 1

    @staticmethod
    def default_to_invoice():
        return True

    @fields.depends('product', 'desc')
    def on_change_product(self, name=None):
        if self.product:
            self.desc = self.product.name

    @classmethod
    def validate(cls, services):
        super(HealthServiceLine, cls).validate(services)
        for service in services:
            service.validate_invoice_status()

    def validate_invoice_status(self):
        if (self.name):
            if (self.name.state == 'invoiced'):
                raise ServiceAlreadyInvoiced(
                    gettext('health_service.msg_service_already_invoiced'))

    def get_rec_name(self, name):
        if self.name:
            return f'{self.desc} ({self.name.name})'

# Add Prescription order charges to service model
class PatientPrescriptionOrder(ModelSQL, ModelView):
    'Prescription Order'
    __name__ = 'gnuhealth.prescription.order'

    service = fields.Many2One(
        'gnuhealth.health_service', 'Service',
        domain=[('patient', '=', Eval('patient'))], depends=['patient'],
        states={'readonly': Equal(Eval('state'), 'done')},
        help="Service document associated to this prescription")

    @classmethod
    def __setup__(cls):
        super(PatientPrescriptionOrder, cls).__setup__()
        cls._buttons.update({
            'update_service': {
                'readonly': Equal(Eval('state'), 'done'),
            },
            })

    @classmethod
    @ModelView.button
    def update_service(cls, prescriptions):
        pool = Pool()
        HealthService = pool.get('gnuhealth.health_service')

        hservice = []
        prescription = prescriptions[0]

        if not prescription.service:
            raise NoServiceAssociated(
                    gettext('health_service.msg_no_service_associated'))

        service_data = {}
        service_lines = []

        # Add the prescription lines to the service document

        for line in prescription.prescription_line:
            service_lines.append(('create', [{
                'product': line.medicament.name.id,
                'desc': 'Prescription Line',
                'qty': line.quantity
                }]))

        hservice.append(prescription.service)

        description = "Services including " + \
            prescription.prescription_id

        service_data['desc'] = description
        service_data['service_line'] = service_lines

        HealthService.write(hservice, service_data)


# Include  Patient Evaluation service
class PatientEvaluation(ModelSQL, ModelView):
    'Patient Evaluation'
    __name__ = 'gnuhealth.patient.evaluation'

    service = fields.Many2One(
        'gnuhealth.health_service', 'Service',
        domain=[('patient', '=', Eval('patient'))], depends=['patient'],
        states={'readonly': Equal(Eval('state'), 'done')},
        help="Service document associated to this evaluation")

    product = fields.Many2One('product.product', 'Product')

    @classmethod
    def __setup__(cls):
        super(PatientEvaluation, cls).__setup__()
        cls._buttons.update({
            'update_service': {
                'readonly': Equal(Eval('state'), 'done'),
            },
            })

    @classmethod
    @ModelView.button
    def update_service(cls, evaluations):
        pool = Pool()
        HealthService = pool.get('gnuhealth.health_service')

        hservice = []
        evaluation = evaluations[0]

        if not evaluation.service:
            raise NoServiceAssociated(
                    gettext('health_service.msg_no_service_associated'))

        if not evaluation.product:
            raise NoProductAssociated(
                    gettext('health_service.msg_no_product_associated'))

        service_data = {}
        service_lines = []

        # Add the evaluation to the service document line

        service_lines.append(('create', [{
            'product': evaluation.product.id,
            'desc': 'Medical evaluation services',
            'qty': 1
            }]))

        hservice.append(evaluation.service)

        description = "Medical evaluation services"
        service_data['desc'] = description
        service_data['service_line'] = service_lines

        HealthService.write(hservice, service_data)
