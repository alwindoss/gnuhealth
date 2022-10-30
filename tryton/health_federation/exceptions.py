# SPDX-FileCopyrightText: 2008-2022 Luis Falcón <falcon@gnuhealth.org>
# SPDX-FileCopyrightText: 2011-2022 GNU Solidario <health@gnusolidario.org>
#
# SPDX-License-Identifier: GPL-3.0-or-later

from trytond.exceptions import UserError, UserWarning


class NeedLoginCredentials(UserError):
    pass


class ServerAuthenticationError(UserError):
    pass


class ThalamusConnectionError(UserError):
    pass


class ThalamusConnectionOK(UserWarning):
    pass


class NoInstitution(UserError):
    pass
