#!/usr/bin/env python

"""
Utility methods for making perfSONAR queries.
"""
__authors__ = [
    '"Ahmed El-Hassany" <<ahassany@udel.edu>',
  ]

from psapi.protocol import events
from psapi.protocol import SelectSubject
from psapi.protocol import SelectParameters
from psapi.protocol import Metadata


def make_filter(filter_args, meta_id):
    """Create a filter subject"""
    if 'filter_type' not in filter_args:
        raise ValueError("Filter type is not defined.")
    
    filter_meta = None
    filter_type = filter_args['filter_type']
    params = filter_args.copy()
    del params['filter_type']
    
    
    if filter_type == 'select':
        filter_subject = SelectSubject(ref_id=meta_id)
        filter_args = SelectParameters(params)
        filter_meta = Metadata(filter_subject,
                               events.SELECT,
                               filter_args,
                               object_id="filter." + meta_id)
    
    return filter_meta

    
def make_iperf_query(**args):
    """Make iperf MA query.
    """
    from psapi.query import IPerfQuery
    query = IPerfQuery.make_iperf_query(**args)
    return query

def make_snmp_query(**args):
    """Make SNMP MA query."""
    from psapi.query import SNMPQuery
    query = SNMPQuery.make_snmp_query(**args)
    return query

def make_owamp_query(**args):
    """Make OWAMP MA query.
    """
    from psapi.query import OWAMPQuery
    query = OWAMPQuery.make_owamp_query(**args)
    return query

def make_traceroute_query(**args):
    """Make Traceroute MA query.
    """
    from psapi.query import TracerouteQuery
    query = TracerouteQuery.make_traceroute_query(**args)
    return query

def make_lookup_query(**args):
    """Make Lookup query.
    """
    from psapi.query import LookupQuery
    query = LookupQuery.make_lookup_query(**args)
    return query

def make_ganglia_query(**args):
    """Make Ganglia MA query."""
    from psapi.query import GangliaQuery
    query = GangliaQuery.make_ganglia_query(**args)
    return query

def make_query(event_type, **args):
    """
    Return results from the appropriate query maker based on the event
    type.
    """
    if event_type == events.IPERF2 or event_type == events.BANDWIDTH:
        query = make_iperf_query(**args)
    elif event_type == events.NET_UTILIZATION:
        query = make_snmp_query(**args)
    elif event_type == events.OWAMP:
        query = make_owamp_query(**args)
    elif event_type == events.TRACEROUTE:
        query = make_traceroute_query(**args)
    elif event_type == events.SUMMARY:
        query = make_lookup_query(**args)
    return query
