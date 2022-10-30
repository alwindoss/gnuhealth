#!/usr/bin/env python

# SPDX-FileCopyrightText: 2008-2022 Luis Falcón <falcon@gnuhealth.org>
# SPDX-FileCopyrightText: 2011-2022 GNU Solidario <health@gnusolidario.org>

# SPDX-License-Identifier: GPL-3.0-or-later

#########################################################################
#   Hospital Management Information System (HMIS) component of the      #
#                       GNU Health project                              #
#                   https://www.gnuhealth.org                           #
#########################################################################
#                     HEALTH NTD package                                #
#                health_ntd.py: main module                             #
#########################################################################

from datetime import datetime
from trytond.model import ModelView, ModelSQL, fields
from trytond.pyson import Eval, Not, Bool
from trytond.pool import Pool


__all__ = ['ChagasDUSurvey']


class ChagasDUSurvey(ModelSQL, ModelView):
    'Chagas DU Entomological Survey'
    __name__ = 'gnuhealth.chagas_du_survey'

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

    # Findings of Triatomines in the DU
    triatomines = fields.Boolean(
        'Triatomines', help="Check this box if triatomines were found")
    vector = fields.Selection([
        (None, ''),
        ('t_infestans', 'T. infestans'),
        ('t_brasilensis', 'T. brasilensis'),
        ('r_prolixus', 'R. prolixus'),
        ('t_dimidiata', 'T. dimidiata'),
        ('p_megistus', 'P. megistus'),
        ], 'Vector', help="Vector", sort=False)

    nymphs = fields.Boolean(
        'Nymphs', "Check this box if triatomine nymphs were found")
    t_in_house = fields.Boolean(
        'Domiciliary',
        help="Check this box if triatomines were found inside the house")
    t_peri = fields.Boolean(
        'Peri-Domiciliary',
        help="Check this box if triatomines were found "
             "in the peridomiciliary area")

    # Infrastructure conditions
    dfloor = fields.Boolean(
        'Floor',
        help="Current floor can host triatomines")
    dwall = fields.Boolean(
        'Walls',
        help="Wall materials or state can host triatomines")
    droof = fields.Boolean(
        'Roof',
        help="Roof materials or state can host triatomines")
    dperi = fields.Boolean(
        'Peri-domicilary',
        help="Peri domiciliary area can host triatomines")

    # Preventive measures

    bugtraps = fields.Boolean(
        'Bug traps',
        help="The DU has traps to detect triatomines")

    # Chemical controls

    du_fumigation = fields.Boolean(
        'Fumigation',
        help="The DU has been fumigated")
    fumigation_date = fields.Date(
        'Fumigation Date',
        help="Last Fumigation Date",
        states={'invisible': Not(Bool(Eval('du_fumigation')))})

    du_paint = fields.Boolean(
        'Insecticide Paint',
        help="The DU has been treated with insecticide-containing paint")
    paint_date = fields.Date(
        'Paint Date',
        help="Last Paint Date",
        states={'invisible': Not(Bool(Eval('du_paint')))})

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
            'chagas_du_survey_sequence', **pattern)
        if sequence:
            return sequence.get()

    @classmethod
    def create(cls, vlist):
        vlist = [x.copy() for x in vlist]
        for values in vlist:
            if not values.get('name'):
                values['name'] = cls.generate_code()
        return super(ChagasDUSurvey, cls).create(vlist)
