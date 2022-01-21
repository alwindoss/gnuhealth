# This file is part of GNU Health.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.
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
