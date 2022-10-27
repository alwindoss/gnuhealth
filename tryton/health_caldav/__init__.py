# SPDX-FileCopyrightText: 2009-2013 Bertrand Chenal
# SPDX-FileCopyrightText: 2009-2016 B2CK
# SPDX-FileCopyrightText: 2009-2016 Cédric Krier
# SPDX-FileCopyrightText: 2009-2016 Tryton Foundation <info@tryton.org>
# SPDX-FileCopyrightText: 2016-2022 GNU Solidario <health@gnusolidario.org>
# SPDX-FileCopyrightText: 2016-2022 Luis Falcón <falcon@gnuhealth.org>
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""GNU Health Calendar for WebDAV3

The package is the continuation of the CalDAV functionality
for the discontinued Tryton package.

It has been ported to Python 3 and GNU Health.

It contains the models to use Calendars in GNU Health HMIS.



"""

from trytond.pool import Pool
from . import caldav
from . import webdav
from . import calendar_
from . import res


def register():
    Pool.register(
        webdav.Collection,
        calendar_.Calendar,
        calendar_.ReadUser,
        calendar_.WriteUser,
        calendar_.Category,
        calendar_.Location,
        calendar_.Event,
        calendar_.EventCategory,
        calendar_.EventAlarm,
        calendar_.EventAttendee,
        calendar_.EventRDate,
        calendar_.EventExDate,
        calendar_.EventRRule,
        calendar_.EventExRule,
        res.User,
        module='health_caldav', type_='model')
