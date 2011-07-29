#!/usr/bin/env python

"""
Query SNMP Data
"""

__authors__ = [
    '"Ahmed El-Hassany" <<ahassany@udel.edu>',
  ]

from psapi.protocol import Data
from psapi.protocol import Interface
from psapi.protocol import Metadata
from psapi.protocol import NetDiscardSubject
from psapi.protocol import NetErrorSubject
from psapi.protocol import NetUtilSubject
from psapi.protocol import Parameters
from psapi.protocol import events
from psapi.query import Query


class SNMPQuery(Query):
    """
    SNMPQuery contains the mostly used SNMP query parameters in the
    constructor.
    If more parameters are needed use the static method make_SNMP_query.
    """
    def __init__(self, interface=None, maKey=None, event=events.NET_UTILIZATION,
                 consolidation_function=None, resolution=None, start_time=None,
                 end_time=None):
        """
        Arguments:
            interface: Object of type Interface
            maKey: metadata key
            event: NET_UTILIZATION, NET_ERROR, NET_DISCARD
            consolidation_function: AVERAGE
            resolution: resolution in seconds
            start_time: unix time format
            end_time: unix time format            
        """
        if not interface and not maKey:
            raise ValueError("interface or maKey must be defined")
        
        Query.__init__(self, events.NET_UTILIZATION)
        self.interface = interface
        self.maKey = maKey
        self.event = event 
        self.consolidation_function = consolidation_function
        self.resolution = resolution
        self.start_time = start_time
        self.end_time = end_time
        
    
    @staticmethod
    def make_snmp_query(**args):
        """Make SNMP MA query."""
        
        #Exctract Argments
        #args_rest = args.copy()
        params = args.pop('params', None)
        data_filter = args.pop('data_filter', None)
        interface = args.pop('interface', None)
        meta_id = args.pop('meta_id', None)
        data_id = args.pop('data_id', None)
        maKey = args.pop('maKey', None)
        event = args.pop('event', events.NET_UTILIZATION)
        
        if interface is None:
            interface = Interface(**args)
        elif not isinstance(interface, Interface):
            raise ValueError("interface must be of \
                        type Interface while object of type '%s' \
                        is found" % type(interface))
            
        if maKey:
            meta = Metadata(maKey=maKey, event_types=event,
                            parameters=params, object_id=meta_id)
        else:
            if event == events.NET_UTILIZATION:
                subject = NetUtilSubject(interface)
            elif event == events.NET_DISCARD:
                subject = NetDiscardSubject(interface)
            elif event == events.NET_ERROR:
                subject = NetErrorSubject(interface)
            else:
                raise ValueError("event must be NET_UTILIZATION, NET_DISCARD, or NET_ERROR")
            
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
            data_filter['protocol'] = self.resolution
        
        if self.start_time is not None:
            data_filter['startTime'] = self.start_time
        
        if self.end_time is not None:
            data_filter['endTime'] = self.end_time
        
        
        if len(data_filter) == 1:
            data_filter = None
        
        query = SNMPQuery.make_snmp_query(params=None,
                                        data_filter=data_filter,
                                        interface=self.interface,
                                        maKey=self.maKey,
                                        event=self.event,
                                        meta_id=self._meta_object_id,
                                        data_id=self._data_object_id)
        return query

