# This file is part of GNU Health.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.
from trytond.exceptions import UserError, UserWarning
from trytond.model.exceptions import ValidationError


class NoCompanyTimezone(ValidationError):
    pass


class EndDateBeforeStart(ValidationError):
    pass


class PeriodTooLong(ValidationError):
    pass


class AppointmentEndDateBeforeStart(ValidationError):
    pass
