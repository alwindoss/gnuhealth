# SPDX-FileCopyrightText: 2008-2022 Luis Falcón <falcon@gnuhealth.org>
# SPDX-FileCopyrightText: 2013 Sebastian Marro <smarro@thymbra.com>
# SPDX-FileCopyrightText: 2011-2022 GNU Solidario <health@gnusolidario.org>
#
# SPDX-License-Identifier: GPL-3.0-or-later
#########################################################################
#   Hospital Management Information System (HMIS) component of the      #
#                       GNU Health project                              #
#                   https://www.gnuhealth.org                           #
#########################################################################
#                         HEALTH REPORTING package                      #
#                 __init__.py: Package declaration file                 #
#########################################################################

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
