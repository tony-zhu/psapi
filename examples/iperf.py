"""
Sample Run of PsAPI Client to collect iperf data
"""
import calendar

import time
import datetime
from psapi.client import ServiceClient
from psapi.query import Query
from psapi.query import IPerfQuery
from psapi.protocol import EndPointPair
from psapi.protocol import events


################################
# Create new client
################################

# Service access point
url = 'http://bandwidth.cs.utah.edu:8085/perfSONAR_PS/services/pSB'
c = ServiceClient(url)

################################
# making a single query
################################

# This purely using python objects and needs min knowldge of the 
# perfSONAR protocol because all params are part of the constructor

# To query for specific (src, dst) pair
endpointpair = EndPointPair(src='bandwidth.cs.utah.edu', dst='bandwidth.chpc.utah.edu')

# To query for everything
#endpointpair = EndPointPair()

query = IPerfQuery(endpointpair=endpointpair, protocol='TCP',
                  start_time=calendar.timegm(
                        datetime.datetime(2013,11,14,3,30,15).utctimetuple()),
                  end_time=calendar.timegm(
                       datetime.datetime(2013,12,15,15,30,50).utctimetuple()))

r = c.query(query)

#read the metadata
if isinstance(r.meta, dict):
    for metaKey in r.meta:
        meta = r.meta[metaKey]
        data = r.data[metaKey]
        print ""
        print "IPERF data for: src=%s dst=%s" % (meta.subject.src, meta.subject.dst)
        if isinstance(data, list):
            for datum in data:
                print datum
        else:
            print data

        

#####################################
# This method allows the user to add any parameter or filter
#####################################
# Any key/value pairs paramters can go here
params = {'protocol':'TCP', 'timeDuration':'20'}

# Only filter_type is mandotary, the rest can be any key/value pairs
select={'filter_type':'select', 'startTime':int(time.time())-100000, 'endTime':int(time.time())}

# everything but event type is optional!
q = Query(events.IPERF2, params=params, src='pnwg-pt1.es.net', dst='ga-pt1.es.net', data_filter=select)
r = c.query(q)

#read the metadata
if isinstance(r.meta, list):
    for meta in r.meta:
        print meta
else:
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

q1 = Query(events.IPERF2, params=params, src= 'pnwg-pt1.es.net', dst='ga-pt1.es.net', data_filter=select)
q2 = Query(events.IPERF2, params=params, src= 'pnwg-pt1.es.net', dst='llnl-pt1.es.net', data_filter=select)
q3 = Query(events.IPERF2, params=params, src= 'pnwg-pt1.es.net', dst='nersc-pt1.es.net', data_filter=select)
q4 = Query(events.IPERF2, params=params, src= 'pnwg-pt1.es.net', dst='chic-pt1.es.net', data_filter=select)

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
