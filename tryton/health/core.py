##############################################################################
#
#    GNU Health HMIS: The Free Health and Hospital Information System
#    Copyright (C) 2008-2022 Luis Falcon <falcon@gnuhealth.org>
#    Copyright (C) 2011-2022 GNU Solidario <health@gnusolidario.org>
#
#    The GNU Health HMIS component is part of the GNU Health project
#    www.gnuhealth.org
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

# Core, commonly used ojects
import pytz

from dateutil.relativedelta import relativedelta
from datetime import datetime
from trytond.transaction import Transaction
from trytond.pool import Pool
from trytond.i18n import gettext

from .exceptions import (NoAssociatedHealthProfessional)


def convert_date_timezone(sdate, target):
    """
    Convert dates from UTC to local timezone and viceversa
    Datetime values are stored in UTC, so we need conversion
    """

    Company = Pool().get('company.company')

    institution_timezone = None
    company_id = Transaction().context.get('company')
    if company_id:
        company = Company(company_id)
        if company.timezone:
            institution_timezone = pytz.timezone(company.timezone)

    if (target == 'utc'):
        # Convert date to UTC timezone
        res = institution_timezone.localize(sdate).astimezone(pytz.utc)
    else:
        # Convert from UTC to institution local timezone
        res = pytz.utc.localize(sdate).astimezone(institution_timezone)
    return res


def compute_age_from_dates(dob, deceased, dod, gender, caller, extra_date):
    """ Get the person's age.

    Calculate the current age of the patient or age at time of death.

    Returns:
    If caller == 'age': str in Y-M-D,
       caller == 'childbearing_age': boolean,
       caller == 'raw_age': [Y, M, D]

    """
    today = datetime.today().date()

    if dob:
        start = datetime.strptime(str(dob), '%Y-%m-%d')
        end = datetime.strptime(str(today), '%Y-%m-%d')

        if extra_date:
            end = datetime.strptime(str(extra_date), '%Y-%m-%d')

        if deceased and dod:
            end = datetime.strptime(
                        str(dod), '%Y-%m-%d %H:%M:%S')

        rdelta = relativedelta(end, start)

        years_months_days = str(rdelta.years) + 'y ' \
            + str(rdelta.months) + 'm ' \
            + str(rdelta.days) + 'd'

    else:
        return None

    if caller == 'age':
        return years_months_days

    elif caller == 'childbearing_age':
        if (rdelta.years >= 11
           and rdelta.years <= 55 and gender == 'f'):
            return True
        else:
            return False

    elif caller == 'raw_age':
        return [rdelta.years, rdelta.months, rdelta.days]

    else:
        return None


def get_institution():
    # Retrieve the institution associated to this GNU Health instance
    # That is associated to the Company.
    company = Transaction().context.get('company')

    cursor = Transaction().connection.cursor()
    cursor.execute('SELECT party FROM company_company WHERE id=%s \
        LIMIT 1', (company,))
    party_id = cursor.fetchone()
    if party_id:
        cursor = Transaction().connection.cursor()
        cursor.execute('SELECT id FROM gnuhealth_institution WHERE \
            name = %s LIMIT 1', (party_id[0],))
        institution_id = cursor.fetchone()
        if (institution_id):
            return int(institution_id[0])


def get_health_professional(required=True):
    # Get the professional associated to the internal user id
    # that logs into GNU Health
    # If the method is called with the arg "required" as False, then
    # the error message won't be shown in the case of not finding
    # the corresponding healthprof (eg, creating a new appointment)
    cursor = Transaction().connection.cursor()
    User = Pool().get('res.user')
    user = User(Transaction().user)
    login_user_id = int(user.id)
    cursor.execute('SELECT id FROM party_party WHERE is_healthprof=True \
        AND internal_user = %s LIMIT 1', (login_user_id,))
    partner_id = cursor.fetchone()
    if partner_id:
        cursor = Transaction().connection.cursor()
        cursor.execute('SELECT id FROM gnuhealth_healthprofessional WHERE \
            name = %s LIMIT 1', (partner_id[0],))
        healthprof_id = cursor.fetchone()
        if (healthprof_id):
            return int(healthprof_id[0])
    else:
        if required:
            raise NoAssociatedHealthProfessional(gettext(
                ('health.msg_no_associated_health_professional'))
            )
