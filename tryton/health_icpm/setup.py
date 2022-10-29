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
#                      HEALTH ICPM package                              #
#                   setup.py: Setuptools file                           #
#########################################################################

from setuptools import setup
import re
import os
import configparser


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname),
                encoding="UTF-8").read()


config = configparser.ConfigParser()
config.readfp(open('tryton.cfg'))
info = dict(config.items('tryton'))

for key in ('depends', 'extras_depend', 'xml'):
    if key in info:
        info[key] = info[key].strip().splitlines()
major_version, minor_version = 6, 0

requires = []

for dep in info.get('depends', []):
    if (dep == 'health'):
        requires.append('gnuhealth == %s' % (info.get('version')))

    elif dep.startswith('health_'):
        health_package = dep.split('_', 1)[1]
        requires.append(
            'gnuhealth_%s == %s' %
            (health_package, info.get('version')))
    else:
        if not re.match(r'(ir|res|webdav)(\W|$)', dep):
            requires.append(
                'trytond_%s >= %s.%s, < %s.%s' %
                (dep, major_version, minor_version, major_version,
                    minor_version + 1))

setup(
    name='gnuhealth_icpm',
    version=info.get('version', '0.0.1'),
    description=info.get(
        'description',
        'GNU Health WHO ICPM package.'
        ' International Classsification of Procedures in Medicine'),
    long_description=read('README'),
    author='GNU Solidario',
    author_email='health@gnusolidario.org',
    url='https://www.gnuhealth.org',
    download_url='http://ftp.gnu.org/gnu/health/',
    package_dir={'trytond.modules.health_icpm': '.'},
    packages=[
        'trytond.modules.health_icpm',
        'trytond.modules.health_icpm.tests',
        ],

    package_data={
        'trytond.modules.health_icpm': info.get('xml', [])
        + info.get('translation', [])
        + ['tryton.cfg', 'view/*.xml', 'doc/*.rst', 'locale/*.po',
           'report/*.fodt', 'icons/*.svg'],
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
    zip_safe=False,
    entry_points="""
    [trytond.modules]
    health_icpm = trytond.modules.health_icpm
    """,
    test_suite='tests',
    test_loader='trytond.test_loader:Loader',
    )
