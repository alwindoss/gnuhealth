#!/usr/bin/env python 
# SPDX-FileCopyrightText: 2008-2022 Luis Falcón <falcon@gnuhealth.org>
# SPDX-FileCopyrightText: 2011-2022 GNU Solidario <health@gnusolidario.org>
#
# SPDX-License-Identifier: GPL-3.0-or-later

#########################################################################
#   Hospital Management Information System (HMIS) component of the      #
#                       GNU Health project                              #
#                   https://www.gnuhealth.org                           #
#########################################################################
#                       gh_queue_manager.py                             #
#   Sends the queued messages from the HMIS to the GH Federation        #
#########################################################################

from proteus import config, Model
import sys

dbname = 'health34'
user = 'admin'
password = 'gnusolidario'
hostname = 'localhost'
port = '8000'

health_server = \
    'http://'+user+':'+password+'@'+hostname+':'+port+'/'+dbname+'/'


usage = """
   Usage : gh_queue_manager <action> [args]
    Actions:
        * check: View messages in queue
        * push: Send messages to the federation
    """
def federation_queue(action):
    Queue = Model.get('gnuhealth.federation.queue')

    mqueued = Queue.find ([('state', '=', 'queued')])
    queued_messages = len(mqueued)
    
    print ("Number of messages in the queue", queued_messages)
    if (action == "check"):
        exit (0)

    if (action == "push"):
        print ("Sending messages with status Queued...")
        for msg in mqueued:
            print (msg.msgid, msg.federation_locator, msg.time_stamp, msg.model, msg.node)
            try:
                msg.click('send')
            except:
                print ("Failed to send message ", msg.msgid)



if (len(sys.argv) < 2):
    exit (usage)
    
print ("Connecting to GNU Health Server ...")
conf = config.set_xmlrpc(health_server)
print ("Connected !")

federation_queue(action=sys.argv[1])
