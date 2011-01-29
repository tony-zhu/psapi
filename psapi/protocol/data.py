#!/usr/bin/env python

"""Represents Data object

TODO: Needs a better way of identifying time series
"""

__authors__ = [
    '"Ahmed El-Hassany" <<ahassany@udel.edu>',
  ]

from lxml import etree

from psapi.protocol import Key
from psapi.protocol import PsDatum
from psapi.protocol import PsObject
from psapi.protocol import Metadata
from psapi.protocol import namespaces as ns
from psapi.protocol.xmlmapper import parse_timeseries


class Data(PsObject):
    """nmwg:data object."""
    def __init__(self, data=None, object_id=None, ref_id=None):
        PsObject.__init__(self, object_id, ref_id)
        self.data = data

    def __eq__(self, other):
        if self.object_id != other.object_id:
            return False
        if self.ref_id != other.ref_id:
            return False
        if self.data != other.data:
            return False
        return True

    def __ne__(self, other):
        return not self.__eq__(other)

    def __getattribute__(self,name):
        try:
            return object.__getattribute__(self, name)
        except AttributeError:
            return getattr(object.__getattribute__(self, 'data'), name)

    @staticmethod
    def from_xml(xml):
        tree = PsObject.assert_xml(xml, '{%s}data' % ns.NMWG)

        object_id = tree.get('id')
        ref_id = tree.get('metadataIdRef')

        first_child = tree.iterchildren().next()
        if first_child.tag == '{%s}key' % ns.NMWG:
            data = Key.from_xml(first_child)
        elif first_child.tag == '{%s}metadata' % ns.NMWG:
            data = Metadata.from_xml(first_child)
        elif first_child.tag == '{%s}datum' % ns.PSSERVICE:
            data = PsDatum.from_xml(first_child)
        elif first_child.tag == '{%s}datum' % ns.NMWGR:
            data = first_child.text
        else:
            data = parse_timeseries(tree)

        return Data(data, object_id, ref_id)

    def __datum_to_xml(self, datumns, datum, parent):
        """Create a ns:datum element"""
        tree = etree.SubElement(parent, '{%s}datum' % datumns)
        for key in datum:
            if key == 'value':
                tree.text = datum[key]
            else:
                tree.set(key, datum[key])

    def to_xml(self, parent=None, tostring=True):
        """Serialize to XML representation."""
        if parent is None:
            tree = etree.Element('{%s}data' % ns.NMWG, nsmap=ns.nsmap)
        else:
            tree = etree.SubElement(parent, '{%s}data' % ns.NMWG)

        if self.object_id is None:
            self.object_id = PsObject.generate_id()

        tree.set('id', self.object_id)

        if self.ref_id is not None:
            tree.set('metadataIdRef', self.ref_id)

        if self.data is not None:
            for datumns in self.data:
                for datum in self.data[datumns]:
                    self.__datum_to_xml(datumns, datum, tree)

        if tostring:
            return etree.tostring(tree, pretty_print=True)
        else:
            return tree
