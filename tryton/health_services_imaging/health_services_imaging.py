# SPDX-FileCopyrightText: 2008-2022 Luis Falcón <falcon@gnuhealth.org>
# SPDX-FileCopyrightText: 2011-2022 GNU Solidario <health@gnusolidario.org>
#
# SPDX-License-Identifier: GPL-3.0-or-later
#########################################################################
#   Hospital Management Information System (HMIS) component of the      #
#                       GNU Health project                              #
#                   https://www.gnuhealth.org                           #
#########################################################################
#                     HEALTH SERVICES_IMAGING PACKAGE                   #
#                 Health_services_imaging.py: Main module               #
#########################################################################

from trytond.model import ModelView, ModelSQL, fields
from trytond.pyson import Eval, Equal
from trytond.pool import Pool
from .exceptions import (NoServiceAssociated)
from trytond.i18n import gettext

__all__ = ['ImagingTestRequest']


""" Add Imaging order charges to service model """


class ImagingTestRequest(ModelSQL, ModelView):
    'Imaging Order'
    __name__ = 'gnuhealth.imaging.test.request'

    service = fields.Many2One(
        'gnuhealth.health_service', 'Service',
        domain=[('patient', '=', Eval('patient'))], depends=['patient'],
        states={'readonly': Equal(Eval('state'), 'done')},
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
            raise NoServiceAssociated(
                gettext('health_service_imaging.msg_no_service_associated')
                )

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

        service_data['desc'] = description
        service_data['service_line'] = service_lines

        HealthService.write(hservice, service_data)
