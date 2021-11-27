# -*- coding: utf-8 -*-
##############################################################################
#
#    GNU Health: The Free Health and Hospital Information System
#    Copyright (C) 2008-2021 Luis Falcon <lfalcon@gnusolidario.org>
#    Copyright (C) 2011-2021 GNU Solidario <health@gnusolidario.org>
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
from trytond.model import ModelView, ModelSQL, fields, ModelSingleton, Unique
from trytond.pyson import Eval, Equal
from trytond.pool import Pool


__all__ = ['ImagingTestRequest']



""" Add Imaging order charges to service model """

class ImagingTestRequest(ModelSQL, ModelView):
    'Imaging Order'
    __name__ = 'gnuhealth.imaging.test.request'


    service = fields.Many2One(
        'gnuhealth.health_service', 'Service',
        domain=[('patient', '=', Eval('patient'))], depends=['patient'],
        states = {'readonly': Equal(Eval('state'), 'done')},
        help="Service document associated to this Imaging Request")

    @classmethod
    def __setup__(cls):
        super(ImagingTestRequest, cls).__setup__()
        cls._buttons.update({
            'update_service': {
                'readonly': Equal(Eval('state'), 'done'),
            },
            })


    @classmethod
    @ModelView.button
    def update_service(cls, imaging_orders):
        pool = Pool()
        HealthService = pool.get('gnuhealth.health_service')

        hservice = []
        imaging_order = imaging_orders[0]

        if not imaging_order.service:
            cls.raise_user_error("Need to associate a service !")

        service_data = {}
        service_lines = []

        # Add the imaging order to the service document

        service_lines.append(('create', [{
            'product': imaging_order.requested_test.product.id,
            'desc': imaging_order.requested_test.product.rec_name,
            'qty': 1
            }]))

            
        hservice.append(imaging_order.service)
        
        description = "Services and Imaging"
        
        service_data ['desc'] =  description
        service_data ['service_line'] = service_lines
                
        HealthService.write(hservice, service_data)
