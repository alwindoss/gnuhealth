# Copyright (C) 2008-2022 Luis Falcon <falcon@gnuhealth.org>
# Copyright (C) 2011-2022 GNU Solidario <health@gnusolidario.org>
# SPDX-FileCopyrightText: 2008-2022 Luis Falcón <falcon@gnuhealth.org>
# SPDX-FileCopyrightText: 2011-2022 GNU Solidario <health@gnusolidario.org>
#
# SPDX-License-Identifier: GPL-3.0-or-later

from sql.aggregate import Count
from sql.functions import DateTrunc
from datetime import date, datetime
from trytond.report import Report
from trytond.pool import Pool
from trytond.transaction import Transaction
from dateutil.relativedelta import relativedelta

__all__ = ['InstitutionSummaryReport']


class InstitutionSummaryReport(Report):
    __name__ = 'gnuhealth.summary.report'

    @classmethod
    def get_population_with_no_dob(cls):
        """ Return Total Number of living people in the system
        without a date of birth"""
        pool = Pool()
        Party = pool.get('party.party')

        return Party.search([
                ('is_person', '=', True),
                ('deceased', '!=', True),
                ('dob', '=', None),
                ], count=True)

    @classmethod
    def get_population(cls, date1, date2, gender, total):
        """ Return Total Number of living people in the system
        segmented by age group and gender"""
        pool = Pool()
        Party = pool.get('party.party')

        domain = [
            ('deceased', '!=', True),
            ('gender', '=', gender),
            ]

        if not total:
            domain.append(('dob', '>=', date2))
            domain.append(('dob', '<=', date1))

        return Party.search(domain, count=True)

    @classmethod
    def get_new_people(cls, start_date, end_date, in_health_system):
        """ Return Total Number of new registered persons alive """
        pool = Pool()
        Party = pool.get('party.party')

        domain = [
            ('activation_date', '>=', start_date),
            ('activation_date', '<=', end_date),
            ('deceased', '!=', True),
            ('is_person', '=', True),
            ]

        if in_health_system:
            domain.append(('is_patient', '=', True))

        return Party.search(domain, count=True)

    @classmethod
    def get_new_births(cls, start_date, end_date):
        """ Return birth certificates within that period """
        pool = Pool()
        BirthCertificate = pool.get('gnuhealth.birth_certificate')

        return BirthCertificate.search([
                ('dob', '>=', start_date),
                ('dob', '<=', end_date),
                ], count=True)

    @classmethod
    def get_new_deaths(cls, start_date, end_date):
        """ Return death certificates within that period """
        """ Truncate the timestamp of DoD to match a whole day"""
        pool = Pool()
        DeathCertificate = pool.get('gnuhealth.death_certificate')
        table = DeathCertificate.__table__()

        dod = DateTrunc('day', table.dod)

        cursor = Transaction().connection.cursor()
        cursor.execute(*table.select(
                Count(table.dod),
                where=((dod >= start_date) & (dod <= end_date))))
        return cursor.fetchone()

    @classmethod
    def get_evaluations(cls, start_date, end_date, dx, count=False):
        """ Return evaluation info """
        pool = Pool()

        Evaluation = pool.get('gnuhealth.patient.evaluation')
        start_date = datetime.strptime(str(start_date), '%Y-%m-%d')
        end_date = datetime.strptime(str(end_date), '%Y-%m-%d')
        end_date += relativedelta(hours=+23, minutes=+59, seconds=+59)

        clause = [
            ('evaluation_start', '>=', start_date),
            ('evaluation_start', '<=', end_date),
            ]

        if dx:
            clause.append(('diagnosis', '=', dx))

        return Evaluation.search(clause, count=count)

    @classmethod
    def count_evaluations(cls, start_date, end_date, dx):
        """ count diagnoses by groups """
        return cls.get_evaluation(start_date, end_date, dx, count=True)

    @classmethod
    def get_context(cls, records, header, data):
        context = super(
            InstitutionSummaryReport, cls).get_context(records, header, data)

        start_date = data['start_date']
        end_date = data['end_date']

        context['demographics'] = data['demographics']
        context['patient_evaluations'] = data['patient_evaluations']

        context['start_date'] = data['start_date']
        context['end_date'] = data['end_date']

        # Demographics
        today = date.today()

        context[''.join(['p', 'total_', 'f'])] = \
            cls.get_population(None, None, 'f', total=True)

        context[''.join(['p', 'total_', 'm'])] = \
            cls.get_population(None, None, 'm', total=True)

        # Living people with NO date of birth
        context['no_dob'] = \
            cls.get_population_with_no_dob()

        # Build the Population Pyramid for registered people
        for age_group in range(0, 21):
            date1 = today - relativedelta(years=(age_group*5))
            date2 = today - relativedelta(years=((age_group*5)+5), days=-1)

            context[''.join(['p', str(age_group), 'f'])] = \
                cls.get_population(date1, date2, 'f', total=False)
            context[''.join(['p', str(age_group), 'm'])] = \
                cls.get_population(date1, date2, 'm', total=False)

        # Count those lucky over 105 years old :)
        date1 = today - relativedelta(years=105)
        date2 = today - relativedelta(years=200)

        context['over105f'] = \
            cls.get_population(date1, date2, 'f', total=False)
        context['over105m'] = \
            cls.get_population(date1, date2, 'm', total=False)

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

        # Get evaluations within the specified date range

        context['evaluations'] = \
            cls.get_evaluations(start_date, end_date, None)

        evaluations = cls.get_evaluations(start_date, end_date, None)

        eval_dx = []
        non_dx_eval = 0
        non_age_eval = 0
        eval_f = 0
        eval_m = 0

        # Global Evaluation info
        for evaluation in evaluations:
            if evaluation.diagnosis:
                eval_dx.append(evaluation.diagnosis)
            else:
                # Increase the evaluations without Dx counter
                non_dx_eval += 1
            if (evaluation.gender == 'f'):
                eval_f += 1
            else:
                eval_m += 1

            if not evaluation.computed_age:
                non_age_eval += 1

        context['non_dx_eval'] = non_dx_eval
        context['eval_num'] = len(evaluations)
        context['eval_f'] = eval_f
        context['eval_m'] = eval_m
        context['non_age_eval'] = non_age_eval

        # Create a set to work with single diagnoses
        # removing duplicate entries from eval_dx

        unique_dx = set(eval_dx)

        summary_dx = []
        # Traverse the evaluations with Dx to get the key values
        for dx in unique_dx:
            # unique_evaluations holds the evaluations with
            # the same diagnostic
            unique_evaluations = cls.get_evaluations(start_date, end_date, dx)

            group_1 = group_2 = group_3 = group_4 = group_5 = 0
            group_1f = group_2f = group_3f = group_4f = group_5f = 0

            total_evals = len(unique_evaluations)

            new_conditions = 0

            for unique_eval in unique_evaluations:

                if (unique_eval.computed_age):

                    # Strip to get the raw year
                    age = int(unique_eval.computed_age.split(' ')[0][:-1])

                    # Age groups in this diagnostic
                    if (age < 5):
                        group_1 += 1
                        if (unique_eval.gender == 'f'):
                            group_1f += 1
                    if (age in range(5, 14)):
                        group_2 += 1
                        if (unique_eval.gender == 'f'):
                            group_2f += 1
                    if (age in range(15, 45)):
                        group_3 += 1
                        if (unique_eval.gender == 'f'):
                            group_3f += 1
                    if (age in range(46, 60)):
                        group_4 += 1
                        if (unique_eval.gender == 'f'):
                            group_4f += 1
                    if (age > 60):
                        group_5 += 1
                        if (unique_eval.gender == 'f'):
                            group_5f += 1

                # Check for new conditions vs followup / chronic checkups
                # in the evaluation with a particular diagnosis

                if (unique_eval.visit_type == 'new'):
                    new_conditions += 1

            eval_dx = {
                'diagnosis': unique_eval.diagnosis.rec_name,
                'age_group_1': group_1, 'age_group_1f': group_1f,
                'age_group_2': group_2, 'age_group_2f': group_2f,
                'age_group_3': group_3, 'age_group_3f': group_3f,
                'age_group_4': group_4, 'age_group_4f': group_4f,
                'age_group_5': group_5, 'age_group_5f': group_5f,
                'total': total_evals, 'new_conditions': new_conditions,
                }

            # Append into the report list the resulting
            # dictionary entry

            summary_dx.append(eval_dx)

        context['summary_dx'] = summary_dx

        return context
