#!/usr/bin/env python
"""
Specific SNMP Network Interface discard Subject.

see http://anonsvn.internet2.edu/svn/nmwg/trunk/nmwg/schema/rnc/snmp.rnc
"""

__authors__ = [
    '"Ahmed El-Hassany" <<ahassany@udel.edu>',
  ]


from psapi.protocol import SNMPSubject
from psapi.protocol import namespaces as ns


class NetDiscardSubject(SNMPSubject):
    """See netdisc:subject schema."""
    def __init__(self, interface=None, object_id=None, ref_id=None):
        SNMPSubject.__init__(self, interface, object_id, ref_id)

    @staticmethod
    def from_xml(xml):
        return SNMPSubject._snmp_from_xml(NetDiscardSubject, ns.NETDISC, xml)

    def to_xml(self, parent=None, tostring=True):
        return self._snmp_to_xml(ns.NETDISC, parent, tostring)