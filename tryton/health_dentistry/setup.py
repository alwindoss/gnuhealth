#!/usr/bin/env python

# SPDX-FileCopyrightText: 2008-2022 Luis Falcón <falcon@gnuhealth.org>
# SPDX-FileCopyrightText: 2011-2022 GNU Solidario <health@gnusolidario.org>
# SPDX-FileCopyrightText: 2011 Cédric Krier <cedric.krier@b2ck.com>

# SPDX-License-Identifier: GPL-3.0-or-later

#########################################################################
#   Hospital Management Information System (HMIS) component of the      #
#                       GNU Health project                              #
#                   https://www.gnuhealth.org                           #
#########################################################################
#                   HEALTH DENTISTRY package                            #
#                   setup.py: Setuptools file                           #
#########################################################################

import re
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
    if (dep == 'health'):
        requires.append('gnuhealth == %s' % (info.get('version')))

    elif dep.startswith('health_'):
        health_package = dep.split('_', 1)[1]
        requires.append(
            'gnuhealth_%s == %s' % (health_package, info.get('version')))
    else:
        if not re.match(r'(ir|res|webdav)(\W|$)', dep):
            requires.append(
                'trytond_%s >= %s.%s, < %s.%s' %
                (dep, major_version, minor_version, major_version,
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
