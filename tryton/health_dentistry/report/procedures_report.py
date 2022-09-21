# This file is part health_dentistry module for GNU Health HMIS component
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
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
