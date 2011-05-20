#!/usr/bin/env python

"""
LS Summarization Discovery Query
"""

__authors__ = [
    '"Ahmed El-Hassany" <<ahassany@udel.edu>',
  ]

from psapi.protocol import Data
from psapi.protocol import Message
from psapi.protocol import Metadata
from psapi.protocol import SummarySubject
from psapi.protocol import events
from psapi.query import Query


class LookupQuery(Query):
    
    def __init__(self, objects=None, event_types=None):
        """
        Arguments:
            objects: Objects to query about
            event_types: 
        """
        Query.__init__(self, event_types)
        self.objects = objects
        self.event_types = event_types
        self.default_message_type = Message.LS_QUERY_REQUEST
    
    @staticmethod
    def make_lookup_query(objects, event_types, meta_object_id=None, data_object_id=None):
        """Make LS Summarization query.
        """
        summary_subject = SummarySubject(objects, event_types)
        meta = Metadata(summary_subject, events.SUMMARY, object_id=meta_object_id)        
        data = Data(object_id=data_object_id, ref_id=meta.object_id)
        query = {'meta': meta, 'data':data}
        return query
    
    def get_psobjects(self):
        query = LookupQuery.make_lookup_query(self.objects,
                                              self.event_types,
                                              meta_object_id=self._meta_object_id,
                                              data_object_id=self._data_object_id)
        return query

