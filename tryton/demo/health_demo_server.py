#    Copyright (C) 2008-2011  Luis Falcon

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


import csv

from proteus import config, Model, Wizard


parties = csv.reader(open('parties.csv', 'r'))

    
config = config.set_trytond('gnuhealth_demo', database_type='postgresql', user='admin', password='admin')

def InitDatabase ():
    
    Module = Model.get('ir.module.module')
    (health_profile,) = Module.find([('name', '=', 'health_profile')])
    Module.button_install([health_profile.id], config.context)
    Wizard('ir.module.module.install_upgrade').execute('start')

InitDatabase()


def LoadParties ():
 
   
    Party = Model.get('party.party')

    parties = csv.reader(open('parties.csv', 'r'))

    header=True

    for line in parties:
        party = Party()
        party.name = line[0]
        party.lastname = line[1]
        if line[2]:
            party.ref = line[2]
        party.is_patient = False if line[3] == '0' else True
        party.is_doctor = False if line[4] == '0' else True
        party.is_insurance_company = False if line[5] == '0' else True
        party.is_institution = False if line[6] == '0' else True
        party.is_person = False if line[7] == '0' else True
        
# Skip the header
        if not header:
            print line, party.is_patient
            party.save()
        header=False
        
LoadParties()
        
        



