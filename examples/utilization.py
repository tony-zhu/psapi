#!/usr/bin/env python

"""
Sample Run of PsAPI Client to collect SNMP data
"""

import time
from psapi.client import Client
from psapi.query import Query
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

# Only filter_type is mandotary, the rest can be any key/value pairs
select={'filter_type':'select', 'consolidationFunction': 'AVERAGE', \
        'resolution': 60, 'startTime':int(time.time())-100000, \
        'endTime':int(time.time())}
      
# everything but event type is optional!
q = Query(events.NETUTIL, ifAddress='198.124.216.213', \
        hostName='aofa-cr2', ifName='xe-1/3/0.2611', direction='in', data_filter=select)
r = c.query(q)

#read the metadata
print r['meta']

# read the data
print r['data'].data




