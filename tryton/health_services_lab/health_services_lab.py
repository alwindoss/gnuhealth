# SPDX-FileCopyrightText: 2008-2022 Luis Falcón <falcon@gnuhealth.org>
# SPDX-FileCopyrightText: 2011  Adrián Bernardi, Mario Puntin (health_invoice)
# SPDX-FileCopyrightText: 2011-2022 GNU Solidario <health@gnusolidario.org>
#
# SPDX-License-Identifier: GPL-3.0-or-later
#########################################################################
#   Hospital Management Information System (HMIS) component of the      #
#                       GNU Health project                              #
#                   https://www.gnuhealth.org                           #
#########################################################################
#                       HEALTH SERVICES LAB PACKAGE                     #
#                     health_services.py: Main module                   #
#########################################################################
from trytond.model import ModelView, ModelSQL, fields
from trytond.pyson import Eval, Equal
from trytond.pool import Pool
from trytond.i18n import gettext

from .exceptions import (NoServiceAssociated)

__all__ = ['PatientLabTestRequest']


""" Add Lab order charges to service model """


class PatientLabTestRequest(ModelSQL, ModelView):
    'Lab Order'
    __name__ = 'gnuhealth.patient.lab.test'

    service = fields.Many2One(
        'gnuhealth.health_service', 'Service',
        domain=[('patient', '=', Eval('patient_id'))],
        depends=['patient'],
        states={'readonly': Equal(Eval('state'), 'done')},
        help="Service document associated to this Lab Request")

    @classmethod
    def __setup__(cls):
        super(PatientLabTestRequest, cls).__setup__()
        cls._buttons.update({
            'update_service': {
                'readonly': Equal(Eval('state'), 'done'),
            },
            })

    @classmethod
    @ModelView.button
    def update_service(cls, laborders):
        pool = Pool()
        HealthService = pool.get('gnuhealth.health_service')

        hservice = []
        laborder = laborders[0]

        if not laborder.service:
            raise NoServiceAssociated(
                gettext('health_services_lab.msg_no_service_associated')
                )

        service_data = {}
        service_lines = []

        # Add the laborder to the service document

        service_lines.append(('create', [{
            'product': laborder.name.product_id.id,
            'desc': laborder.name.product_id.rec_name,
            'qty': 1
            }]))

        hservice.append(laborder.service)

        description = "Services and Lab"

        service_data['desc'] = description
        service_data['service_line'] = service_lines

        HealthService.write(hservice, service_data)
