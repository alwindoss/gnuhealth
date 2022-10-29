# SPDX-FileCopyrightText: 2008-2022 Luis Falcón <falcon@gnuhealth.org>
# SPDX-FileCopyrightText: 2011-2022 GNU Solidario <health@gnusolidario.org>
#
# SPDX-License-Identifier: GPL-3.0-or-later

from trytond.exceptions import UserError, UserWarning
from trytond.model.exceptions import ValidationError


class PatientAlreadyPregnant(ValidationError):
    pass

