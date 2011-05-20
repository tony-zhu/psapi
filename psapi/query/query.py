#!/usr/bin/env python

"""
Generic perfSONAR query class this class can be extended to support more
specific query types.
"""

__authors__ = [
    '"Ahmed El-Hassany" <<ahassany@udel.edu>',
  ]

from psapi.protocol import Message
from psapi.protocol import PsObject
from psapi.query.query_maker import make_query


class Query(object):
    """
    Query object can hold any query to perfSONAR.
    """
    def __init__(self, event_type, **args):
        """
        query_type: query types are defined in psapi.query.types(SNMP, IPERF, etc)
        args: can be any dict of arguments based on the query type
        """
        self.event_type = event_type
        self.args = args
        self.default_message_type = Message.SETUP_DATA_REQUEST
        
        # To make sure that each query object gets the same meta and data ids
        self._meta_object_id = PsObject.generate_id()
        self._data_object_id = PsObject.generate_id()
    
    def get_psobjects(self):
        """Get a dict of meta, data"""
        return make_query(self.event_type, **self.args)
    
    def get_message(self, message_type=None):
        """create perfSONAR message"""
        query = self.get_psobjects()
        if message_type is None:
            message_type = self.default_message_type
        return Message(message_type=message_type, **query)
    
    def to_xml(self, message_type=Message.SETUP_DATA_REQUEST):
        """Serialize the query to XML to be sent to perfSONAR."""
        return self.get_message(message_type=message_type).to_xml()
