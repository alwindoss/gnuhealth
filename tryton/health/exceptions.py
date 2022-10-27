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
#                  exceptions.py: Exceptions classes                    #
#########################################################################

from trytond.exceptions import UserError
from trytond.model.exceptions import ValidationError


class WrongDateofBirth(ValidationError):
    pass


class DateHealedBeforeDx(ValidationError):
    pass


class EndTreatmentDateBeforeStart(ValidationError):
    pass


class MedEndDateBeforeStart(ValidationError):
    pass


class NextDoseBeforeFirst(ValidationError):
    pass


class DrugPregnancySafetyCheck(ValidationError):
    pass


class NoAssociatedHealthProfessional(ValidationError):
    pass


class EvaluationEndBeforeStart(ValidationError):
    pass


class MustBeAPerson(ValidationError):
    pass


class DupOfficialName(ValidationError):
    pass


class FedAccountMismatch(ValidationError):
    pass


class BirthCertDateMismatch(ValidationError):
    pass


class NoAppointmentSelected(UserError):
    pass


class CanNotModifyVaccination(UserError):
    pass
