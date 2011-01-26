"""
Sample Run of PsAPI Client to collect Traceroute data
"""
import time
from psapi.client import ServiceClient
from psapi.query import TracerouteQuery
from psapi.protocol import EndPointPair


################################
# Create new client
################################

# Service access point
url = 'http://wash-pt1.es.net:8085/perfSONAR_PS/services/tracerouteMA'
c = ServiceClient(url)

################################
# making a single query
################################

# This purely using python objects and needs min knowldge of the 
# perfSONAR protocol because all params are part of the constructor

endpointpair = EndPointPair(src='198.124.238.34', dst='198.124.252.121')
query = TracerouteQuery(endpointpair=endpointpair, \
                        start_time=int(time.time())-1000, \
                        end_time=int(time.time()))


r = c.query(query)

#read the metadata
print r.meta

# read the data
print r.data
