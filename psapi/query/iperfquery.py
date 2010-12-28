#!/usr/bin/env python

"""
Query IPerf Data
"""

__authors__ = [
    '"Ahmed El-Hassany" <<ahassany@udel.edu>',
  ]

from psapi.protocol import Data
from psapi.protocol import EndPointPair
from psapi.protocol import IPerfSubject
from psapi.protocol import Metadata
from psapi.protocol import Parameters
from psapi.protocol import events
from psapi.query import Query


class IPerfQuery(Query):
    """
    IPerfQuery contains the mostly used iperf query parameters in the
    constructor.
    If more parameters are needed use the static method make_iperf_query.
    """
    def __init__(self, endpointpair, protocol=None, time_duration=None,
                                        start_time=None, end_time=None):
        """
        Arguments:
            endpointpair: Object of type EndPointPair
            protocol: 'TCP' or 'UDP'
            time_duration:
            start_time: unix time format
            end_time: unix time format
        """
        Query.__init__(self, events.IPERF2)
        self.endpointpair = endpointpair
        self.protocol = protocol
        self.time_duration = time_duration
        self.start_time = start_time
        self.end_time = end_time
    
    @staticmethod
    def make_iperf_query(**args):
        """Make iperf MA query.
        """
        src = None
        dst = None
        params = None
        ends = None
        
        if 'src' in args:
            src = args['src']
        
        if 'dst' in args:
            dst = args['dst']
        
        if 'endpointpair' in args:
            ends = args['endpointpair']
            if not isinstance(ends, EndPointPair):
                raise ValueError("endpointpair must be of \
                            type EndPointPair while object of type '%s' \
                            is found" % type(ends))
       
        if ends is None:
            ends = EndPointPair(src, dst)
                
        if 'params' in args:
            params = args['params']
        
        
        iperf = IPerfSubject(ends)
        if params != None:
            params = Parameters(params)
        meta = Metadata(iperf, events.IPERF2, params)
        
        filter_meta = None
        if 'data_filter' in args:
            from psapi.query.query_maker import make_filter
            filter_meta = make_filter(args['data_filter'], meta.object_id)
        
        if filter_meta is None:
            data = Data(ref_id=meta.object_id)
            query = {'meta': meta, 'data':data}
        else:
            data = Data(ref_id=filter_meta.object_id)
            query = {'meta': [meta, filter_meta], 'data':data}

        return query
    
    def get_psobjects(self):
        params = {}
        data_filter = {'filter_type':'select'}
        
        # Params
        if self.protocol is not None:
            params['protocol'] = self.protocol
        
        if self.time_duration is not None:
            params['protocol'] = self.time_duration
        
        # Time select filter
        if self.start_time is not None:
            data_filter['startTime'] = self.start_time
        
        if self.end_time is not None:
            data_filter['endTime'] = self.end_time
        
        
        if len(data_filter) == 1:
            data_filter = None
        if len(params) == 0:
            params = None
        
        query = IPerfQuery.make_iperf_query(params=params,
                                        data_filter=data_filter,
                                        endpointpair=self.endpointpair)
        return query

