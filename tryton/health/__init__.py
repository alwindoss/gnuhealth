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
from . import health
from . import core
from . import sequences
from . import wizard
from . import report


def register():
    Pool.register(
        health.OperationalArea,
        health.OperationalSector,
        health.DomiciliaryUnit,
        health.FederationCountryConfig,
        health.Occupation,
        health.Ethnicity,
        health.BirthCertificate,
        health.DeathCertificate,
        health.Party,
        health.ContactMechanism,
        health.PersonName,
        health.PartyAddress,
        health.DrugDoseUnits,
        health.MedicationFrequency,
        health.DrugForm,
        health.DrugRoute,
        health.MedicalSpecialty,
        health.HealthInstitution,
        health.HealthInstitutionSpecialties,
        health.HealthInstitutionOperationalSector,
        health.HealthInstitutionO2M,
        health.HospitalBuilding,
        health.HospitalUnit,
        health.HospitalOR,
        health.HospitalWard,
        health.HospitalBed,
        health.HealthProfessional,
        health.HealthProfessionalSpecialties,
        health.PhysicianSP,
        health.Family,
        health.FamilyMember,
        health.MedicamentCategory,
        health.Medicament,
        health.ImmunizationSchedule,
        health.ImmunizationScheduleLine,
        health.ImmunizationScheduleDose,
        health.PathologyCategory,
        health.PathologyGroup,
        health.Pathology,
        health.DiseaseMembers,
        health.BirthCertExtraInfo,
        health.DeathCertExtraInfo,
        health.DeathUnderlyingCondition,
        health.ProcedureCode,
        health.InsurancePlan,
        health.Insurance,
        health.AlternativePersonID,
        health.Product,
        health.PatientData,
        health.PatientDiseaseInfo,
        health.Appointment,
        health.AppointmentReport,
        health.OpenAppointmentReportStart,
        health.PatientPrescriptionOrder,
        health.PrescriptionLine,
        health.PatientMedication,
        health.PatientVaccination,
        health.PatientEvaluation,
        health.Directions,
        health.SecondaryCondition,
        health.DiagnosticHypothesis,
        health.SignsAndSymptoms,
        health.PatientECG,
        health.ProductTemplate,
        health.PageOfLife,
        health.Commands,
        health.Modules,
        health.Help,
        wizard.wizard_check_immunization_status.CheckImmunizationStatusInit,
        sequences.GnuHealthSequences,
        sequences.PatientSequence,
        sequences.PatientEvaluationSequence,
        sequences.AppointmentSequence,
        sequences.PrescriptionSequence,
        module='health', type_='model')

    Pool.register(
        health.OpenAppointmentReport,
        wizard.wizard_appointment_evaluation.CreateAppointmentEvaluation,
        wizard.wizard_check_immunization_status.CheckImmunizationStatus,
        module='health', type_='wizard')
    Pool.register(
        report.health_report.PatientDiseaseReport,
        report.health_report.PatientMedicationReport,
        report.health_report.PatientVaccinationReport,
        report.immunization_status_report.ImmunizationStatusReport,
        module='health', type_='report')
