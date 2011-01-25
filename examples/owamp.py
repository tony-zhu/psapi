"""
Sample Run of PsAPI Client to collect OWAMP data
"""

import time
from psapi.client import ServiceClient
from psapi.query import OWAMPQuery
from psapi.protocol import EndPointPair
from psapi.protocol import events


################################
# Create new client
################################

# Service access point
url = 'http://lhcperfmon.bnl.gov:8085/perfSONAR_PS/services/pSB'
c = ServiceClient(url)

################################
# making a single query
################################

# This purely using python objects and needs min knowldge of the 
# perfSONAR protocol because all params are part of the constructor

endpointpair = EndPointPair(src= '192.12.15.26', dst='131.243.24.11')
query = OWAMPQuery(endpointpair=endpointpair)


r = c.query(query)

#read the metadata
print r.meta

# read the data
print r.data
