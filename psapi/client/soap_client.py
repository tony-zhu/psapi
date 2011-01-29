"""
SOAP service client.
"""

from httplib import HTTPConnection
from httplib import HTTPSConnection
from lxml import etree


class SoapClient:
    """Very simple client to send SOAP requests to perfSONAR service."""
    def __init__(self, host, port, uri, cert=None, key=None):
        self.host = host
        self.port = port
        self.uri = uri
        self.cert = cert
        self.key = key

    @staticmethod
    def soapify_message(message):
        """Adds a SOAP protocol headers to the message."""

        header_string = """<SOAP-ENV:Envelope
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
        return header_string

    def send_request(self, message, use_ssl=False, issoap=False, parse=False):
        """Send the message to the SOAP server.

        Arguments:
        message: message string
        use_ssl: if set secure HTTPS connection will be used
        issoap: if not set the client will add a SOAP header to the
                message.
        parse: if true an object of etree Element with be returned
        """

        if use_ssl:
            conn = HTTPSConnection(self.host, self.port, self.key, self.cert)
        else:
            conn = HTTPConnection(self.host, self.port)

        conn.connect()
        headers = {'SOAPAction': '', 'Content-Type': 'text/xml'}
        if issoap == False:
            message = SoapClient.soapify_message(message)
        conn.request('POST', self.uri, message, headers)
        resp = conn.getresponse()
        response = resp.read()
        conn.close()
        
        tree = etree.fromstring(response)

        message = tree.xpath('soap:Body/nmwg:message', \
                         namespaces={'soap': \
                                     'http://schemas.xmlsoap.org/soap/envelope/', \
                                 'nmwg': 'http://ggf.org/ns/nmwg/base/2.0/'})
        if parse is True:
            return message[0]
        else:
            return etree.tostring(message[0], pretty_print=True)
