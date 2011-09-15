# -*- coding: utf-8 -*-
from trytond.transaction import Transaction
from trytond.modules.company import CompanyReport


class LabTest(CompanyReport):
    _name = 'patient.labtest'

    def parse(self, report, objects, datas, localcontext):
        localcontext['get_test'] = self._get_test
        localcontext['get_doctor_id'] = self.get_doctor_id
        localcontext['get_doctor'] = self.get_doctor
        return super(LabTest, self).parse(report, objects, datas,
                localcontext)

    def _get_test(self, patient):
        doctor_id = self.get_doctor_id()
        if doctor_id:
            test_ids = self.pool.get('gnuhealth.patient.lab.test').search([
                    ('doctor_id', '=', doctor_id),
                    ('patient_id', '=', patient.id),
                    ('state', '=', 'draft'),
                ])
            if test_ids:
                return self.pool.get(
                        'gnuhealth.patient.lab.test').browse(test_ids)
        return []

    def get_doctor_id(self):
        user_obj = self.pool.get('res.user')
        user = user_obj.browse(Transaction().user)
        uid = int(user.id)

        party_id = self.pool.get('party.party').search([
                ('internal_user', '=', uid)])
        if party_id:
            physician_id = self.pool.get('gnuhealth.physician').search([
                    ('name', 'in', party_id)])
            if physician_id:
                return physician_id[0]
        return False

    def get_doctor(self):
        user_obj = self.pool.get('res.user')
        user = user_obj.browse(Transaction().user)
        uid = int(user.id)

        party_id = self.pool.get('party.party').search([
                ('internal_user', '=', uid)])
        if party_id:
            return self.pool.get('party.party').read(
                    party_id, ['name'])[0]['name']
        else:
            return ''

LabTest()


class LabTestReport(CompanyReport):
    _name = 'patient.labtest.report'

LabTestReport()
