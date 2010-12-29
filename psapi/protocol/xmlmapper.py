#!/usr/bin/env python

"""
XML mapping functions
"""

__authors__ = [
    '"Ahmed El-Hassany" <<ahassany@udel.edu>',
  ]

import re
from lxml import etree
        
def parse_psobject_from_xml(xml):
    """
    Read XML and return the appropriate object
    """
    from psapi.protocol import namespaces as ns
    if isinstance(xml, str):
        tree = etree.fromstring(xml)
    else:
        tree = xml
        
    if tree.tag == '{%s}endPointPair' % ns.NMWGT:
        from psapi.protocol.endpointpair import EndPointPair
        return EndPointPair.from_xml(tree)
    
    if tree.tag == '{%s}parameters' % ns.NMWG:
        from psapi.protocol.parameters import Parameters
        return Parameters.from_xml(tree)
    
    if tree.tag == '{%s}parameters' % ns.SELECT:
        from psapi.protocol.selectparameters import SelectParameters
        return SelectParameters.from_xml(tree)
        
    elif tree.tag == '{%s}subject' % ns.NMWG:
        from psapi.protocol.subject import Subject
        return Subject.from_xml(tree)
    
    elif tree.tag == '{%s}subject' % ns.IPERF2:
        from psapi.protocol.iperfsubject import IPerfSubject
        return IPerfSubject.from_xml(tree)
    
    elif tree.tag == '{%s}subject' % ns.SELECT:
        from psapi.protocol.selectsubject import SelectSubject
        return SelectSubject.from_xml(tree)
    
    elif tree.tag == '{%s}subject' % ns.NETUTIL:
        from psapi.protocol.netutilsubject import NetUtilSubject
        return NetUtilSubject.from_xml(tree)
    
    elif tree.tag == '{%s}interface' % ns.NMWGT:
        from psapi.protocol.interface import Interface
        return Interface.from_xml(tree)
    
    elif tree.tag == '{%s}metadata' % ns.NMWG:
        from psapi.protocol.metadata import Metadata
        return Metadata.from_xml(tree)
    
    elif tree.tag == '{%s}data' % ns.NMWG:
        from psapi.protocol.data import Data
        return Data.from_xml(tree)
    
    elif tree.tag == '{%s}message' % ns.NMWG:
        from psapi.protocol.message import Message
        return Message.from_xml(tree)
        
    elif tree.tag == '{%s}key' % ns.NMWG:
        from psapi.protocol.key import Key
        return Key.from_xml(tree)
        
    else:
        return None

def parse_timeseries(xml):
    """
    Parse any time series data
    """
    from psapi.protocol import namespaces as ns
    if isinstance(xml, str):
        tree = etree.fromstring(xml)
    else:
        tree = xml
    
    if tree.tag != '{%s}data' % ns.NMWG:
        raise Exception("Found element of type '%s' while expecting \
                        element of type '%s'" % \
                        (tree.tag, '{%s}data' % ns.NMWG))
        
    series = {}
    for child in tree.iterchildren():
        if not child.tag.endswith('}datum'):
            pass # TODO err or warn
        else:
            nsdatum = re.match("{(.*)}", child.tag).groups()[0]
            if nsdatum not in series:
                series[nsdatum] = []
            datum = dict(child.attrib)
            
            series[nsdatum].append(datum)
    
    if len(series) == 0:
        series = None
    return series
