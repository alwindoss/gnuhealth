# coding=utf-8

#    Copyright (C) 2008-2012 Luis Falcon <lfalcon@gnusolidario.org>

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

import qrcode
import StringIO
from trytond.model import ModelView, ModelSQL, fields


# Add the QR field and QR image in the patient model

class Patient(ModelSQL, ModelView):
    'Patient'
    _name = 'gnuhealth.patient'

    def make_qrcode(self, ids, name):
# Create the QR code
        result = {}
        for patient_data in self.browse(ids):

            if not patient_data.ssn:
                patient_data.ssn = ''

            if not patient_data.blood_type:
                patient_data.blood_type = ''

            if not patient_data.rh:
                patient_data.rh = ''

            if not patient_data.sex:
                patient_data.sex = ''

            if not patient_data.dob:
                patient_data.sex = ''

            if not patient_data.identification_code:
                patient_data.identification_code = ''

            if not patient_data.lastname:
                patient_data.lastname = ''

            qr_string = 'ID: ' + patient_data.identification_code \
                + '\nName: ' + patient_data.lastname + ',' \
                        + patient_data.name.name \
                + '\nSSN: ' + patient_data.ssn \
                + '\nSex: ' + patient_data.sex \
                + '\nDoB: ' + str(patient_data.dob) \
                + '\nDoB: ' + patient_data.blood_type + ' ' + patient_data.rh

            qr_image = qrcode.make(qr_string)

# Make a PNG image from PIL without the need to create a temp file
            holder = StringIO.StringIO()
            qr_image.save(holder, format='PNG')
            qr_png = holder.getvalue()
            holder.close()

            result[patient_data.id] = buffer(qr_png)

        return result

# Add the QR Code to the Patient
    qr = fields.Function(fields.Binary('QR Code'), 'make_qrcode')

Patient()


# Add the QR code field and image to the Newborn

class Newborn(ModelSQL, ModelView):
    'NewBorn'
    _name = 'gnuhealth.newborn'

    def make_qrcode(self, ids, name):
# Create the QR code
        result = {}
        for newborn_data in self.browse(ids):

            if not newborn_data.name:
                newborn_data.name = ''

            qr_string = 'ID: ' + newborn_data.name \
                + '\nMother: ' + newborn_data.mother.name.lastname + ',' \
                        + newborn_data.mother.name.name \
                + '\nMother\'s ID: ' \
                        + newborn_data.mother.identification_code \
                + '\nSex: ' + newborn_data.sex \
                + '\nDoB: ' + str(newborn_data.birth_date)

            qr_image = qrcode.make(qr_string)

# Make a PNG image from PIL without the need to create a temp file
            holder = StringIO.StringIO()
            qr_image.save(holder, format='PNG')
            qr_png = holder.getvalue()
            holder.close()

            result[newborn_data.id] = buffer(qr_png)

        return result

# Add the QR Code to the Newborn
    qr = fields.Function(fields.Binary('QR Code'), 'make_qrcode')

Newborn()
