#!/usr/bin/env python

"""
Utility methods for making perfSONAR queries.
"""

from psapi.protocol import Data
from psapi.protocol import events
from psapi.protocol import EndPointPair
from psapi.protocol import IPerfSubject
from psapi.protocol import SelectSubject
from psapi.protocol import SelectParameters
from psapi.protocol import Metadata
from psapi.protocol import Parameters


def make_filter(filter_args, meta_id):
    if 'filter_type' not in filter_args:
        raise ValueError("Filter type is not defined.")
    
    filter_meta = None
    filter_type = filter_args['filter_type']
    params = filter_args.copy()
    del params['filter_type']
    
    
    if filter_type == 'select':
        filter_subject = SelectSubject(ref_id=meta_id)
        filter_args = SelectParameters(params)
        filter_meta = Metadata(filter_subject, events.SELECT, filter_args)
    
    return filter_meta

    
def make_iperf_query(**args):
    """Make iperf MA query.
    """
    src = None
    dst = None
    params = None
    
    if 'src' in args:
        src = args['src']
    
    if 'dst' in args:
        dst = args['dst']
    
    if 'params' in args:
        params = args['params']
    
    ends = EndPointPair(src, dst)
    iperf = IPerfSubject(ends)
    if params != None:
        params = Parameters(params)
    meta = Metadata(iperf, events.IPERF2, params)
    
    filter_meta = None
    if 'data_filter' in args:
        filter_meta = make_filter(args['data_filter'], meta.object_id)
    
    if filter_meta is None:
        data = Data(ref_id=meta.object_id)
        query = {'meta': meta, 'data':data, 'message_type':'SetupDataRequest'}
    else:
        data = Data(ref_id=filter_meta.object_id)
        query = {'meta': [meta, filter_meta], 'data':data, \
                                    'message_type':'SetupDataRequest'}

    return query

def make_snmp_query(*args):
    """Make SNMP MA query."""
    # TODO: Implement this
    return None

def make_query(event_type, **args):
    """
    Return results from the appropriate query maker based on the event
    type.
    """
    if event_type == events.IPERF2:
        query = make_iperf_query(**args)
    elif event_type == events.SNMP:
        query = make_snmp_query(**args)
    return query
