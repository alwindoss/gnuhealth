# SPDX-FileCopyrightText: 2001-2022 Luis Falcón <falcon@gnuhealth.org>
# SPDX-FileCopyrightText: 2011-2022 GNU Solidario <health@gnusolidario.org>
# SPDX-FileCopyrightText: 2011 Cédric Krier <cedric.krier@b2ck.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

#########################################################################
#   Hospital Management Information System (HMIS) component of the      #
#                       GNU Health project                              #
#                   https://www.gnuhealth.org                           #
#########################################################################
#                           HEALTH package                              #
#                       setup.py: Setuptools file                       #
#########################################################################
#!/usr/bin/env python

from setuptools import setup
import re
import os
import configparser


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


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
        requires.append('gnuhealth_%s == %s' %
                        (health_package, info.get('version')))
    else:
        if not re.match(r'(ir|res|webdav)(\W|$)', dep):
            requires.append('trytond_%s >= %s.%s, < %s.%s' %
                            (dep, major_version, minor_version, major_version,
                             minor_version + 1))

requires.append('trytond >= %s.%s, < %s.%s' %
                (major_version, minor_version, major_version,
                 minor_version + 1))

setup(
    name='gnuhealth',
    version=info.get('version', '0.0.1'),
    description=info.get('description', 'GNU Health HMIS: Hospital and Health'
                         ' Information System'),
    long_description=read('README.rst'),
    author='GNU Solidario',
    author_email='health@gnusolidario.org',
    url='https://www.gnuhealth.org',
    download_url='http://ftp.gnu.org/gnu/health/',
    package_dir={'trytond.modules.health': '.'},
    packages=[
        'trytond.modules.health',
        'trytond.modules.health.tests',
        'trytond.modules.health.wizard',
        'trytond.modules.health.report',
        ],

    package_data={
        'trytond.modules.health': info.get('xml', []) +
        info.get('translation', []) +
        ['tryton.cfg', 'view/*.xml', 'doc/*.rst',
            'locale/*.po', 'report/*.fodt', 'icons/*.svg'],
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
    health = trytond.modules.health
    """,
    test_suite='tests',
    test_loader='trytond.test_loader:Loader',
)
