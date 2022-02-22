#    Copyright (C) 2008-2022 Luis Falcon
#    Copyright (C) 2008-2022 GNU SOLIDARIO

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

# Functionality :
# Small SAMPLE proteus script to create the parties and their respective patients 
# from a CSV file

# CSV Format :
# "FIRST NAME","FAMILY NAME", "PUID", "Gender", "DoB", "Phone",
# "Alternative ID","address 1 (eg street)", "addr cont (city..)",
# "activation date"

# Usage: patient_uploader <csv_file> <hostname:port> <user:password> <dbname>

from datetime import datetime
import sys
import csv

from proteus import Model
from proteus import config as pconfig


def PartyDemographics(line):
    Party = Model.get('party.party')
    PartyAddress = Model.get('party.address')
    PartyAlternativeID = Model.get('gnuhealth.person_alternative_identification')
    ContactMethod = Model.get('party.contact_mechanism')
    Patient = Model.get('gnuhealth.patient')

    party = Party()

    party.name = line[0]
    party.lastname = line[1]
    party.ref = line[2]
    party.is_patient = True
    party.is_person = True

    if line[3] and (line[3] in ['m','f','u']):
        party.gender = line[3]

    # Set Date of birth
    try:
        party.dob = datetime.strptime(line[4], '%d/%m/%Y')
    except:
        party.dob = None

    # Set telephone number (mobile)

    if line[5]:
        contactmethod = ContactMethod()
        contactmethod.type = 'mobile'
        contactmethod.value = line[5]
        
        party.contact_mechanisms.append(contactmethod)
        
    # Set alternative Identification
    if line[6]:
        party.alternative_identification = True
        altid = PartyAlternativeID()
        altid.alternative_id_type = 'other'
        altid.code = line[6]

        party.alternative_ids.append(altid)


    # Set the party address

    address = PartyAddress()

    if line[7]:
        address.street = line[7]
 
    if line[8]:
        address.city = line[8]


    # Use this if one address only, so it won't leave the first record blank
    party.addresses[0] = address

    # For multiple addresses, append . party.addresses.append(address)
    try:
        party.activation_date = datetime.strptime(line[9], '%d/%m/%Y')
    except:
        party.activation_date = None


    party.save()

    patient = Patient()
    patient.name = party
    
    patient.save()


# Parse the CSV file
counter=0


if (len(sys.argv) < 4):
    exit ("usage: ./patient_uploader <csv_file> \
        <hostname> <port> <user> <password> <dbname>")

csv_file = csv.reader(open(sys.argv[1], 'r'))

# Set the connection params
hostname = sys.argv[2]
port = sys.argv[3]
user = sys.argv[4]
passwd = sys.argv[5]
dbname = sys.argv[6]

health_server = 'http://'+user+':'+passwd+'@'+hostname+':'+port+'/'+dbname+'/'

print ("Connecting to GNU Health Server ...")
conf = pconfig.set_xmlrpc(health_server)
# Use XML RPC using session
#conf = pconfig.set_xmlrpc_session(health_server, username=user, password=passwd)
print ("Connected !")

next(csv_file) #Skip header

for line in csv_file:
    counter=counter+1
    print ("Uploading patient #", counter, line)
    PartyDemographics(line)   
