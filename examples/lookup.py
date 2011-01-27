"""
Sample Run of PsAPI Client for Lookup Service
"""

from psapi.client import ServiceClient
from psapi.query import LookupQuery
from psapi.protocol import Address
from psapi.protocol import events

################################
# Create new client
################################

# Service access point
url = 'http://ps1.es.net:9990/perfSONAR_PS/services/gLS'
c = ServiceClient(url)

src = Address('198.124.252.117')
dst = Address('198.129.254.46')

gls_query = LookupQuery([src, dst], events.IPERF2)

r = c.query(gls_query)

for result in r.data:
    print result.accessPoint
