# SPDX-FileCopyrightText: 2008-2022 Luis Falcón <falcon@gnuhealth.org>
# SPDX-FileCopyrightText: 2011-2022 GNU Solidario <health@gnusolidario.org>
#
# SPDX-License-Identifier: GPL-3.0-or-later
#########################################################################
#   Hospital Management Information System (HMIS) component of the      #
#                       GNU Health project                              #
#                   https://www.gnuhealth.org                           #
#########################################################################
#                     HEALTH FEDERATION package                         #
#                __init__.py: Package declaration file                  #
#########################################################################
"""
health_federation package: HMIS Federation manager

This package is responsible to communicate the GNU Health HMIS
with Thalamus, the Federation message server.

The main functionalities of the package are :
    * HMIS configuration to connect to Thalamus message server
    * Define the models that will participate on the Federation
    * Define which fields of each model will be shared on the Federation
    * Queue manager: Manages the local node queue to be sent to the Federation.
    * Defines the classes for each model and specific methods to interact
      with Thalamus
"""

from trytond.pool import Pool
from . import health_federation


def register():
    Pool.register(
        health_federation.FederationNodeConfig,
        health_federation.FederationQueue,
        health_federation.FederationObject,
        health_federation.PartyFed,
        health_federation.PoLFed,
        module='health_federation', type_='model')
