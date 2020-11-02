THE GNU HEALTH FHIR SERVER
==========================

The GNU Health Fast Healthcare Interoperability Resources (FHIR) Server allows to query different resources from a 
running GNU Health HMIS node.

The GH FHIR server runs in Python3 and GNU Health HMIS node 3.6 or higher

Installation
------------

The GNU Health FHIR server is pip installable

The server requires Flask and a few of its addons. And, of course, a working GNU Health HMIS instance. 


Configuration
-------------

The server ships with a simple production config file. However, it needs to be edited.

    server/config.py
    ----------------
    TRYTON_DATABASE = ''    # GNU Health database
    SERVER_NAME = ''        # Domain name of the server (e.g., fhir.example.com)
    SECRET_KEY = ''         # Set this value to a long and random string

There are other options available for Flask and its addons:
* [Flask](http://flask.pocoo.org/)
* [Flask-Login](https://flask-login.readthedocs.org/en/latest/)
* [Flask-Tryton](https://pypi.org/project/flask-tryton/)
* [Flask-Restful](http://flask-restful.readthedocs.org/en/latest/quickstart.html)
* [Flask-WTF](https://flask-wtf.readthedocs.org/en/latest/)

Security
--------

Use TLS. Sensitive medical information must be protected and confidential.

By default, all FHIR endpoints except the Conformance statement require user authentication. The user authentication and access follows Tryton's model, respecting model and field access rights.

The same credentials used to sign into GNU Health are used to access the FHIR REST server.

Running the server
-----------------

The server ships with a simple script (run_server.py) to run the server using [Tornado](http://www.tornadoweb.org/en/stable/).

As the gnuhealth user, run the server.

    $ python3 run_server.py


