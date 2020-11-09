#!/usr/bin/env python3
##############################################################################
#
#     GNU Health Fast Healthcare Interoperability Resources - FHIR - Server
#              The FHIR Server is part of the GNU Health project
#
##############################################################################
#
#    Copyright (C) 2015 - 2018  Chris Zimmerman 
#    Copyright (C) 2018 - 2020  GNU Solidario <health@gnusolidario.org>
#    Copyright (C) 2020         Luis Falcon  <falcon@gnuhealth.org>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from setuptools import setup, find_packages

long_desc = open("README.rst", "r").read()

version = open("version").read().strip()

setup(name='gnuhealth-fhir-server',
    version=version,
    description = 'The GNU Health FHIR Server',
    keywords='health API REST HL7 FHIR',
    long_description = long_desc,
    platforms='any',
    author='GNU Solidario',
    author_email='info@gnuhealth.org',
    url='https://www.gnuhealth.org',
    download_url='http://ftp.gnu.org/gnu/health',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Flask',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Healthcare Industry',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Topic :: Scientific/Engineering :: Medical Science Apps.',
        ],
    install_requires = [
        "defusedxml>=0.4.1",
        "Flask>=0.10.1",
        "Flask-Login>=0.3.2",
        "Flask-RESTful>=0.3.2",
        "flask-tryton",
        "Flask-WTF>=0.11"
    ],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
 )
