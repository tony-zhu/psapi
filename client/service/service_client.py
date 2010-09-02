"""
An abstract client for service protocols, e.g. LS, OWMP, BWCTL

Author: Ahmed El-Hassany <ahassany@udel.edu>
"""

from urlparse import urlparse

class ServiceClient:

    def __init__(self, url, timeout=None):
        """
        @param url: the full service url, e.g. "http://host.edu:port/path"
        @parm timeout: optional timeout period
        """
        self.url = url
        p = urlparse(url)
        self.host = p.hostname
        self.port = p.port
        self.path = p.path
        self.timeout = timeout
    
    
    def send_query(self, query, timeout=None):
        """
        Send query of Query object type.
        """
        pass
