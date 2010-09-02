"""
Client for gLS service.

Author: Ahmed El-Hassany <ahassany@udel.edu>
"""
from xml.etree import ElementTree
import re

from psapi.client.service import ServiceClient
from psapi.client.service import namespaces as ns

class GLSClient(ServiceClient):
    """This client handles querying gLSes for summarization information."""
    
    def __init__(self, url, timeout=None):
        ServiceClient.__init__(self, url, timeout)
    
    
    def _parse_results(self, xml):
        """Parse xml result into a python list of dictionaries.
        
        This client only cares about the addresses of perfSONAR services to get
        data from. It doesn't parse any other information given by gLS.
        """
        tree = ElementTree.fromstring(xml)
        meta = tree.find('{NMWG}metadata'.format(NMWG='{'+ns.NMWG+'}'))
        eventtype = meta.find('{NMWG}eventType'.format(NMWG='{'+ns.NMWG+'}'))
        
        if eventtype.text == 'error.ls.query.empty_results':
            # this not really an error, nothing to return
            return None
        elif eventtype.text.startswith == 'error.':
            # TODO: raise an exception with error message
            data = tree.find('{NMWG}data'.format(NMWG='{'+ns.NMWG+'}'))
            datum = data.find('{NMWGR}datum'.format(NMWGR='{'+ns.NMWGR+'}'))
            # datum.text
            return datum.text
        elif eventtype.text == 'success.ls.query':
            # everything is ok go on
            services = tree.findall('*//{PS}service'.format(PS='{'+ns.PSSERVICE+'}'))
            result = []
            for s in services:
                service = {}
                for c in s.getchildren():
                    tag = re.match('{(.+)}(.+)', c.tag).group(2)
                    text = c.text
                    service[tag] = text
                result.append(service)
            return result
        else:
            # TODO: raise an exception
            return None

    
                        
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
            # TODO: an exception should be throughn 
            pass
