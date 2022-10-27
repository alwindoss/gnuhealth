#!/usr/bin/env python 
# SPDX-FileCopyrightText: 2008-2022 Luis Falcón <falcon@gnuhealth.org>
# SPDX-FileCopyrightText: 2011-2022 GNU Solidario <health@gnusolidario.org>
#
# SPDX-License-Identifier: GPL-3.0-or-later

#########################################################################
#   Hospital Management Information System (HMIS) component of the      #
#                       GNU Health project                              #
#                   https://www.gnuhealth.org                           #
#########################################################################
#                    health_csv_lab_interface.py                        #
#         Sample script to upload lab orders from a CSV file            #
#########################################################################

from proteus import config, Model
import csv
import sys

dbname = 'health40'
user = 'admin'
password = 'gnusolidario'
hostname = 'federation.gnuhealth.org'
port = '8000'

health_server = \
    'http://'+user+':'+password+'@'+hostname+':'+port+'/'+dbname+'/'

def check_lab_test():
    LabTest = Model.get('gnuhealth.lab')
    LabTestLine = Model.get('gnuhealth.lab.test.critearea')

    # Verify that each test exists at the DB before trying 
    # to upload the results
    csv_file = csv.reader(open(sys.argv[1], 'r'))
    for line in csv_file:
        test_id = line[0]
        analyte = line[1]
        if not (LabTest.find(['name','=',test_id])):
            exit("ERROR: Test %s not found" %test_id)
            
        if  not (LabTestLine.find([('name','=',analyte), \
            ('gnuhealth_lab_id','=',test_id)])):
            exit("ERROR: Analyte %s not found on %s" %(analyte, test_id))

    print ("Basic check on test ID and analytes succeeded")
            
def input_results():
    LabTestLine = Model.get('gnuhealth.lab.test.critearea')
    csv_file = csv.reader(open(sys.argv[1], 'r'))
    for line in csv_file:
        test_id = line[0]
        analyte = line[1]
        result = line[2]
        # Update the model with the result values
        for result_line in LabTestLine.find([('name','=',analyte), \
            ('gnuhealth_lab_id','=',test_id)]):
            result_line.result = float(result)
            result_line.save()

if (len(sys.argv) < 2):
    exit ("You need to specify a CSV file with the lab results")
    
print ("Connecting to GNU Health Server ...")
conf = config.set_xmlrpc(health_server)
print ("Connected !")

print ("Checking integrity of the batch file ...")
check_lab_test()
print ("Updating lab results from batch file ...")
input_results()
print ("Done !")
