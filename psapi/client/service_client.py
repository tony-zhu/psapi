#!/usr/bin/env python

"""
perfSONAR service client. This client make use of the SOAP client to
talk to perfSONAR services.
"""
from urlparse import urlparse
from psapi.client import SoapClient
from psapi.client import ResultSet
from psapi.protocol import PsService
from psapi.protocol import Message


class ServiceClient(object):
    """perfSONAR service client."""
    def __init__(self, access_point, cert=None, key=None):
        """
        Arguments:
        access_point: full perfSONAR URL
        cert: if provided SSL connection will be used
        key: if provided SSL connection will be used
        """
        if isinstance(access_point, PsService):
            self.access_point = access_point.accessPoint
        else:
            self.access_point = access_point
        self.cert = cert
        self.key = key

        parse = urlparse(access_point)
        self.soap_client = SoapClient(parse.hostname, parse.port, \
                                                parse.path, cert, key)

    def aggregate_query(self, queries, \
                        message_type=Message.SETUP_DATA_REQUEST, \
                        parse_result=True):
        """
        Send multiple queries to the same service to save round trip
        time.

        Arguments:
        queries: list of queries either objects of type Query or
                 XML strings.
        message_type: perfSONAR message types, possible values are
                      defined in Message
        parse_results: If False return raw XML string
        """
        if not isinstance(queries, list):
            raise ValueError("queries should be a list.")

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

        xml = Message(meta, data, message_type=message_type).to_xml()
        result = self.soap_client.send_request(xml, parse=parse_result)

        if parse_result is True:
            return ResultSet.parse_result(result)
        else:
            return result

    def query(self, query, message_type=None, parse_result=True):
        """
        Send One query to perfSONAR service

        Arguments:
        query: either objects of type Query or XML strings
        message_type: perfSONAR message types, possible values are
                      defined in Message
        parse_results: If False return raw XML string
        """
        result = None
        if hasattr(query, 'to_xml'):
            result = self.soap_client.send_request(\
                                query.to_xml(message_type=message_type),
                                parse=parse_result)
        elif isinstance(query, str):
            result = self.soap_client.send_request(query)
        else:
            raise ValueError("Query should be Query instance.")

        if parse_result is True:
            return ResultSet.parse_result(result)
        else:
            return result
