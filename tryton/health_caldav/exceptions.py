# This file is part of GNU Health.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.
# from trytond.exceptions import UserError, UserWarning
from trytond.model.exceptions import ValidationError


class InvalidCalendarExtension(ValidationError):
    pass


class InvalidRecurrence(ValidationError):
    pass


class InvalidBySecond(ValidationError):
    pass


class InvalidByMinute(ValidationError):
    pass


class InvalidByHour(ValidationError):
    pass


class InvalidByDay(ValidationError):
    pass


class InvalidByMonthDay(ValidationError):
    pass


class InvalidByWeekNumber(ValidationError):
    pass


class InvalidByYearDay(ValidationError):
    pass


class InvalidByMonth(ValidationError):
    pass


class InvalidBySetPosition(ValidationError):
    pass
