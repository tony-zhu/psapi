#!/usr/bin/env python

"""
To make customized LS XQueries.
"""

__authors__ = [
    '"Ahmed El-Hassany" <<ahassany@udel.edu>',
  ]

from psapi.protocol import Data
from psapi.protocol import Message
from psapi.protocol import Metadata
from psapi.protocol import XQueryParameters
from psapi.protocol import XQuerySubject
from psapi.protocol import events
from psapi.query import Query


class XQuery(Query):
    """Query for plain XQueries to perfSONAR services"""
    
    def __init__(self, query=None):
        """
        Arguments:
            query: string XQuery
        """
        Query.__init__(self, events.XQUERY)
        self.query = query
        self.default_message_type = Message.LS_QUERY_REQUEST
    
    @staticmethod
    def make_xquery(query, meta_object_id=None, data_object_id=None):
        """Make LS XQuery.
        """
        xsubject = XQuerySubject(query)
        xparams = XQueryParameters({'lsOutput':'native'})
        meta = Metadata(xsubject,
                        events.XQUERY, xparams,
                        object_id=meta_object_id)        
        data = Data(object_id=data_object_id, ref_id=meta.object_id)
        query = {'meta': meta, 'data':data}
        return query
    
    def get_psobjects(self):
        query = XQuery.make_xquery(self.query,
                                   meta_object_id=self._meta_object_id,
                                   data_object_id=self._data_object_id)
        return query

