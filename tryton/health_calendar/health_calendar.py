# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2011  Sebastián Marró <smarro@thymbra.com>
#    $Id$
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

from trytond.model import ModelView, ModelSQL, fields
from trytond.transaction import Transaction

class Appointment(ModelSQL, ModelView):
    'Add Calendar to the Appointment'
    _name = 'gnuhealth.appointment'
    _description = __doc__

    event = fields.Many2One('calendar.event', 'Calendar Event', readonly=True,
        help="Calendar Event")
        
    def create(self, values):
        user_obj = self.pool.get('res.user')
        calendar_obj = self.pool.get('calendar.calendar')        
        event_obj = self.pool.get('calendar.event')
        patient_obj = self.pool.get('gnuhealth.patient')        
        physician_obj = self.pool.get('gnuhealth.physician')
                
        patient = patient_obj.browse(values['patient'])
        if values['doctor']:
            doctor = physician_obj.browse(values['doctor'])
            event_doctor = ' with ' + doctor.name.name
        else:
            event_doctor = ''
        user = user_obj.browse(Transaction().user)
        calendar_ids = calendar_obj.search([('owner', '=', user)], limit=1)
        if calendar_ids:
            calendar = calendar_ids[0]
        else:
            return False
        values['event'] = event_obj.create({
            'dtstart': values['appointment_date'], 
            'calendar': calendar, 
            'summary': 'Appointment ' + patient.name.name + event_doctor 
            })
        return super(Appointment, self).create(values)

    def write(self, ids, values):
        event_obj = self.pool.get('calendar.event')
        physician_obj = self.pool.get('gnuhealth.physician')
                
        for appointment_id in ids:
            appointment = self.browse(appointment_id)
            if 'appointment_date' in values:
                event_obj.write(appointment.event.id, {
                    'dtstart': values['appointment_date'],
                    })
            if 'doctor' in values:
                doctor = physician_obj.browse(values['doctor'])
                event_obj.write(appointment.event.id, {
                    'summary': 'Appointment ' + appointment.patient.name.name + 
                        ' with ' + doctor.name.name,
                    })
        return super(Appointment, self).write(ids, values)
        
Appointment() 
