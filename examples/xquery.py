from psapi.client import ServiceClient
from psapi.query import XQuery

# Service access point
url = 'http://ps1.es.net:9990/perfSONAR_PS/services/gLS'
c = ServiceClient(url)

query_text = """
declare namespace nmwg="http://ggf.org/ns/nmwg/base/2.0/";
declare namespace perfsonar="http://ggf.org/ns/nmwg/tools/org/perfsonar/1.0/";
declare namespace psservice="http://ggf.org/ns/nmwg/tools/org/perfsonar/service/1.0/";
declare namespace summary="http://ggf.org/ns/nmwg/tools/org/perfsonar/service/lookup/summarization/2.0/";

for $metadata in /nmwg:store[@type="LSStore"]/nmwg:metadata
    let $metadata_id := $metadata/@id 
    let $data := /nmwg:store[@type="LSStore"]/nmwg:data[@metadataIdRef=$metadata_id]
    return
        element {"nmwg:metadata"} {
            attribute id {$metadata_id},
            element {"perfsonar:subject"} {    
                $metadata/perfsonar:subject/psservice:service        
            },
            $data/nmwg:metadata/nmwg:eventType
        }
"""

xquery = XQuery(query_text)
r = c.query(xquery)

for metaKey in r.meta:
    for service in r.data[metaKey]:
        print service.subject.accessPoint 
