#!/usr/bin/env python
"""
Pinger Subject, very similar to NMWG Subject
"""
__authors__ = [
    '"Ahmed El-Hassany" <<ahassany@udel.edu>',
  ]

from lxml import etree

from psapi.protocol import PsObject
from psapi.protocol import Subject
from psapi.protocol import namespaces as ns


class PingerSubject(Subject):
    """See pinger:subject schema."""
    def __init__(self, endpointpair=None, object_id=None, ref_id=None):
        Subject.__init__(self, endpointpair, object_id, ref_id)

    @staticmethod
    def from_xml(xml):
        tree = PsObject.assert_xml(xml, '{%s}subject' % ns.PINGER)
        object_id = tree.get('id')
        ref_id = tree.get('metadataIdRef')
        
        if len(tree.getchildren()) == 0:
            endpointpair = None
        elif len(tree.getchildren()) == 1:
            endpointpair = PsObject.from_xml(tree.getchildren()[0])
        else:
            pass # TODO raise err

        return PingerSubject(endpointpair, object_id, ref_id)

    def to_xml(self, parent=None, tostring=True):
        """Serialize to XML representation."""
        if parent is None:
            tree = etree.Element('{%s}subject' % ns.PINGER, nsmap=ns.nsmap)
        else:
            tree = etree.SubElement(parent, '{%s}subject' % ns.PINGER)

        if self.object_id is not None:
            tree.set('id', self.object_id)

        if self.ref_id is not None:
            tree.set('metadataIdRef', self.ref_id)

        if self.contents is None:
            pass
        elif isinstance(self.contents, PsObject):
            self.contents.to_xml(tree, False)

        if tostring:
            return etree.tostring(tree, pretty_print=True)
        else:
            return tree
