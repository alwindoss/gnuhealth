# Copyright (C) 2008-2022 Luis Falcon <lfalcon@gnusolidario.org>
# Copyright (C) 2011-2022 GNU Solidario <health@gnusolidario.org>
# SPDX-FileCopyrightText: 2008-2022 Luis Falcón <falcon@gnuhealth.org>
# SPDX-FileCopyrightText: 2011-2022 GNU Solidario <health@gnusolidario.org>
#
# SPDX-License-Identifier: GPL-3.0-or-later

from . import health_disability
from trytond.pool import Pool


def register():
    Pool.register(
        health_disability.GnuHealthPatient,
        health_disability.Product,
        health_disability.BodyFunctionCategory,
        health_disability.BodyFunction,
        health_disability.BodyStructureCategory,
        health_disability.BodyStructure,
        health_disability.ActivityAndParticipationCategory,
        health_disability.ActivityAndParticipation,
        health_disability.EnvironmentalFactorCategory,
        health_disability.EnvironmentalFactor,
        health_disability.PatientDisabilityAssessment,
        health_disability.PatientBodyFunctionAssessment,
        health_disability.PatientBodyStructureAssessment,
        health_disability.PatientActivityAndParticipationAsssessment,
        health_disability.PatientEnvironmentalFactorAssessment,
        health_disability.PatientAmputation,
        health_disability.PatientProthesis,
        health_disability.PatientData,
        module='health_disability', type_='model')
