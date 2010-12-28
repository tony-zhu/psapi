#!/usr/bin/env python

"""
Query SNMP Data
"""

__authors__ = [
    '"Ahmed El-Hassany" <<ahassany@udel.edu>',
  ]

from psapi.protocol import Data
from psapi.protocol import Interface
from psapi.protocol import NetUtilSubject
from psapi.protocol import Metadata
from psapi.protocol import Parameters
from psapi.protocol import events
from psapi.query import Query


class SNMPQuery(Query):
    """
    SNMPQuery contains the mostly used SNMP query parameters in the
    constructor.
    If more parameters are needed use the static method make_SNMP_query.
    """
    def __init__(self, interface, consolidation_function=None, \
                    resolution=None, start_time=None, end_time=None):
        """
        Arguments:
            interface: Object of type Interface
            consolidation_function: AVERAGE
            resolution: resolution in seconds
            start_time: unix time format
            end_time: unix time format
        """
        Query.__init__(self, events.NETUTIL)
        self.interface = interface
        self.consolidation_function = consolidation_function
        self.resolution = resolution
        self.start_time = start_time
        self.end_time = end_time
    
    @staticmethod
    def make_snmp_query(**args):
        """Make SNMP MA query."""
        params = None
        data_filter = None
        filter_meta = None
        args_rest = args.copy()
        
        if 'params' in args:
            params = args['params']
            del args_rest['params']
        
        if 'data_filter' in args:
            data_filter = args['data_filter']
            
            del args_rest['data_filter']
        
        if 'interface' in args_rest:
            interface = args_rest['interface']
            if not isinstance(interface, Interface):
                raise ValueError("interface must be of \
                            type Interface while object of type '%s' \
                            is found" % type(interface))
        else:
            interface = Interface(**args_rest)
        
        subject = NetUtilSubject(interface)
        
        if params is not None:
            params = Parameters(params)
        meta = Metadata(subject, events.NETUTIL, params)
        
        if data_filter is not None:
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
        data_filter = {'filter_type':'select'}
        
        if self.consolidation_function is not None:
            data_filter['consolidationFunction'] = self.consolidation_function
        
        if self.resolution is not None:
            data_filter['protocol'] = self.resolution
        
        if self.start_time is not None:
            data_filter['startTime'] = self.start_time
        
        if self.end_time is not None:
            data_filter['endTime'] = self.end_time
        
        
        if len(data_filter) == 1:
            data_filter = None
        
        query = SNMPQuery.make_snmp_query(params=None,
                                        data_filter=data_filter,
                                        interface=self.interface)
        return query

