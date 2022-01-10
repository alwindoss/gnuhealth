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

from trytond.pool import Pool
from . import health_inpatient
from . import wizard
from . import sequences

def register():
    Pool.register(
        health_inpatient.DietTherapeutic,
        health_inpatient.InpatientRegistration,
        health_inpatient.BedTransfer,
        health_inpatient.Appointment,
        health_inpatient.PatientEvaluation,
        health_inpatient.ECG,
        health_inpatient.PatientData,
        health_inpatient.InpatientMedication,
        health_inpatient.InpatientMedicationAdminTimes,
        health_inpatient.InpatientMedicationLog,
        health_inpatient.InpatientDiet,
        wizard.CreateBedTransferInit,
        health_inpatient.InpatientMeal,
        health_inpatient.InpatientMealOrder,
        health_inpatient.InpatientMealOrderItem,
        sequences.GnuHealthSequences,
        sequences.InpatientRegistrationSequence,
        sequences.InpatientMealOrderSequence,
        module='health_inpatient', type_='model')
    
    Pool.register(
        wizard.CreateBedTransfer,
        wizard.CreateInpatientEvaluation,
        module='health_inpatient', type_='wizard')
