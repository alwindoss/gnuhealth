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
#                       gnuhealth_product_uploader.py                   #
#         Sample script to upload products from a CSV file              #
#########################################################################

# Requirements
# Proteus version : 5.0.x 
# pip3 install --upgrade --user "proteus>=5.0,<5.1"

# ##### Usage ########
# python3 ./gnuhealth_product_uploader.py products_file_name.csv

# Product CSV Format
# Name,List Price,Cost Price,Type,UOM
# Sample csv content
# "Rapid urease test",15,12,"service","Unit"

from proteus import config, Model
import csv
import sys

from decimal import Decimal

dbname = 'health37dev'
user = 'admin'
password = 'gnusolidario'
hostname = 'localhost'
port = '8000'

health_server = \
    'http://'+user+':'+password+'@'+hostname+':'+port+'/'+dbname+'/'

            
def input_results():
    ProductInfo = Model.get('product.template')
    ProductUOM = Model.get('product.uom')
    csv_file = csv.reader(open(sys.argv[1], "r"))
    for line in csv_file:
        name = line[0]
        list_price = line[1]
        cost_price = line[2]
        product_type = line[3]
        uom = line[4]
        # Update the model with the result values
        product = ProductInfo ()
        product.name = name
        product.list_price = Decimal(list_price)
        product.cost_price = Decimal(cost_price)
        uom_val, = ProductUOM.find([('name','=',uom)])
        product.default_uom = uom_val
        
        product.save()

if (len(sys.argv) < 2):
    exit ("You need to specify a CSV file with the product list")
    
print ("Connecting to GNU Health Server ...")
conf = config.set_xmlrpc(health_server)
print ("Connected !")

print ("Updating products from batch file ...")
input_results()
print ("Done !")
