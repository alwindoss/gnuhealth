# SPDX-FileCopyrightText: 2008-2022 Luis Falcón <falcon@gnuhealth.org>
# SPDX-FileCopyrightText: 2011-2022 GNU Solidario <health@gnusolidario.org>
#
# SPDX-License-Identifier: GPL-3.0-or-later

#########################################################################
#   Hospital Management Information System (HMIS) component of the      #
#                       GNU Health project                              #
#                   https://www.gnuhealth.org                           #
#########################################################################
#                   HEALTH CONTACT TRACING package                      #
#             health_contact_tracing.py: main module                    #
#########################################################################

from trytond.model import ModelView, ModelSQL, fields


__all__ = ['ContactTracing']


class ContactTracing(ModelSQL, ModelView):
    'Person Contacts tracing'
    __name__ = 'gnuhealth.contact_tracing'

    patient = fields.Many2One(
        'gnuhealth.patient', 'Source', required=True,
        help="Person suspected or confirmed")

    pathology = fields.Many2One(
        'gnuhealth.pathology', 'Disease',
        help='Disease to trace')

    contact = fields.Many2One(
        'party.party', 'Contact',
        domain=[('is_person', '=', True)],
        help="Person that the patient has contacted")

    contact_date = fields.DateTime("Date")

    du = fields.Many2One(
        'gnuhealth.du', 'Dom.Unit',
        help="Domiciliary Unit")

    operational_sector = fields.Many2One(
        'gnuhealth.operational_sector', 'Op.Sector',
        help="Operational / Sanitary region")

    exposure_risk = fields.Selection((
        ('low', 'Low'),
        ('high', 'High'),
        ('na', 'Not available'),
        ), 'Exposure', required=True, sort=False)

    exposure_time = fields.Integer(
        "Exposure time",
        help="Exposure time in minutes")

    status = fields.Selection((
        ('unreached', 'Unreached'),
        ('followingup', 'Following up'),
        ('na', 'Not available'),
        ), 'Status', required=True, sort=False,
        help="Unreached: The contact has not been reached yet."
        "\nFollowing up: The contact has been traced, demographics information"
        " has been created and followup evaluations status are stored in the"
        " evaluations")

    context = fields.Char(
        "Context",
        help="Airport, meeting, concert, ...")

    comments = fields.Text("Comments")

    @fields.depends('du')
    def on_change_with_operational_sector(self):
        if (self.du and self.du.operational_sector):
            return (self.du.operational_sector.id)
