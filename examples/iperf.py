"""
Sample Run of PsAPI Client to collect iperf data
"""

import time
from psapi.client import Client
from psapi.query import Query
from psapi.query import IPerfQuery
from psapi.protocol import EndPointPair
from psapi.protocol import events


################################
# Create new client
################################

# Service access point
url = 'http://pnwg-pt1.es.net:8085/perfSONAR_PS/services/pSB'
c = Client(url)

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
print r['meta']

# read the data
print r['data'].data


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
print r['meta']

# read the data
print r['data'].data


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
print r['data'][0].data
print r['data'][1].data
print r['data'][2].data
print r['data'][3].data

################################################################
#This is example reteriving all endpoints
################################################################

# Any key/value pairs paramters can go here
params = {'protocol':'TCP', 'timeDuration':'20'}

# Only filter_type is mandotary, the rest can be any key/value pairs
select={'filter_type':'select', 'startTime':int(time.time())-100000, 'endTime':int(time.time())}

q = Query(events.IPERF2, params=params, data_filter=select)
r = c.query(q)

for i in range(len(r['meta'])):
    ends = r['meta'][i].subject.contents
    data = r['data'][i]
    # its good to check other ordering first
    if r['meta'][i].object_id == data.ref_id:
        print "---------------------------------"
        print "Endpoint: (%s, %s)" % (ends.src, ends.dst)
        print "Data: %s" % data.data
        print "---------------------------------"
    else:
        print "Not matching references (%s, %s)" % (r['meta'][i].object_id, data.ref_id)
