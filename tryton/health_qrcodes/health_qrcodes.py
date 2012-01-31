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


from trytond.model import ModelView, ModelSingleton, ModelSQL, fields
from trytond.tools import safe_eval, datetime_strftime
from trytond.transaction import Transaction
from trytond.pyson import Eval, Not, Equal, If, In, Bool, Get, Or, And, \
        PYSONEncoder
from trytond.pool import Pool



# Add the QR field and QR image in the party model

class PartyPatient (ModelSQL, ModelView):
    "Party"
    _name = "party.party"

    def make_qrcode(self, ids, name):
# Create the QR code 
        result = {}
        for party_data in self.browse(ids):
            qr_image = qrcode.make(party_data.name)
 
# Make a PNG image from PIL without the need to create a temp file            
            holder = StringIO.StringIO()
            qr_image.save(holder, format="PNG")
            qr_png = holder.getvalue()
            holder.close()

            result[party_data.id] = buffer(qr_png)

        return result

# Add the QR Code to the Party

    qr = fields.Function(fields.Binary('QR Code'), 'make_qrcode')


PartyPatient()

# Add the QR code field and image to the Newborn

class Newborn (ModelSQL, ModelView):
    "NewBorn"
    _name = "gnuhealth.newborn"

    def make_qrcode(self, ids, name):
# Create the QR code 
        result = {}
        for newborn_data in self.browse(ids):
            qr_image = qrcode.make(newborn_data.name)
 
# Make a PNG image from PIL without the need to create a temp file            
            holder = StringIO.StringIO()
            qr_image.save(holder, format="PNG")
            qr_png = holder.getvalue()
            holder.close()

            result[newborn_data.id] = buffer(qr_png)

        return result

# Add the QR Code to the Party

    qr = fields.Function(fields.Binary('QR Code'), 'make_qrcode')


Newborn()
