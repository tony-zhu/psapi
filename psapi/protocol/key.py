#!/usr/bin/env python

"""
The key is used to return a 'pointer' or otherwise special piece
of identifying information in response to a request.
"""

__authors__ = [
    '"Ahmed El-Hassany" <ahassany@udel.edu>',
  ]

from lxml import etree

from psapi.protocol import Parameters
from psapi.protocol import PsObject
from psapi.protocol import namespaces as ns


class Key(PsObject):
    """See nmwg:key schema."""
    def __init__(self, parameters, object_id=None):
        PsObject.__init__(self, object_id, ref_id=None)
        self.parameters = parameters

    def __eq__(self, other):
        if other is None:
            return False
        if not hasattr(other, 'parameters'):
            return False
        if self.parameters != other.parameters:
            return False
        return True

    @staticmethod
    def from_xml(xml):
        tree = PsObject.assert_xml(xml, '{%s}key' % ns.NMWG)

        object_id = tree.get('id')
        params = None

        for child in tree.iterchildren():
            params = PsObject.from_xml(child)
            if not isinstance(params, Parameters):
                raise ValueError("Key only accepts children of type\
                                   parameters")

        return Key(params, object_id)

    def to_xml(self, parent=None, tostring=True):
        """Serialize to XML representation."""
        if parent is None:
            tree = etree.Element('{%s}key' % ns.NMWG, nsmap=ns.nsmap)
        else:
            tree = etree.SubElement(parent, '{%s}key' % ns.NMWG)

        if self.object_id is not None:
            tree.set('id', self.object_id)

        if self.parameters is not None:
            self.parameters.to_xml(tree, tostring=False)

        if tostring is True:
            return etree.tostring(tree, pretty_print=True)
        else:
            return tree
