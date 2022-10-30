# SPDX-FileCopyrightText: 2008-2022 Luis Falcón <falcon@gnuhealth.org>
# SPDX-FileCopyrightText: 2011-2022 GNU Solidario <health@gnusolidario.org>
#
# SPDX-License-Identifier: GPL-3.0-or-later

# This file is part of GNU Health.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.
from trytond.exceptions import UserError
from trytond.model.exceptions import ValidationError


class DiscountPctOutOfRange(ValidationError):
    pass

class NeedAPolicy(ValidationError):
    pass

class DiscountWithoutElement(ValidationError):
    pass


class ServiceInvoiced(UserError):
    pass


class NoInvoiceAddress(UserError):
    pass


class NoPaymentTerm(UserError):
    pass

class NoAccountReceivable(UserError):
    pass
