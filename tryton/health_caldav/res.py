# SPDX-FileCopyrightText: 2009-2013 Bertrand Chenal
# SPDX-FileCopyrightText: 2009-2016 B2CK
# SPDX-FileCopyrightText: 2009-2016 Cédric Krier
# SPDX-FileCopyrightText: 2009-2016 Tryton Foundation <info@tryton.org>
# SPDX-FileCopyrightText: 2016-2022 GNU Solidario <health@gnusolidario.org>
# SPDX-FileCopyrightText: 2016-2022 Luis Falcón <falcon@gnuhealth.org>
#
# SPDX-License-Identifier: GPL-3.0-or-later

from trytond.model import fields
from trytond.pool import PoolMeta
from trytond.pyson import Bool, Eval

__all__ = ['User']


class User(metaclass=PoolMeta):
    __name__ = 'res.user'

    calendars = fields.One2Many('calendar.calendar', 'owner', 'Calendars')

    @classmethod
    def __setup__(cls):
        super(User, cls).__setup__()
        required = Bool(Eval('calendars'))
        if not cls.email.states.get('required'):
            cls.email.states['required'] = required
        else:
            cls.email.states['required'] = (
                cls.email.states['required'] | required)
        if 'calendars' not in cls.email.depends:
            cls.email.depends.append('calendars')
