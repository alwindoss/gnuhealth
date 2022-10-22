.. SPDX-FileCopyrightText: 2008-2022 Luis Falcón 
..
.. SPDX-License-Identifier: CC-BY-SA-4.0

gnuhealth_csv_lab_interface.py

Simple script to show ways to interface with GNU Health in a
non-interactive way.
This program reads a CSV formatted file with that contains the 
lab test id, the analytes and its results.
Included in this directory a sample TEST006.csv, that contains the results of
the test "TEST006", a "Complete Blood Count - CBC" 


Requirements :
This version works with the following versions :

- GNU Health : 4.0 
- Proteus library : 6.0

Installing proteus :
$ pip3 install --user "proteus>=6.0,<6.1"


Usage :
Invoke the program and pass the csv formatted file as an argument
eg:

$ ./gnuhealth_csv_lab_interface.py TEST006.csv

The main steps are :
- Test connection to the GNU Health server
- Check that the Lab test has been created on GNU Health (eg, TEST006)
- Check that the analytes from the csv files are on the system
- Upload the results.


This is part of GNU Health, the Free Hospital and Health Information System
https://www.gnuhealth.org
