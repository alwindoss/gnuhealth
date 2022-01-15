# -*- coding: utf-8 -*-
##############################################################################
#
#    GNU Health: The Free Health and Hospital Information System
#    Copyright (C) 2008-2022 Luis Falcon <lfalcon@gnusolidario.org>
#    Copyright (C) 2011-2022 GNU Solidario <health@gnusolidario.org>
#
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
