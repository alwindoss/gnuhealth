# SPDX-FileCopyrightText: 2009-2013 Bertrand Chenal
# SPDX-FileCopyrightText: 2009-2016 B2CK
# SPDX-FileCopyrightText: 2009-2016 Cédric Krier
# SPDX-FileCopyrightText: 2016-2022 GNU Solidario <health@gnusolidario.org>
# SPDX-FileCopyrightText: 2016-2022 Luis Falcón <falcon@gnuhealth.org>
#
# SPDX-License-Identifier: GPL-3.0-or-later

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
