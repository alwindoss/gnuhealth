# This file is part of GNU Health.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.
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
