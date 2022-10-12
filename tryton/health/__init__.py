# SPDX-FileCopyrightText: 2008-2022 Luis Falcón <falcon@gnuhealth.org>
# SPDX-FileCopyrightText: 2011-2022 GNU Solidario <health@gnusolidario.org>
#
# SPDX-License-Identifier: GPL-3.0-or-later
#########################################################################
#   Hospital Management Information System (HMIS) component of the      #
#                       GNU Health project                              #
#                   https://www.gnuhealth.org                           #
#########################################################################
#                           HEALTH package                              #
#                __init__.py: Package declaration file                  #
#########################################################################

from trytond.pool import Pool
from . import health
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
