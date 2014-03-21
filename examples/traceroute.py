"""
Sample Run of PsAPI Client to collect Traceroute data
"""
import datetime
import calendar
from psapi.client import ServiceClient
from psapi.query import Query
from psapi.query import TracerouteQuery
from psapi.protocol import events
from psapi.protocol import EndPointPair
from psapi.protocol import Message


################################
# Create new client
################################

# Service access point
url = 'http://wash-pt1.es.net:8086/perfSONAR_PS/services/tracerouteMA'
c = ServiceClient(url)

start = calendar.timegm(datetime.datetime(2014, 02, 13, 3, 30, 15).utctimetuple())
end = calendar.timegm(datetime.datetime(2014, 02, 14, 3, 30, 15).utctimetuple())

###############################
# Endpoint query
###############################
select = {
    'filter_type': 'select',
    'startTime': start,
    'endTime': end,
}

q = Query(events.TRACEROUTE, data_filter=select)
#print q.to_xml()
r = c.query(q, message_type=Message.METADATA_KEY_REQUEST)


# read the data
for key, value in r.meta.iteritems():
    if value.subject is None:
        continue
    print "Endpoint:  (src: %s, dst:%s)" % (value.subject.src, value.subject.dst)
    print value.event_types
    #print value.to_xml()
    print r.data[key]
    print "\n"

################################
# making a single query
################################

# This purely using python objects and needs min knowledge of the
# perfSONAR protocol because all params are part of the constructor

# The end point pair should be from the output of the previous
# select query

endpointpair = EndPointPair(src='wash-pt1.es.net', dst='slac-pt1.es.net')
query = TracerouteQuery(
    endpointpair=endpointpair, start_time=start, end_time=end)

r = c.query(query)

# read the data
for key, value in r.meta.iteritems():
    if value.subject is None:
        continue

    print "Endpoint:  (src: %s, dst:%s)" % (value.subject.src, value.subject.dst)
    for trace in r.data[key]:
        print "Trace:"
        for p in trace:
            print p
        print "\n"

