# -*- coding: utf-8 -*-
##############################################################################
#
#    GNU Health: The Free Health and Hospital Information System
#    Copyright (C) 2008-2020 Luis Falcon <falcon@gnuhealth.org>
#    Copyright (C) 2011-2020 GNU Solidario <health@gnusolidario.org>
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
from datetime import date, datetime
from trytond.report import Report
from trytond.pool import Pool
from trytond.transaction import Transaction
from dateutil.relativedelta import relativedelta

from matplotlib import pyplot as plt
from matplotlib.ticker import MaxNLocator

import io

__all__ = ['InstitutionEpidemicsReport']

class InstitutionEpidemicsReport(Report):
    __name__ = 'gnuhealth.epidemics.report'


    @classmethod
    def get_population_with_no_dob(cls):
        """ Return Total Number of living people in the system 
        without a date of birth"""
        cursor = Transaction().connection.cursor()

        # Check for entries without date of birth
        cursor.execute("SELECT COUNT(id) \
            FROM party_party WHERE is_person is TRUE and \
            deceased is not TRUE and dob is null")

        res = cursor.fetchone()[0]

        return(res)

    @classmethod
    def get_population(cls,date1,date2,gender,total):
        """ Return Total Number of living people in the system 
        segmented by age group and gender"""
        cursor = Transaction().connection.cursor()

        if (total):
            cursor.execute("SELECT COUNT(id) \
                FROM party_party WHERE \
                gender = %s and deceased is not TRUE",(gender))

        else:
            cursor.execute("SELECT COUNT(id) \
                FROM party_party \
                WHERE dob BETWEEN %s and %s AND \
                gender = %s  \
                and deceased is not TRUE" ,(date2, date1, gender))

        res = cursor.fetchone()[0]

        return(res)

    @classmethod
    def get_new_people(cls, start_date, end_date, in_health_system):
        """ Return Total Number of new registered persons alive """

        query = "SELECT COUNT(activation_date) \
            FROM party_party \
            WHERE activation_date BETWEEN \
            %s AND %s and is_person=True and deceased is not TRUE"
        if (in_health_system):
            query = query + " and is_patient=True"
        cursor = Transaction().connection.cursor()
        cursor.execute(query,(start_date, end_date))
        res = cursor.fetchone()
        return(res)

    @classmethod
    def get_new_births(cls, start_date, end_date):
        """ Return birth certificates within that period """

        query = "SELECT COUNT(dob) \
            FROM gnuhealth_birth_certificate \
            WHERE dob BETWEEN \
            %s AND %s"

        cursor = Transaction().connection.cursor()
        cursor.execute(query,(start_date, end_date))

        res = cursor.fetchone()
        return(res)

    @classmethod
    def get_new_deaths(cls, start_date, end_date):
        """ Return death certificates within that period """
        """ Truncate the timestamp of DoD to match a whole day"""

        query = "SELECT COUNT(dod) \
            FROM gnuhealth_death_certificate \
            WHERE date_trunc('day', dod) BETWEEN \
            %s AND %s"

        cursor = Transaction().connection.cursor() 
        cursor.execute(query,(start_date, end_date))

        res = cursor.fetchone()
        return(res)

    @classmethod
    def get_confirmed_cases(cls, start_date, end_date, dx):
        """ Return number of confirmed cases """

        Condition = Pool().get('gnuhealth.patient.disease')

        clause = [
            ('diagnosed_date', '>=', start_date),
            ('diagnosed_date', '<=', end_date),
            ]

        if dx:
            clause.append(('pathology', '=', dx))

        res = Condition.search(clause)

        return(res)

    @classmethod
    def get_epi_by_day(cls, start_date, end_date, dx):
        """ Return number of confirmed cases """

        Condition = Pool().get('gnuhealth.patient.disease')

        current_day = start_date
        aggr = []
        while current_day <= end_date:
            current_day = current_day + relativedelta(days=1)

            clause = [
                ('diagnosed_date', '=', current_day),
                ]

            if dx:
                clause.append(('pathology', '=', dx))

            res = Condition.search(clause)
            cases_day = len(res)
            daily_data = {'date':str(current_day), 'cases':cases_day}
            aggr.append(daily_data)
        return(aggr)


    @classmethod
    def get_context(cls, records, data):
        Condition = Pool().get('gnuhealth.pathology')

        context = super(InstitutionEpidemicsReport, cls).get_context(records, data)

        start_date = data['start_date']
        context['start_date'] = data['start_date']

        end_date = data['end_date']
        context['end_date'] = data['end_date']

        demographics = data['demographics']
        context['demographics'] = data['demographics']

        health_condition = data['health_condition']
        context['health_condition'] = Condition.search(
                [('id', '=', health_condition)], limit=1)[0]

        # Demographics
        today = date.today()

        context[''.join(['p','total_','f'])] = \
            cls.get_population (None,None,'f', total=True)

        context[''.join(['p','total_','m'])] = \
            cls.get_population (None,None,'m', total=True)

        # Living people with NO date of birth
        context['no_dob'] = \
            cls.get_population_with_no_dob()

        # Build the Population Pyramid for registered people

        for age_group in range (0,21):
            date1 = today - relativedelta(years=(age_group*5))
            date2 = today - relativedelta(years=((age_group*5)+5), days=-1)

            context[''.join(['p',str(age_group),'f'])] = \
                cls.get_population (date1,date2,'f', total=False)
            context[''.join(['p',str(age_group),'m'])] = \
                cls.get_population (date1,date2,'m', total=False)


        # Count those lucky over 105 years old :)
        date1 = today - relativedelta(years=105)
        date2 = today - relativedelta(years=200)

        context['over105f'] = \
            cls.get_population (date1,date2,'f', total=False)
        context['over105m'] = \
            cls.get_population (date1,date2,'m', total=False)


        # Count registered people, and those within the system of health
        context['new_people'] = \
            cls.get_new_people(start_date, end_date, False)
        context['new_in_health_system'] = \
            cls.get_new_people(start_date, end_date, in_health_system=True)

        # New births
        context['new_births'] = \
            cls.get_new_births(start_date, end_date)

        # New deaths
        context['new_deaths'] = \
            cls.get_new_deaths(start_date, end_date)

        # Get cases within the specified date range

        confirmed_cases = cls.get_confirmed_cases(start_date, end_date, health_condition)

        context['confirmed_cases'] = confirmed_cases

        epidemics_dx =[]
        non_age_cases = 0
        cases_f = 0
        cases_m = 0


        # Global Condition info
        for confirmed_case in confirmed_cases:
            if (confirmed_case.name.gender == 'f'):
                cases_f +=1
            else:
                cases_m +=1

            if not confirmed_case.name.age:
                non_age_cases +=1

        total_cases = len(confirmed_cases)

        context['confirmed_cases_num'] = total_cases
        context['cases_f'] = cases_f
        context['cases_m'] = cases_m
        context['non_age_cases'] = non_age_cases


        group_1 = group_2 = group_3 = group_4 = group_5 = 0
        group_1f = group_2f = group_3f = group_4f = group_5f = 0


        for case in confirmed_cases:

            if (case.name.age):

                #Strip to get the raw year
                age = int(case.name.age.split(' ')[0][:-1])


                # Age groups in this diagnostic
                if (age < 5):
                    group_1 += 1
                    if (case.name.gender == 'f'):
                        group_1f += 1
                if (age in range(5,14)):
                    group_2 += 1
                    if (case.name.gender == 'f'):
                        group_2f += 1
                if (age in range(15,45)):
                    group_3 += 1
                    if (case.name.gender == 'f'):
                        group_3f += 1
                if (age in range(46,60)):
                    group_4 += 1
                    if (case.name.gender == 'f'):
                        group_4f += 1
                if (age > 60):
                    group_5 += 1
                    if (case.name.gender == 'f'):
                        group_5f += 1

        cases = {'diagnosis': health_condition,
            'age_group_1': group_1, 'age_group_1f': group_1f,
            'age_group_2': group_2, 'age_group_2f': group_2f,
            'age_group_3': group_3, 'age_group_3f': group_3f,
            'age_group_4': group_4, 'age_group_4f': group_4f,
            'age_group_5': group_5, 'age_group_5f': group_5f,
            'total': total_cases,}

        # Append into the report list the resulting
        # dictionary entry

        epidemics_dx.append(cases)

        context['epidemics_dx'] = epidemics_dx

        epi_series = cls.get_epi_by_day(start_date, end_date, health_condition)

        days=[]
        cases_day=[]
        for day in epi_series:
            days.append(day['date'])
            # Confirmed cases by day
            cases_day.append(day['cases'])

        fig = plt.figure(figsize=(6,3))
        cases_by_day = fig.add_subplot(1, 1, 1)
        cases_by_day.set_title('New cases by day')
        cases_by_day.plot(days,cases_day, linewidth=2)
        fig.autofmt_xdate()
        cases_by_day.yaxis.set_major_locator(MaxNLocator(integer=True))

        holder = io.BytesIO()
        fig.savefig(holder)
        image_png = holder.getvalue()

        holder.close()
        context['histogram'] = image_png

        return context
