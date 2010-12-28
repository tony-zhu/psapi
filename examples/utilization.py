#!/usr/bin/env python

"""
Sample Run of PsAPI Client to collect SNMP data
"""

import time
from psapi.client import Client
from psapi.query import Query
from psapi.query import SNMPQuery
from psapi.protocol import events
from psapi.protocol import NetUtilSubject
from psapi.protocol import Interface


################################
# Create new client
################################

# Service access point
url = 'http://ps3.es.net:8080/perfSONAR_PS/services/snmpMA'
c = Client(url)

################################
# making a single query
################################

interface = Interface(ifAddress='198.124.216.213', direction='in', \
                            ifName='xe-1/3/0.2611', hostName='aofa-cr2')

query = SNMPQuery(interface=interface, resolution=60, \
                    consolidation_function='AVERAGE', \
                    start_time=int(time.time())-1000, \
                    end_time=int(time.time()))

r = c.query(query)

#read the metadata
print r['meta']

# read the data
print r['data'].data

################################
################################
# Only filter_type is mandotary, the rest can be any key/value pairs
select={'filter_type':'select', 'consolidationFunction': 'AVERAGE', \
        'resolution': 60, 'startTime':int(time.time())-10000, \
        'endTime':int(time.time())}
      
# everything but event type is optional!
q = Query(events.NETUTIL, ifAddress='198.124.216.213', \
        hostName='aofa-cr2', ifName='xe-1/3/0.2611', direction='in', data_filter=select)
r = c.query(q)

#read the metadata
print r['meta']

# read the data
print r['data'].data




