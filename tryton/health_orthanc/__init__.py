##############################################################################
#
#    GNU Health: The Free Health and Hospital Information System
#    Copyright (C) 2011-2022 GNU Solidario <health@gnusolidario.org>
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
from . import health_orthanc
from . import wizard


def register():
    Pool.register(
        wizard.wizard.AddOrthancInit,
        wizard.wizard.AddOrthancResult,
        health_orthanc.OrthancServerConfig,
        health_orthanc.OrthancStudy,
        health_orthanc.OrthancPatient,
        health_orthanc.TestResult,
        health_orthanc.Patient,
        module="health_orthanc",
        type_="model",
    )
    Pool.register(
        wizard.wizard.FullSyncOrthanc, module="health_orthanc", type_="wizard")
