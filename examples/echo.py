from psapi.client import ServiceClient
from psapi.query import EchoRequest


################################
# Create new client
################################

# Service access point
url = 'http://pnwg-pt1.es.net:8085/perfSONAR_PS/services/pSB'
c = ServiceClient(url)


q = EchoRequest()
r = c.query(q)

print r.meta
print r.data
