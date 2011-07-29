#!/usr/bin/env python

"""
Query OWAMP Data
"""

__authors__ = [
    '"Ahmed El-Hassany" <<ahassany@udel.edu>',
  ]

from psapi.protocol import Data
from psapi.protocol import EndPointPair
from psapi.protocol import Metadata
from psapi.protocol import Parameters
from psapi.protocol import OWAMPSubject
from psapi.protocol import events
from psapi.query import Query


class OWAMPQuery(Query):
    """
    OWAMPQuery contains the mostly used OWAMP query parameters in the
    constructor.
    If more parameters are needed use the static method make_owamp_query.
    """
    def __init__(self, endpointpair=None, maKey=None, start_time=None, end_time=None):
        """
        Arguments:
            endpointpair: Object of type EndPointPair
            start_time: unix time format
            end_time: unix time format
            maKey: metadata key
        """
        if not endpointpair and not maKey:
            raise ValueError("endpointpair or maKey must be defined")
        
        Query.__init__(self, events.OWAMP)
        self.endpointpair = endpointpair
        self.start_time = start_time
        self.end_time = end_time
        self.maKey = maKey
    
    @staticmethod
    def make_owamp_query(**args):
        """Make owamp MA query."""
        
        # Extract Arguments
        src = args.get('src', None)
        dst = args.get('dst', None)
        params = args.get('params', None)
        ends = args.get('endpointpair', None)
        data_filter = args.get('data_filter', None)
        meta_id = args.get('meta_id', None)
        data_id = args.get('data_id', None)
        maKey = args.get('maKey', None)
        
        if ends is None:
            ends = EndPointPair(src, dst)
        elif not isinstance(ends, EndPointPair):
            raise ValueError("endpointpair must be of \
                            type EndPointPair while object of type '%s' \
                            is found" % type(ends))
        
        if params:
            params = Parameters(params)
        
        if maKey:
            meta = Metadata(maKey=maKey, event_types=events.OWAMP,
                            parameters=params, object_id=meta_id)
        else: 
            owamp = OWAMPSubject(ends)
            meta = Metadata(subject=owamp, event_types=events.OWAMP,
                    parameters=params, object_id=meta_id)
         
        
        if data_filter is None:
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

        # Time select filter
        if self.start_time is not None:
            data_filter['startTime'] = self.start_time

        if self.end_time is not None:
            data_filter['endTime'] = self.end_time

        if len(data_filter) == 1:
            data_filter = None

        query = OWAMPQuery.make_owamp_query(data_filter=data_filter,
                                        endpointpair=self.endpointpair,
                                        maKey=self.maKey,
                                        meta_id=self._meta_object_id,
                                        data_id=self._data_object_id)
        return query
