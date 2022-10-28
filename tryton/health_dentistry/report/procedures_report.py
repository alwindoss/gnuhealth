# SPDX-FileCopyrightText: 2020-2021 National University of Entre Rios (UNER)
#                         School of Engineering
#                         <saludpublica@ingenieria.uner.edu.ar>
# SPDX-FileCopyrightText: 2020 Mario Puntin <mario@silix.com.ar>
# SPDX-FileCopyrightText: 2020-2022 Luis Falcón <falcon@gnuhealth.org>
# SPDX-FileCopyrightText: 2020-2022 GNU Solidario <health@gnusolidario.org>

# SPDX-License-Identifier: GPL-3.0-or-later
#########################################################################
#   Hospital Management Information System (HMIS) component of the      #
#                       GNU Health project                              #
#                   https://www.gnuhealth.org                           #
#########################################################################
#                         HEALTH DENTISTRY package                      #
#                procedures_report: Procedures report module            #
#########################################################################

import io
import os
from PIL import Image, ImageDraw

from collections import defaultdict

from trytond.pool import Pool
from trytond.report import Report

__all__ = ['DentistryProcedureReport']


class DentistryProcedureReport(Report):
    __name__ = 'health_dentistry.procedure.report'

    @classmethod
    def digest_treatments(cls, patient, lang=None):
        pool = Pool()
        Procedure = pool.get('gnuhealth.dentistry.procedure')

        result = []
        treatments = patient.dentistry_treatments
        for t in treatments:
            add_notes = True
            notes = t.notes.strip()
            data = defaultdict(list)
            for p in t.procedures:
                data[p.procedure.id].append(p.tooth if p.tooth else '')
            for k, v in data.items():
                procedure = Procedure.browse([k])[0]
                procedure_info = procedure.name + ' (' + ', '.join(v) + ')'
                if notes:
                    notes = notes if add_notes else '"'
                    add_notes = False
                result.append({
                    'treatment_date': t.treatment_date,
                    'state': t.state_string,
                    'procedure': procedure_info,
                    'notes': notes,
                    })
        return result

    @classmethod
    def get_context(cls, records, header, data):
        pool = Pool()
        Date = pool.get('ir.date')
        context = super(DentistryProcedureReport, cls).get_context(
            records, header, data)
        context['today'] = Date.today()
        context['digest_treatments'] = cls.digest_treatments

        return context
