##############################################################################
#
#    GNU Health. Hospital Information System (HIS) component.
#
#                       ***  Dentistry Package  ***
#
#    Copyright (C) 2020-2021 National University of Entre Rios (UNER)
#                  School of Engineering <saludpublica@ingenieria.uner.edu.ar>
#    Copyright (C) 2020 Mario Puntin <mario@silix.com.ar>
#    Copyright (C) 2020-2022 GNU Solidario <health@gnusolidario.org>
#    Copyright (C) 2020-2022 Luis Falcon <falcon@gnuhealth.org>
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
