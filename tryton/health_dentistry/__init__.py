# SPDX-FileCopyrightText: 2020-2021 National University of Entre Rios (UNER)
#                         School of Engineering
#                         <saludpublica@ingenieria.uner.edu.ar>
# SPDX-FileCopyrightText: 2020 Mario Puntin <mario@silix.com.ar>
# SPDX-FileCopyrightText: 2020-2022 Luis Falcón <falcon@gnuhealth.org>
# SPDX-FileCopyrightText: 2020-2022 GNU Solidario <health@gnusolidario.org>

# SPDX-License-Identifier: GPL-3.0-or-later
#########################################################################
#   Hospital Management Information System (HMIS) component of the      #
#                       GNU Health project                              #
#                   https://www.gnuhealth.org                           #
#########################################################################
#                         HEALTH DENTISTRY package                      #
#                __init__.py: Package declaration file                  #
#########################################################################


from trytond.pool import Pool
from . import health_dentistry
from . import wizard
from . import report


def register():
    Pool.register(
        health_dentistry.PatientData,
        health_dentistry.DentistryTreatment,
        health_dentistry.DentistryProcedure,
        health_dentistry.TreatmentProcedure,
        wizard.patient_set_odontogram.SetOdontogramStart,
        wizard.load_procedure.LoadProcedureStart,
        module='health_dentistry', type_='model')
    Pool.register(
        wizard.patient_set_odontogram.SetOdontogram,
        wizard.load_procedure.LoadProcedure,
        module='health_dentistry', type_='wizard')
    Pool.register(
        report.procedures_report.DentistryProcedureReport,
        report.odontogram_report.Odontogram,
        module='health_dentistry', type_='report')
