#!/usr/bin/env python

"""
Represents Parameters object
"""

__authors__ = [
    '"Ahmed El-Hassany" <<ahassany@udel.edu>',
  ]

from psapi.protocol import Parameters
from psapi.protocol import namespaces as ns


class XQueryParameters(Parameters):
    """xquery:parameters object.
    paramters has to be a dict of key/value pairs
    """
    def __init__(self, parameters=None, object_id=None, ref_id=None):
        Parameters.__init__(self, parameters, object_id, ref_id)

    @staticmethod
    def from_xml(xml):
        return Parameters._parse_parameters(xml, XQueryParameters, ns.XQUERY)

    def to_xml(self, parent=None, tostring=True):
        return self._parameters_to_xml(ns.XQUERY, parent, tostring)
