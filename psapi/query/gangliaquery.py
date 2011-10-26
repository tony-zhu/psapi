#!/usr/bin/env python

"""
Query Ganglia Data
"""

__authors__ = [
    '"Ahmed El-Hassany" <<ahassany@udel.edu>',
  ]

from psapi.protocol import Data
from psapi.protocol import GangliaSubject
from psapi.protocol import Interface
from psapi.protocol import Metadata
from psapi.protocol import Node
from psapi.protocol import events
from psapi.query import Query


class GangliaQuery(Query):
    def __init__(self, event, subject=None, maKey=None,
                 consolidation_function=None, resolution=None, start_time=None,
                 end_time=None):

        if not subject and not maKey:
            raise ValueError("subject or maKey must be defined")
        
        Query.__init__(self, events.GANGLIA_NET_UTILIZATION_SENT)
        self.subject = subject
        self.maKey = maKey
        self.event = event 
        self.consolidation_function = consolidation_function
        self.resolution = resolution
        self.start_time = start_time
        self.end_time = end_time
        
    
    @staticmethod
    def make_ganglia_query(**args):
        params = args.pop('params', None)
        data_filter = args.pop('data_filter', None)
        subject = args.pop('subject', None)
        meta_id = args.pop('meta_id', None)
        data_id = args.pop('data_id', None)
        maKey = args.pop('maKey', None)
        event = args.pop('event', None)
        
        if subject is None:
            try:
                interface = Interface(**args)
            except:
                interface = None
            try:
                node = Node(**args)
            except:
                node = None
        
            if interface:
                subject = interface
            elif node:
                subject = node    
            if not isinstance(subject, Node) and  not isinstance(subject, Interface):
                raise ValueError("subject must be of \
                            type Interface or Node while object of type '%s' \
                        is found" % type(interface))
            
        if maKey:
            meta = Metadata(maKey=maKey, event_types=event,
                            parameters=params, object_id=meta_id)
        else:
            subject = GangliaSubject(subject)
            meta = Metadata(subject=subject, event_types=event,
                            parameters=params, object_id=meta_id)
        
        
        if not data_filter:
            data = Data(object_id=data_id, ref_id=meta.object_id)
            query = {'meta': meta, 'data':data}
        else:
            from psapi.query.query_maker import make_filter
            filter_meta = make_filter(data_filter, meta.object_id)
            data = Data(object_id=data_id, ref_id=filter_meta.object_id)
            query = {'meta': [meta, filter_meta], 'data':data}

        return query
    
    def get_psobjects(self):
        data_filter = {'filter_type':'select'}
        
        if self.consolidation_function is not None:
            data_filter['consolidationFunction'] = self.consolidation_function
        
        if self.resolution is not None:
            data_filter['resolution'] = self.resolution
        
        if self.start_time is not None:
            data_filter['startTime'] = self.start_time
        
        if self.end_time is not None:
            data_filter['endTime'] = self.end_time
        
        
        if len(data_filter) == 1:
            data_filter = None
            
        query = GangliaQuery.make_ganglia_query(params=None,
                                        data_filter=data_filter,
                                        subject=self.subject,
                                        maKey=self.maKey,
                                        event=self.event,
                                        meta_id=self._meta_object_id,
                                        data_id=self._data_object_id)
        return query

