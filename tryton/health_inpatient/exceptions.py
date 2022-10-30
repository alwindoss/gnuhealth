# SPDX-FileCopyrightText: 2008-2022 Luis Falcón <falcon@gnuhealth.org>
# SPDX-FileCopyrightText: 2011-2022 GNU Solidario <health@gnusolidario.org>
#
# SPDX-License-Identifier: GPL-3.0-or-later

from trytond.exceptions import UserError, UserWarning
from trytond.model.exceptions import ValidationError


class NoAssociatedHealthProfessional(ValidationError):
    pass


class DischargeReasonNeeded(UserError):
    pass


class DischargeBeforeAdmission(UserError):
    pass


class BedIsNotAvailable(UserError):
    pass


class DestinationBedNotAvailable(UserError):
    pass


class NeedTimeZone(UserError):
    pass


class AdmissionMustBeToday(UserError):
    pass


class ManyRecordsChosen(UserError):
    pass


class NoRecordSelected(UserError):
    pass


class SpecialMealNeeds(UserWarning):
    pass
