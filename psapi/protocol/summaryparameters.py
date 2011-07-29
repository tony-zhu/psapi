#!/usr/bin/env python

"""
Represents Summary Parameters object
"""

__authors__ = [
    '"Ahmed El-Hassany" <<ahassany@udel.edu>',
  ]


from psapi.protocol import Parameters
from psapi.protocol import namespaces as ns


class SummaryParameters(Parameters):
    """summary:parameters object.
    paramters has to be a dict of key/value pairs
    """
    def __init__(self, parameters=None, object_id=None, ref_id=None):
        Parameters.__init__(self, parameters, object_id, ref_id)
    
    @staticmethod
    def from_xml(xml):
        return Parameters._parse_parameters(xml, SummaryParameters, ns.SUMMARY)

    def to_xml(self, parent=None, tostring=True):
        return self._parameters_to_xml(ns.SUMMARY, parent, tostring)

