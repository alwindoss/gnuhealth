# SPDX-FileCopyrightText: 2008-2022 Luis Falcón <falcon@gnuhealth.org>
# SPDX-FileCopyrightText: 2011-2022 GNU Solidario <health@gnusolidario.org>
# SPDX-FileCopyrightText: 2011-2014 Sebastian Marro <smarro@thymbra.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later
#########################################################################
#   Hospital Management Information System (HMIS) component of the      #
#                       GNU Health project                              #
#                   https://www.gnuhealth.org                           #
#########################################################################
#                       HEALTH CALENDAR PACKAGE                         # 
#                health_calendar.py: Main calendar module               #
#########################################################################
from trytond.model import fields
from trytond.pyson import Eval, Not, Bool
from trytond.pool import Pool, PoolMeta
from trytond.i18n import gettext

from .exceptions import (AppointmentEndDateBeforeStart)

__all__ = ['User', 'Appointment']


class User(metaclass=PoolMeta):
    __name__ = "res.user"

    use_caldav = fields.Boolean('CalDAV', help="The user has a CalDav account")
    calendar = fields.Many2One(
        'calendar.calendar', 'Calendar',
        states={
            'invisible': Not(Bool(Eval('use_caldav'))),
            'required': Bool(Eval('use_caldav')),
            })


class Appointment(metaclass=PoolMeta):
    __name__ = 'gnuhealth.appointment'

    event = fields.Many2One(
        'calendar.event', 'CalDAV Event', readonly=True,
        help="Calendar Event",
        states={'invisible': Not(Bool(Eval('event')))})
    appointment_date_end = fields.DateTime('End Date and Time')

    @classmethod
    def validate(cls, appointments):
        super(Appointment, cls).validate(appointments)
        for appointment in appointments:
            appointment.validate_appointment_dates()

    def validate_appointment_dates(self):
        if self.appointment_date_end:
            if (self.appointment_date_end < self.appointment_date):
                raise AppointmentEndDateBeforeStart(gettext(
                    'health_calendar.msg_appointment_end_date_before_start',
                    appointment_date=self.appointment_date,
                    appointment_date_end=self.appointment_date_end
                    )
                )

    @classmethod
    def create(cls, vlist):
        pool = Pool()
        Event = pool.get('calendar.event')
        Patient = pool.get('gnuhealth.patient')
        Healthprof = pool.get('gnuhealth.healthprofessional')

        vlist = [x.copy() for x in vlist]

        for values in vlist:
            # Check if the event exists (eg, created from a caldav client)
            # If so, then do not create it again.
            if 'event' in values:
                break

            if values['state'] == 'confirmed':
                if values['healthprof']:
                    healthprof = Healthprof(values['healthprof'])
                    if (healthprof.name.internal_user and
                            healthprof.name.internal_user.calendar):
                        patient = Patient(values['patient'])
                        appointment_date_end = None
                        if values.get('appointment_date_end'):
                            appointment_date_end = \
                                values['appointment_date_end']
                        events = Event.create([{
                            'dtstart': values['appointment_date'],
                            'dtend': appointment_date_end,
                            'calendar':
                                healthprof.name.internal_user.calendar.id,
                            'summary': patient.name.rec_name,
                            'description': values['comments'],
                            }])
                        values['event'] = events[0].id
        return super(Appointment, cls).create(vlist)

    @classmethod
    def write(cls, appointments, values):
        pool = Pool()
        Event = pool.get('calendar.event')
        Patient = pool.get('gnuhealth.patient')
        Healthprof = pool.get('gnuhealth.healthprofessional')

        for appointment in appointments:
            # Update caldav event
            if appointment.event and ('healthprof' not in values):
                if 'appointment_date' in values:
                    Event.write([appointment.event], {
                        'dtstart': values['appointment_date'],
                        })
                if 'appointment_date_end' in values:
                    Event.write([appointment.event], {
                        'dtend': values['appointment_date_end'],
                        })
                if 'patient' in values:
                    patient = Patient(values['patient'])
                    Event.write([appointment.event], {
                        'summary': patient.name.rec_name,
                        })
                if 'comments' in values:
                    Event.write([appointment.event], {
                        'description': values['comments'],
                        })

            else:
                # Move the event to the new health professional
                if appointment.event and ('healthprof' in values):
                    current_event = [appointment.event]
                    if appointment.healthprof.name.internal_user:
                        healthprof = Healthprof(values['healthprof'])
                        if healthprof.name.internal_user.calendar:
                            # Health professional has calendar
                            patient = appointment.patient.name.rec_name
                            comments = ''
                            if 'comments' in values:
                                comments = values['comments']
                            else:
                                comments = appointment.comments
                            if 'appointment_date' in values:
                                appointment_date = values['appointment_date']
                            else:
                                appointment_date = appointment.appointment_date
                            if 'appointment_date_end' in values:
                                appointment_date_end = \
                                    values['appointment_date_end']
                            else:
                                appointment_date_end = \
                                    appointment.appointment_date_end
                            events = Event.create([{
                                'dtstart': appointment_date,
                                'dtend': appointment_date_end,
                                'calendar':
                                    healthprof.name.internal_user.calendar.id,
                                'summary':
                                    patient,
                                'description': comments,
                                }])
                            values['event'] = events[0].id

                    # Delete the event from the current health professional
                    # after it has been transfer to the new healthpfof
                    Event.delete(current_event)
        return super(Appointment, cls).write(appointments, values)

    @classmethod
    def delete(cls, appointments):
        Event = Pool().get('calendar.event')

        for appointment in appointments:
            if appointment.event:
                Event.delete([appointment.event])
        return super(Appointment, cls).delete(appointments)
