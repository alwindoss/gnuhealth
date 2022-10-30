#!/usr/bin/env python

# SPDX-FileCopyrightText: 2008-2022 Luis Falcón <falcon@gnuhealth.org>
# SPDX-FileCopyrightText: 2011-2022 GNU Solidario <health@gnusolidario.org>

# SPDX-License-Identifier: GPL-3.0-or-later

#########################################################################
#   Hospital Management Information System (HMIS) component of the      #
#                       GNU Health project                              #
#                   https://www.gnuhealth.org                           #
#########################################################################
#                    HEALTH NTD DENGUE package                          #
#                health_ntd_dengue.py: main module                      #
#########################################################################

from datetime import datetime
from trytond.model import ModelView, ModelSQL, fields
from trytond.pyson import Eval, Not, Bool
from trytond.pool import Pool


__all__ = ['DengueDUSurvey']


class DengueDUSurvey(ModelSQL, ModelView):
    'Dengue DU Survey'
    __name__ = 'gnuhealth.dengue_du_survey'

    name = fields.Char('Survey Code', readonly=True)
    du = fields.Many2One('gnuhealth.du', 'DU', help="Domiciliary Unit")
    survey_date = fields.Date('Date', required=True)

    du_status = fields.Selection([
        (None, ''),
        ('initial', 'Initial'),
        ('unchanged', 'Unchanged'),
        ('better', 'Improved'),
        ('worse', 'Worsen'),
        ], 'Status',
        help="DU status compared to last visit", required=True, sort=False)

    # Surveillance traps (ovitraps)
    ovitraps = fields.Boolean(
        'Ovitraps',
        help="Check if ovitraps are in place")

    # Current issues
    aedes_larva = fields.Boolean(
        'Larvae', "Check this box if Aedes aegypti larvae were found")
    larva_in_house = fields.Boolean(
        'Domiciliary',
        help="Check this box if larvae were found inside the house")
    larva_peri = fields.Boolean(
        'Peri-Domiciliary',
        help="Check this box if larva were found in the peridomiciliary area")

    old_tyres = fields.Boolean('Tyres', help="Old vehicle tyres found")

    animal_water_container = fields.Boolean(
        'Animal Water containers',
        help="Animal water containers not scrubbed or clean")

    flower_vase = fields.Boolean(
        'Flower vase',
        help="Flower vases without scrubbing or cleaning")

    potted_plant = fields.Boolean(
        'Potted Plants',
        help="Potted Plants with saucers")

    tree_holes = fields.Boolean(
        'Tree holes',
        help="unfilled tree holes")

    rock_holes = fields.Boolean(
        'Rock holes',
        help="unfilled rock holes")

    # Chemical controls for adult mosquitoes

    du_fumigation = fields.Boolean(
        'Fumigation', help="The DU has been fumigated")
    fumigation_date = fields.Date(
        'Fumigation Date', help="Last Fumigation Date",
        states={'invisible': Not(Bool(Eval('du_fumigation')))})

    observations = fields.Text('Observations')
    next_survey_date = fields.Date('Next survey')

    @staticmethod
    def default_survey_date():
        return datetime.now()

    @classmethod
    def generate_code(cls, **pattern):
        Config = Pool().get('gnuhealth.sequences')
        config = Config(1)
        sequence = config.get_multivalue(
            'dengue_du_survey_sequence', **pattern)
        if sequence:
            return sequence.get()

    @classmethod
    def create(cls, vlist):
        vlist = [x.copy() for x in vlist]
        for values in vlist:
            if not values.get('name'):
                values['name'] = cls.generate_code()
        return super(DengueDUSurvey, cls).create(vlist)
