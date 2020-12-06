##############################################################################
#
#    GNU Health. Hospital Information System (HIS) component.
#
#                       ***  Dentistry Package  ***
#
#    Copyright (C) 2020 National University of Entre Rios, Argentina (UNER)
#                  School of Engineering <saludpublica@ingenieria.uner.edu.ar>
#    Copyright (C) 2020 Mario Puntin <mario@silix.com.ar>
#    Copyright (C) 2020 GNU Solidario <health@gnusolidario.org>
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
from .wizard import patient_set_odontogram
from .wizard import load_procedure
from .report import procedures_report


def register():
    Pool.register(
        health_dentistry.PatientData,
        health_dentistry.DentistryTreatment,
        health_dentistry.DentistryProcedure,
        health_dentistry.TreatmentProcedure,
        patient_set_odontogram.SetOdontogramStart,
        load_procedure.LoadProcedureStart,
        module='health_dentistry', type_='model')
    Pool.register(
        patient_set_odontogram.SetOdontogram,
        load_procedure.LoadProcedure,
        module='health_dentistry', type_='wizard')
    Pool.register(
        procedures_report.DentistryProcedureReport,
        module='health_dentistry', type_='report')
