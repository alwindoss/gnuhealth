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
#   health_report.py: Disease, Medication and Vaccination reports       #
#########################################################################
import pytz
from datetime import datetime
from trytond.pool import Pool
from trytond.transaction import Transaction
from trytond.report import Report

__all__ = ['PatientDiseaseReport', 'PatientMedicationReport', 
    'PatientVaccinationReport']

def get_print_date():
    Company = Pool().get('company.company')

    timezone = None
    company_id = Transaction().context.get('company')
    if company_id:
        company = Company(company_id)
        if company.timezone:
            timezone = pytz.timezone(company.timezone)

    dt = datetime.now()
    return datetime.astimezone(dt.replace(tzinfo=pytz.utc), timezone)


class PatientDiseaseReport(Report):
    __name__ = 'patient.disease'

    @classmethod
    def parse(cls, report, objects, data, localcontext):
        localcontext['print_date'] = get_print_date()
        localcontext['print_time'] = localcontext['print_date'].time()

        return super(PatientDiseaseReport, cls).parse(report, objects, data, 
            localcontext)


class PatientMedicationReport(Report):
    __name__ = 'patient.medication'

    @classmethod
    def parse(cls, report, objects, data, localcontext):
        localcontext['print_date'] = get_print_date()
        localcontext['print_time'] = localcontext['print_date'].time()

        return super(PatientMedicationReport, cls).parse(report, objects, data, 
            localcontext)


class PatientVaccinationReport(Report):
    __name__ = 'patient.vaccination'

    @classmethod
    def parse(cls, report, objects, data, localcontext):
        localcontext['print_date'] = get_print_date()
        localcontext['print_time'] = localcontext['print_date'].time()

        return super(PatientVaccinationReport, cls).parse(report, objects, data, 
            localcontext)
