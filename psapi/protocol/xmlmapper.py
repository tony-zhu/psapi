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
    """ Read XML and return the appropriate object. """
    if isinstance(xml, str):
        tree = etree.fromstring(xml)
    else:
        tree = xml
    
    from psapi.protocol import get_namespace_class
    class_def =  get_namespace_class(tree.tag)
    if class_def is None:
        return None
    else:
        return class_def.from_xml(tree)


def parse_timeseries(xml):
    """ Parse any time series data """
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
