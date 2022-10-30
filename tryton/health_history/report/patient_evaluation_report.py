# Copyright (C) 2008-2022 Luis Falcon <falcon@gnuhealth.org>
# Copyright (C) 2011-2022 GNU Solidario <health@gnusolidario.org>
# SPDX-FileCopyrightText: 2008-2022 Luis Falcón <falcon@gnuhealth.org>
# SPDX-FileCopyrightText: 2011-2022 GNU Solidario <health@gnusolidario.org>
#
# SPDX-License-Identifier: GPL-3.0-or-later

import pytz
from datetime import datetime
from trytond.pool import Pool
from trytond.transaction import Transaction
from trytond.report import Report

__all__ = ['PatientEvaluationReport']


class PatientEvaluationReport(Report):
    __name__ = 'patient.evaluation'

    @classmethod
    def parse(cls, report, objects, data, localcontext):
        Company = Pool().get('company.company')

        timezone = None
        company_id = Transaction().context.get('company')
        if company_id:
            company = Company(company_id)
            if company.timezone:
                timezone = pytz.timezone(company.timezone)

        dt = datetime.now()
        localcontext['print_date'] = datetime.astimezone(dt.replace(
            tzinfo=pytz.utc), timezone)
        localcontext['print_time'] = localcontext['print_date'].time()

        return super(PatientEvaluationReport, cls).parse(report,
                                                         objects, data,
                                                         localcontext)
