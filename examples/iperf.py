"""
Sample Run of PsAPI Client to collect iperf data
"""

import time
from psapi.client import ServiceClient
from psapi.query import Query
from psapi.query import IPerfQuery
from psapi.protocol import EndPointPair
from psapi.protocol import events


################################
# Create new client
################################

# Service access point
url = 'http://pnwg-pt1.es.net:8085/perfSONAR_PS/services/pSB'
c = ServiceClient(url)

################################
# making a single query
################################

# This purely using python objects and needs min knowldge of the 
# perfSONAR protocol because all params are part of the constructor

endpointpair = EndPointPair(src= '198.124.252.117', dst='198.129.254.46')
query = IPerfQuery(endpointpair=endpointpair, protocol='TCP',
            time_duration=20, \
            start_time=int(time.time())-100000, \
            end_time=int(time.time()))


r = c.query(query)

#read the metadata
print r.meta

# read the data
print r.data


#####################################
# This method allows the user to add any parameter or filter
#####################################
# Any key/value pairs paramters can go here
params = {'protocol':'TCP', 'timeDuration':'20'}

# Only filter_type is mandotary, the rest can be any key/value pairs
select={'filter_type':'select', 'startTime':int(time.time())-100000, 'endTime':int(time.time())}

# everything but event type is optional!
q = Query(events.IPERF2, params=params, src= '198.124.252.117', dst='198.129.254.46', data_filter=select)
r = c.query(q)

#read the metadata
print r.meta

# read the data
print r.data


################################################################
#This is example of sending multiple queries to the same service
################################################################

# Any key/value pairs paramters can go here
params = {'protocol':'TCP', 'timeDuration':'20'}

# Only filter_type is mandotary, the rest can be any key/value pairs
select={'filter_type':'select', 'startTime':int(time.time())-100000, 'endTime':int(time.time())}

q1 = Query(events.IPERF2, params=params, src= '198.129.254.122', dst='198.129.254.46', data_filter=select)
q2 = Query(events.IPERF2, params=params, src= '198.124.252.117', dst='198.129.254.46', data_filter=select)
q3 = Query(events.IPERF2, params=params, src= '198.129.254.46', dst='198.124.252.141', data_filter=select)
q4 = Query(events.IPERF2, params=params, src= '198.129.254.46', dst='198.129.254.134', data_filter=select)

r = c.aggregate_query([q1, q2, q3, q4])

# read the data
for key, value in r.meta.iteritems():
    print "Endpoint:  (src: %s, dst:%s)" % (value.subject.src, value.subject.dst)
    print r.data[key]
    print "\n"

################################################################
#This is example reteriving all endpoints
################################################################

# Any key/value pairs paramters can go here
params = {'protocol':'TCP', 'timeDuration':'20'}

# Only filter_type is mandotary, the rest can be any key/value pairs
select={'filter_type':'select', 'startTime':int(time.time())-100000, 'endTime':int(time.time())}

q = Query(events.IPERF2, params=params, data_filter=select)
r = c.query(q)


# read the data
for key, value in r.meta.iteritems():
    print "Endpoint:  (src: %s, dst:%s)" % (value.subject.src, value.subject.dst)
    print r.data[key]
    print "\n"
