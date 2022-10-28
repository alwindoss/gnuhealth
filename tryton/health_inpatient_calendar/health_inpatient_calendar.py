# SPDX-FileCopyrightText: 2008-2022 Luis Falcón <falcon@gnuhealth.org>
# SPDX-FileCopyrightText: 2011-2022 GNU Solidario <health@gnusolidario.org>
# SPDX-FileCopyrightText: 2011-2012 Sebastian Marro <smarro@thymbra.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later
#########################################################################
#   Hospital Management Information System (HMIS) component of the      #
#                       GNU Health project                              #
#                   https://www.gnuhealth.org                           #
#########################################################################
#                  HEALTH INPATIENT CALENDAR PACKAGE                    #
#             health_inpatient_calendar.py: main module                 #
#########################################################################

from trytond.model import ModelView, ModelSQL, fields
from trytond.pool import Pool


__all__ = ['HospitalBed', 'InpatientRegistration']


class HospitalBed(ModelSQL, ModelView):
    "Add Calendar to Hospital Bed"
    __name__ = "gnuhealth.hospital.bed"

    calendar = fields.Many2One('calendar.calendar', 'Calendar')


class InpatientRegistration(ModelSQL, ModelView):
    'Add Calendar to the Inpatient Registration'
    __name__ = 'gnuhealth.inpatient.registration'

    event = fields.Many2One(
        'calendar.event', 'Calendar Event', readonly=True,
        help="Calendar Event")

    @classmethod
    def confirmed(cls, registrations):
        super(InpatientRegistration, cls).confirmed(registrations)

        Event = Pool().get('calendar.event')

        for inpatient_registration in registrations:
            if inpatient_registration.bed.calendar:
                if not inpatient_registration.event:
                    bed = inpatient_registration.bed.name.code + ": "
                    events = Event.create([{
                        'dtstart': inpatient_registration.hospitalization_date,
                        'dtend': inpatient_registration.discharge_date,
                        'calendar': inpatient_registration.bed.calendar.id,
                        'summary':
                            bed + inpatient_registration.patient.name.rec_name
                        }])
                    cls.write(
                        [inpatient_registration],
                        {'event': events[0].id})

    @classmethod
    def discharge(cls, registrations):
        super(InpatientRegistration, cls).discharge(registrations)

        Event = Pool().get('calendar.event')

        for inpatient_registration in registrations:
            if inpatient_registration.event:
                Event.delete([inpatient_registration.event])

    @classmethod
    def write(cls, registrations, values):
        Event = Pool().get('calendar.event')
        Patient = Pool().get('gnuhealth.patient')
        HospitalBed = Pool().get('gnuhealth.hospital.bed')

        for inpatient_registration in registrations:
            if inpatient_registration.event:
                if 'hospitalization_date' in values:
                    Event.write([inpatient_registration.event], {
                        'dtstart': values['hospitalization_date'],
                        })
                if 'discharge_date' in values:
                    Event.write([inpatient_registration.event], {
                        'dtend': values['discharge_date'],
                        })
                if 'bed' in values:
                    bed = HospitalBed(values['bed'])
                    Event.write([inpatient_registration.event], {
                        'calendar': bed.calendar.id,
                        })
                if 'patient' in values:
                    patient = Patient(values['patient'])
                    bed = inpatient_registration.bed.name.code + ": "
                    Event.write([inpatient_registration.event], {
                        'summary': bed + patient.name.rec_name,
                        })

        return super(InpatientRegistration, cls).write(registrations, values)

    @classmethod
    def delete(cls, registrations):
        Event = Pool().get('calendar.event')

        for inpatient_registration in registrations:
            if inpatient_registration.event:
                Event.delete([inpatient_registration.event])
        return super(InpatientRegistration, cls).delete(registrations)
