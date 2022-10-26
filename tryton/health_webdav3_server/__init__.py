# SPDX-FileCopyrightText: 2012-2017 Cédric Krier
# SPDX-FileCopyrightText: 2017-2022 GNU Solidario <health@gnusolidario.org>
# SPDX-FileCopyrightText: 2017-2022 Luis Falcon <falcon@gnuhealth.org>
#
# SPDX-License-Identifier: GPL-3.0-or-later

# This file is part of GNU Health.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.
"""WebDAV server for GNU Health

WebDAV server for GNU Health HMIS. It contains the 
functionality for Collections, Shares and Attachments

The package is the continuation of the WebDAV functionality
for the discontinued Tryton package.

It has been ported to Python 3 and GNU Health.


Usage : gnuhealth-webdav-server

"""

from trytond.pool import Pool
from .webdav import *


def register():
    Pool.register(
        Collection,
        Share,
        Attachment,
        module='health_webdav3_server', type_='model')
