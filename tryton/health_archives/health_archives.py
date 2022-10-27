# SPDX-FileCopyrightText: 2008-2022 Luis Falcón <falcon@gnuhealth.org>
# SPDX-FileCopyrightText: 2011-2022 GNU Solidario <health@gnusolidario.org>
#
# SPDX-License-Identifier: GPL-3.0-or-later

#########################################################################
#   Hospital Management Information System (HMIS) component of the      #
#                       GNU Health project                              #
#                   https://www.gnuhealth.org                           #
#########################################################################
#                       HEALTH ARCHIVES package                         #
#                   health_archives.py: main module                     #
#########################################################################
from trytond.model import ModelView, ModelSQL, fields, Unique


__all__ = ['PaperArchive']


class PaperArchive(ModelSQL, ModelView):
    'Location of PAPER Patient Clinical History'

    __name__ = 'gnuhealth.paper_archive'

    patient = fields.Many2One(
        'gnuhealth.patient', 'Patient', required=True,
        help="Patient associated to this newborn baby")

    legacy = fields.Char(
        'Legacy Code', help="If existing, please enter"
        " the old / legacy code associated to this Clinical History")
    location = fields.Many2One(
        'gnuhealth.hospital.unit', 'Unit', required=True,
        help="Location / Unit where this clinical history document"
        " should reside.")

    hc_status = fields.Selection((
        ('archived', 'Archived'),
        ('borrowed', 'Borrowed'),
        ('lost', 'Lost'),
        ), 'Status', required=True, sort=False)

    current_location = fields.Many2One(
        'gnuhealth.hospital.unit', 'Current Location',
        help="Location / Unit where this clinical history document"
        " should reside.")

    identification_code = fields.Function(
        fields.Char('Code'),
        'get_patient_history', searcher='search_patient_code')

    requested_by = fields.Many2One(
        'party.party', 'Requested by',
        domain=[('is_person', '=', True)],
        help="Person who last requested the document")

    request_date = fields.DateTime("Request Date")
    return_date = fields.DateTime("Returned Date")
    comments = fields.Char("Comments")

    @classmethod
    def __setup__(cls):
        '''Create constraints for both the legacy number and patient'''
        super(PaperArchive, cls).__setup__()

        t = cls.__table__()
        cls._sql_constraints = [
            ('legacy_unique', Unique(t, t.legacy),
                'The history already exists'),
            ('patient_unique', Unique(t, t.patient),
                'The patient history already exists'),

            ]

    @classmethod
    def search_patient_code(cls, name, clause):
        '''Retrieve the Patient Identification Code'''
        res = []
        value = clause[2]
        res.append(('patient.puid', clause[1], value))
        return res

    def get_patient_history(self, name):
        return self.patient.puid
