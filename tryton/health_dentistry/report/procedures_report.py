##############################################################################
#
#    GNU Health: The Free Health and Hospital Information System
#    Copyright (C) 2020 GNU Solidario <health@gnusolidario.org>
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
    def get_context(cls, records, data):
        pool = Pool()
        Date = pool.get('ir.date')
        context = super(DentistryProcedureReport, cls).get_context(
            records, data)
        context['today'] = Date.today()
        context['digest_treatments'] = cls.digest_treatments
        return context
