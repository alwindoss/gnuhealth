patient_uploader.py

Simple script to upload people demographics from a CSV formatted file.  

Functionality :
Small SAMPLE proteus script to create the parties and their respective patients
from a CSV file

CSV Format :
# CSV Format :
# "FIRST NAME","FAMILY NAME", "PUID", "Gender", "DoB", "Phone",
# "Alternative ID","address 1 (eg street)", "addr cont (city..)",
# "activation date"


Requirements :
This version works with the following versions :

- GNU Health : 4.0 
- Proteus library : 6.0 

Installing proteus :
$ pip install --user "proteus>=6.0,<6.1"


Usage :
Invoke the program and pass the csv formatted file as an argument
eg:

$ python ./patient_uploader.py demographics.csv localhost:8000 admin:init healthdev39
 
  "admin" and "init" are the correspond to the specific user and passwd 
  "healthdev39" is the database name

The main steps are :
- Test connection to the GNU Health server.
- Upload the person demographic information.
- Create the patient associated to the person.


This is part of GNU Health Hospital Management component
https://www.gnuhealth.org
