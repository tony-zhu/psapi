"""
An abstract client for communication protocols (currently SOAP and REST)

Author: Ahmed El-Hassany <ahassany@udel.edu>
"""

from httplib import HTTPConnection, HTTPSConnection
import re

from psapi.client import CommunicationClient

class SOAPClient(CommunicationClient):
    """
    Very simple client to send SOAP requests to perfSONAR service
    """

    def __init__(self, host, port, endpoint, cert=None, key=None, timeout=None):
        CommunicationClient.__init__(self, host, port, endpoint, cert, key, timeout)
    
    def _add_soap_header(self, message):
        """
        Encapsulate the message in a proper SOAP header.
        """
        headerString = """<SOAP-ENV:Envelope 
            xmlns:SOAP-ENC="http://schemas.xmlsoap.org/soap/encoding/"
            xmlns:xsd="http://www.w3.org/2001/XMLSchema"
            xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
            xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/">
            <SOAP-ENV:Header/>
            <SOAP-ENV:Body>
            %s
            </SOAP-ENV:Body>
            </SOAP-ENV:Envelope>
            """ % message
        return headerString
        
    def _remove_soap_header(self, message):
        """
        Removes the extra soap headers and just leave the nmwg message
        """
        m = re.search('<nmwg:message(.|\n)+</nmwg:message>', message)
        return m.group(0)

    def send_request(self, message, useSSL=False, timeout=None):
        """
        Send and receive a row XML message to the SOAP server.
        """
        if not timeout:
            timeout = self.timeout
            
        if useSSL:
            if timeout:
                conn = HTTPSConnection(self.host, self.port, self.key, \
                        self.cert, timeout=timeout)
            else:
                conn = HTTPSConnection(self.host, self.port, self.key, self.cert)
        else:
            if timeout:
                conn = HTTPConnection(self.host, self.port, timeout=timeout)
            else:
                conn = HTTPConnection(self.host, self.port)
            
        conn.connect()
        headers = {'SOAPAction':'', 'Content-Type': 'text/xml'}
        message = self._add_soap_header(message)
        conn.request('POST', self.path, message, headers)
        resp = conn.getresponse()
        response = resp.read()
        conn.close() 
        return self._remove_soap_header(response)

