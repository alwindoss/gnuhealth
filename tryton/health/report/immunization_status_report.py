# SPDX-FileCopyrightText: 2008-2022 Luis Falcón <falcon@gnuhealth.org>
# SPDX-FileCopyrightText: 2011-2022 GNU Solidario <health@gnusolidario.org>
#
# SPDX-License-Identifier: GPL-3.0-or-later

#########################################################################
#   Hospital Management Information System (HMIS) component of the      #
#                       GNU Health project                              #
#                   https://www.gnuhealth.org                           #
#########################################################################
#                           HEALTH package                              #
#                     immunization_status_report.py                     #
#########################################################################

from trytond.report import Report
from trytond.pool import Pool

__all__ = ['ImmunizationStatusReport']


class ImmunizationStatusReport(Report):
    __name__ = 'gnuhealth.immunization_status_report'

    @classmethod
    def get_context(cls, records, header, data):
        Sched = Pool().get('gnuhealth.immunization_schedule')
        Patient = Pool().get('gnuhealth.patient')
        patient = Patient(data['patient_id'])

        context = super(ImmunizationStatusReport, cls).get_context(
            records, header, data)

        context['patient'] = patient
        sched = Sched(data['immunization_schedule_id'])

        context['immunization_schedule'] = sched

        immunizations_to_check = \
            cls.get_immunizations_for_age(patient, sched)

        immunization_status = \
            cls.verify_status(immunizations_to_check)

        context['immunization_status'] = immunization_status

        return context

    @classmethod
    def get_immunizations_for_age(cls, patient, immunization_schedule):

        immunizations_for_age = []

        for vaccine in immunization_schedule.vaccines:

            for dose in vaccine.doses:
                dose_number, dose_age, age_unit = dose.dose_number, \
                    dose.age_dose, dose.age_unit

                p_age = [patient.age.split(' ')[0][:-1],
                         patient.age.split(' ')[1][:-1],
                         patient.age.split(' ')[2][:-1]]

                # Age of the person in years and months
                pyears, pmonths = int(p_age[0]), int(p_age[1])

                pmonths = (pyears*12)+pmonths

                if ((age_unit == 'months' and pmonths >= dose_age) or
                        (age_unit == 'years' and pyears >= dose_age)):
                    immunization_info = {
                        'patient': patient,
                        'vaccine': vaccine,
                        'dose': dose_number,
                        'dose_age': dose_age,
                        'age_unit': age_unit,
                        'status': None}

                    # Add to the list of this person immunization check
                    immunizations_for_age.append(immunization_info)

        return immunizations_for_age

    @classmethod
    def verify_status(cls, immunizations_to_check):
        Vaccination = Pool().get('gnuhealth.vaccination')

        result = []
        for immunization in immunizations_to_check:
            immunization['status'] = "missing"
            res = Vaccination.search_count([
                ('name', '=', immunization['patient']),
                ('dose', '=', immunization['dose']),
                ('vaccine.name', '=', immunization['vaccine'].vaccine.name),
                ])

            if res:
                immunization['status'] = 'ok'

            result.append(immunization)

        return result
