"""
An abstract client for communication protocols (currently SOAP and REST)

Author: Ahmed El-Hassany <ahassany@udel.edu>
"""
class CommunicationClient:
    def __init__(self, host, port, path, cert=None, key=None, timeout=None):
        self.host = host
        self.port = port
        self.path  = path
        self.cert = cert
        self.key = key
        self.timeout = timeout
        
    def send_request(self, message, useSSL=False, timeout=None):
        """
        Abstract method for sending messages over the communication protocol.
        
        @param message: the actual message content
        @param useSSL: indicates the secure connection should be used, False by default
        @param timeout: connection timeout period
        """
        pass
