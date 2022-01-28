##############################################################################
#
#    GNU Health: The Free Health and Hospital Information System
#    Copyright (C) 2008-2022 Luis Falcon <lfalcon@gnusolidario.org>
#    Copyright (C) 2011-2022 GNU Solidario <health@gnusolidario.org>
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
from trytond.model import fields
from trytond.pool import PoolMeta

__all__ = ['Invoice', 'InvoiceLine']


class Invoice(metaclass=PoolMeta):
    __name__ = 'account.invoice'

    patient = fields.Function(
        fields.Many2One(
            'gnuhealth.patient', 'Patient',
            help="Patient in the invoice"),
        'get_patient')

    health_service = fields.Function(
        fields.Many2One(
            'gnuhealth.health_service', 'Health Service',
            help="The service entry"),
        'get_health_service', searcher='search_health_service')

    def get_patient(self, name):
        try:
            return self.lines[0].origin.name.patient.id
        except:
            return None

    def get_health_service(self, name):
        try:
            return self.lines[0].origin.name.id
        except:
            return None

    @classmethod
    def search_health_service(cls, name, clause):
        return [
            ('lines.origin.name.id',
             clause[1],
             clause[2],
             'gnuhealth.health_service.line')]


class InvoiceLine(metaclass=PoolMeta):
    __name__ = 'account.invoice.line'

    @classmethod
    def _get_origin(cls):
        return super(InvoiceLine, cls)._get_origin() + [
            'gnuhealth.health_service.line'
            ]
