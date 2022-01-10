#!/usr/bin/env python
#    Copyright (C) 2011-2022 Luis Falcon <falcon@gnuhealth.org>
#    Copyright (C) 2011-2022 GNU Solidario <health@gnusolidario.org>
#    Copyright (C) 2011 Cédric Krier

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

import re
import os
import configparser
from setuptools import setup


long_desc = open('README.rst').read()

config = configparser.ConfigParser()
config.readfp(open('tryton.cfg'))
info = dict(config.items('tryton'))

for key in ('depends', 'extras_depend', 'xml'):
    if key in info:
        info[key] = info[key].strip().splitlines()
major_version, minor_version = 6, 0

requires = ['pytz', 'numpy']

for dep in info.get('depends', []):
    if (dep == 'health_dentistry'):
        requires.append('gnuhealth_dentistry == %s' % (info.get('version')))

    elif dep.startswith('health_dentistry_'):
        health_dentistry_package = dep.split('_', 1)[1]
        requires.append('gnuhealth_dentistry_%s == %s' %
                        (health_dentistry_package, info.get('version')))
    else:
        if not re.match(r'(ir|res|webdav)(\W|$)', dep):
            requires.append('trytond_%s >= %s.%s, < %s.%s' %
                            (dep, major_version, minor_version, major_version,
                             minor_version + 1))

requires.append('trytond >= %s.%s, < %s.%s' %
                (major_version, minor_version, major_version,
                 minor_version + 1))

setup(
    name='gnuhealth_dentistry',
    version=info.get('version', '0.0.1'),
    description=info.get('description',
                         'GNU Health: Dentistry Package'),
    long_description=long_desc,
    author='GNU Solidario',
    author_email='health_dentistry@gnusolidario.org',
    url='https://www.gnuhealth_dentistry.org',
    download_url='http://ftp.gnu.org/gnu/health_dentistry/',
    package_dir={'trytond.modules.health_dentistry': '.'},
    packages=[
        'trytond.modules.health_dentistry',
        'trytond.modules.health_dentistry.tests',
        'trytond.modules.health_dentistry.wizard',
        'trytond.modules.health_dentistry.report',
        ],

    package_data={
        'trytond.modules.health_dentistry': info.get('xml', []) +
        info.get('translation', []) +
        ['tryton.cfg', 'view/*.xml', 'doc/*.rst',
            'locale/*.po', 'report/*.fodt', 'icons/*.svg',
            'report/*.png'],
        },

    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Plugins',
        'Framework :: Tryton',
        'Intended Audience :: Developers',
        'Intended Audience :: Healthcare Industry',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Natural Language :: English',
        'Natural Language :: Spanish',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Topic :: Scientific/Engineering :: Medical Science Apps.',
        ],
    license='GPL-3',
    install_requires=requires,
    extras_require={
        'Pillow': ['Pillow'],
        },
    zip_safe=False,
    entry_points="""
    [trytond.modules]
    health_dentistry = trytond.modules.health_dentistry
    """,
    test_suite='tests',
    test_loader='trytond.test_loader:Loader',
)
