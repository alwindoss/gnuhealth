#!/usr/bin/env python
# SPDX-FileCopyrightText: 2017-2022 Luis Falcón <falcon@gnuhealth.org>
# SPDX-FileCopyrightText: 2017-2022 GNU Solidario <health@gnusolidario.org>
# SPDX-FileCopyrightText: 2012-2017 Cédric Krier <cedric.krier@b2ck.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

#########################################################################
#   Hospital Management Information System (HMIS) component of the      #
#                       GNU Health project                              #
#                   https://www.gnuhealth.org                           #
#########################################################################
#                        HEALTH WEBDAV3 SERVER                          #
#                      setup.py: Setuptools file                        #
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

requires = ['PyWebDAV3-GNUHealth >= 0.10.1']

for dep in info.get('depends', []):
    if (dep == 'health'):
        requires.append('gnuhealth == %s' % (info.get('version')))

    elif dep.startswith('health_'):
        health_package = dep.split('_', 1)[1]
        requires.append('gnuhealth_%s == %s' %
                        (health_package, info.get('version')))
    else:
        if not re.match(r'(ir|res)(\W|$)', dep):
            requires.append('trytond_%s >= %s.%s, < %s.%s' %
                            (dep, major_version, minor_version, major_version,
                             minor_version + 1))

setup(name='gnuhealth_webdav3_server',
      version=info.get('version', '0.0.1'),
      description='GNU Health WebDAV server for Python 3',
      long_description=read('README.rst'),
      author='GNU Solidario',
      author_email='health@gnusolidario.org',
      url='https://www.gnuhealth.org',
      download_url='https://ftp.gnu.org/gnu/health/',
      keywords='webdav GNUHealth',
      package_dir={'trytond.modules.health_webdav3_server': '.'},
      packages=[
        'trytond.modules.health_webdav3_server',
        'trytond.modules.health_webdav3_server.tests',
        ],
      package_data={
        'trytond.modules.health_webdav3_server': (info.get('xml', [])
                                                  + ['tryton.cfg',
                                                     'view/*.xml',
                                                     'locale/*.po',
                                                     '*.fodt',
                                                     'icons/*.svg',
                                                     'tests/*.rst']),
        },

      scripts=['bin/gnuhealth-webdav-server'],
      classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Plugins',
        'Framework :: Tryton',
        'Intended Audience :: Developers',
        'Intended Audience :: Financial and Insurance Industry',
        'Intended Audience :: Legal Industry',
        'Intended Audience :: Manufacturing',
        'License :: OSI Approved :: GNU General Public License (GPL)',
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
        health_webdav3_server = trytond.modules.health_webdav3_server
      """,
      test_suite='tests',
      test_loader='trytond.test_loader:Loader',
      )
