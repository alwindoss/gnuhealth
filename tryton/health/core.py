# SPDX-FileCopyrightText: 2008-2022 Luis Falcón <falcon@gnuhealth.org>
# SPDX-FileCopyrightText: 2011-2022 GNU Solidario <health@gnusolidario.org>
#
# SPDX-License-Identifier: GPL-3.0-or-later

#########################################################################
#   Hospital Management Information System (HMIS) component of the      #
#                       GNU Health project                              #
#                   https://www.gnuhealth.org                           #
#########################################################################
#                           HEALTH package                              #
#               core.py: commonly used ojects and methods               #
#########################################################################

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


def estimated_date_from_years(years_old):
    """ returns a date of substracting the
        referred number of years from today's date
        It can be used in different context, such as to estimate
        the date of birth from a referred age in years
    """

    today = datetime.today().date()
    est_dob = today - relativedelta(years=years_old)
    return est_dob


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
    pool = Pool()
    Company = pool.get('company.company')
    Institution = pool.get('gnuhealth.institution')
    company = Company.__table__()
    institution = Institution.__table__()

    company_id = Transaction().context.get('company')

    cursor = Transaction().connection.cursor()
    cursor.execute(*company.join(institution, condition=(
                institution.name == company.party)).select(
            institution.id,
            where=(company.id == company_id)))
    institution_id = cursor.fetchone()
    if institution_id:
        return int(institution_id[0])


def get_health_professional(required=True):
    # Get the professional associated to the internal user id
    # that logs into GNU Health
    # If the method is called with the arg "required" as False, then
    # the error message won't be shown in the case of not finding
    # the corresponding healthprof (eg, creating a new appointment)
    pool = Pool()
    Party = pool.get('party.party')
    Professional = pool.get('gnuhealth.healthprofessional')
    party = Party.__table__()
    professional = Professional.__table__()

    cursor = Transaction().connection.cursor()
    cursor.execute(
        *party.join(professional,
                    condition=(professional.name == party.id)).select(
            professional.id,
            where=(
                (party.is_healthprof)
                & (party.internal_user == Transaction().user))))
    healthprof_id = cursor.fetchone()
    if healthprof_id:
        return int(healthprof_id[0])
    else:
        if required:
            raise NoAssociatedHealthProfessional(gettext(
                ('health.msg_no_associated_health_professional'))
            )
