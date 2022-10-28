# SPDX-FileCopyrightText: 2008-2022 Luis Falcón <falcon@gnuhealth.org>
# SPDX-FileCopyrightText: 2011-2022 GNU Solidario <health@gnusolidario.org>
#
# SPDX-License-Identifier: GPL-3.0-or-later
#########################################################################
#   Hospital Management Information System (HMIS) component of the      #
#                       GNU Health project                              #
#                   https://www.gnuhealth.org                           #
#########################################################################
#                     HEALTH GENETICS package                           #
#              __init__.py: Package declaration file                    #
#########################################################################

from trytond.pool import Pool
from . import health_genetics


def register():
    Pool.register(
        health_genetics.DiseaseGene,
        health_genetics.ProteinDisease,
        health_genetics.GeneVariant,
        health_genetics.GeneVariantPhenotype,
        health_genetics.PatientGeneticRisk,
        health_genetics.FamilyDiseases,
        health_genetics.GnuHealthPatient,
        module='health_genetics', type_='model')
