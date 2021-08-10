# This file is part of GNU Health.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.
from trytond.exceptions import UserError, UserWarning
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
