#!/usr/bin/env python

"""NMTB Address representation.
"""

__authors__ = [
    '"Ahmed El-Hassany" <<ahassany@udel.edu>',
  ]

from lxml import etree

from psapi.protocol import PsObject
from psapi.protocol import namespaces as ns

from psapi.utils.ipaddress import get_address_type


class Address(PsObject):
    """See nmtb:address schema."""
    def __init__(self, address):
        PsObject.__init__(self, None, None)
        self.address = address
        self.address_type = get_address_type(address)

    def __eq__(self, other):
        if not isinstance(self, other):
            return False
        if self.address != other.address:
            return False
        return True

    def __ne__(self, other):
        return not self.__eq__(other)

    @staticmethod
    def from_xml(xml):
        tree = PsObject.assert_xml(xml, '{%s}address' % ns.NMTB)
        address = tree.text
        return Address(address)

    def to_xml(self, parent=None, tostring=True):
        """Serialize to XML representation."""
        if parent is None:
            tree = etree.Element('{%s}address' % ns.NMTB, nsmap=ns.nsmap)
        else:
            tree = etree.SubElement(parent, '{%s}address' % ns.NMTB)

        if self.address is not None:
            tree.text = self.address
            tree.set('type', self.address_type)

        if tostring is True:
            return etree.tostring(tree, pretty_print=True)
        else:
            return tree
