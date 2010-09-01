"""
Client for gLS service.

Author: Ahmed El-Hassany <ahassany@udel.edu>
"""

from psapi.client import ServiceClient

class GLSClient(ServiceClient):
    """This client handles quering gLSes for summerization information."""
    def __init__(self, url, timeout=None):
        ServiceClient.__init__(url, timeout)
    
    
    def _parse_results(self, xml):
        pass
    
                        
    def send_xml_query(self, message, timeout=0, issoap=False):
        """Send row XML query to the gLS server.
        
        keyword arguments:
        message -- an XML query message
        timeout -- time before terminating the connection if no response
        issoap  -- if the message has already a SOAP header
        """
        client = PsClient(self.host, self.port, self.endpoint)
        resp = client.send_request(message=xml, issoap=issoap)
        
        return self._parse_results(resp)
        
    def send_query(self, query, timeout=0):
        """Sends an object of type PsQyery."""
        if isinstance(query, PsQuery):
            return self.send_xml_query(query.to_xml(), timeout)
        else:
            # an exception should be thoughn
            pass
