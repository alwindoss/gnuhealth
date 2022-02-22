##############################################################################
#
#    GNU Health: The Free Health and Hospital Information System
#    Copyright (C) 2008-2022 Luis Falcon <lfalcon@gnusolidario.org>
#    Copyright (C) 2011-2022 GNU Solidario <health@gnusolidario.org>
#
#    Copyright (C) 2013  Sebastian Marro <smarro@gnusolidario.org>
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
from . import health_stock
from . import wizard


def register():
    Pool.register(
        health_stock.Party,
        health_stock.Lot,
        health_stock.Move,
        health_stock.PatientAmbulatoryCare,
        health_stock.PatientAmbulatoryCareMedicament,
        health_stock.PatientAmbulatoryCareMedicalSupply,
        health_stock.PatientRounding,
        health_stock.PatientRoundingMedicament,
        health_stock.PatientRoundingMedicalSupply,
        health_stock.PatientPrescriptionOrder,
        health_stock.PatientVaccination,
        wizard.wizard_create_prescription_stock_move.
        CreatePrescriptionStockMoveInit,
        wizard.wizard_create_vaccination_stock_move.
        CreateVaccinationStockMoveInit,
        module='health_stock', type_='model')
    Pool.register(
        wizard.wizard_create_prescription_stock_move.
        CreatePrescriptionStockMove,
        wizard.wizard_create_vaccination_stock_move.
        CreateVaccinationStockMove,
        module='health_stock', type_='wizard')
