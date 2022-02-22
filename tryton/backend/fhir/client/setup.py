#!/usr/bin/env python
# -*- coding: utf-8 -*-
#    Copyright (C) 2014-2017 Luis Falcon <lfalcon@gnuhealth.org>
#    Copyright (C) 2014-2017 GNU Solidario <health@gnusolidario.org>

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

from setuptools import setup
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()



setup(name='fhir',
    version='0.0.4',
    description='HL7 FHIR Library',
    author='Luis Falcon',
    author_email='lfalcon@gnusolidario.org',
    url='https://www.gnuhealth.org',
    download_url='http://ftp.gnu.org/gnu/health/',
    package_dir={'fhir': '.'},
    packages=['fhir'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Plugins',
        'Intended Audience :: Developers',
        'Intended Audience :: Healthcare Industry',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Natural Language :: English',
        'Natural Language :: Spanish',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Topic :: Scientific/Engineering :: Medical Science Apps.',
        ],
    keywords='HL7 FHIR GNUHEALTH',
    license='GPL-3',
    requires = ['requests'],
)
