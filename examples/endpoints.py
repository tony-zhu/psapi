"""
Sample Run of PsAPI Client for getting all the endpoints of the MA
"""

import datetime
import calendar
from psapi.client import ServiceClient
from psapi.query import Query
from psapi.protocol import Message
from psapi.protocol import events


################################
# Create new client
################################

# Service access point
url = 'http://fnal-pt1.es.net:8085/perfSONAR_PS/services/pSB'
c = ServiceClient(url)


################################################################
#This is example reteriving all endpoints
################################################################


# Only filter_type is mandotary, the rest can be any key/value pairs
select={
    'filter_type':'select',
    'startTime': calendar.timegm(
                datetime.datetime(2013,11,14,3,30,15).utctimetuple()),
    'endTime': calendar.timegm(
                datetime.datetime(2013,12,15,15,30,50).utctimetuple())
}

q = Query(events.IPERF2, data_filter=select)
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
