#!/usr/bin/env python
"""
Specific SNMP Network Interface utilization Subject.

see http://anonsvn.internet2.edu/svn/nmwg/trunk/nmwg/schema/rnc/snmp.rnc
"""

__authors__ = [
    '"Ahmed El-Hassany" <<ahassany@udel.edu>',
  ]


from psapi.protocol import SNMPSubject
from psapi.protocol import namespaces as ns


class NetUtilSubject(SNMPSubject):
    """See netutil:subject schema."""
    def __init__(self, interface=None, object_id=None, ref_id=None):
        SNMPSubject.__init__(self, interface, object_id, ref_id)

    @staticmethod
    def from_xml(xml):
        return SNMPSubject._snmp_from_xml(NetUtilSubject, ns.NETUTIL, xml)

    def to_xml(self, parent=None, tostring=True):
        return self._snmp_to_xml(ns.NETUTIL, parent, tostring)