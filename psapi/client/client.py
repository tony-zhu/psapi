#!/usr/bin/env python

from urlparse import urlparse
from psapi.client import SoapClient
from psapi.protocol import Message
from psapi.protocol.xmlmapper import parse_psobject_from_xml

class Client(object):
    def __init__(self, access_point, cert=None, key=None):
        self.access_point = access_point
        self.cert = cert
        self.key = key
        
        parse = urlparse(access_point)
        self.soap_client = SoapClient(parse.hostname, parse.port, \
                                                parse.path, cert, key)
    
    def __parse_result(self, result):
        """Parse results into a dict of meta and data."""
        parse = parse_psobject_from_xml(result)
        return {'meta':parse.meta, 'data':parse.data}
    
    def aggregate_query(self, queries):
        if not isinstance(queries, list):
            raise ValueError("queries should be a list.")
        
        message_type = None
        meta = []
        data = []
        for query in queries:
            objs = query.get_psobjects()
            
            if isinstance(objs['meta'], list):
                meta = meta + objs['meta']
            else:
                meta.append(objs['meta'])
            
            if isinstance(objs['data'], list):
                data = data + objs['data']
            else:
                data.append(objs['data'])
                
            if message_type is None:
                message_type = objs['message_type']
            elif message_type != objs['message_type']:
                raise ValueError("All queries should be from the same type.")
        
        xml = Message(meta, data, message_type).to_xml()
        result = self.soap_client.send_request(xml)
        return self.__parse_result(result)
    
    
    def query(self, query):
        result = None
        if hasattr(query, 'to_xml'):
            result = self.soap_client.send_request(query.to_xml())
        elif isinstance(query, str):
            result = self.soap_client.send_request(query)
        else:
            raise ValueError("Query should be Query instance.")
        
        return self.__parse_result(result)
        
        
