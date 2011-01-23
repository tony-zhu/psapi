#!/usr/bin/env python
"""
Lookup Service Summarization Subject
"""
__authors__ = [
    '"Ahmed El-Hassany" <<ahassany@udel.edu>',
  ]

from lxml import etree

from psapi.protocol import PsObject
from psapi.protocol import Subject
from psapi.protocol import namespaces as ns


class SummarySubject(Subject):
    """See summary:subject schema."""
    def __init__(self, contents=None, event_types=None, \
                    object_id=None, ref_id=None):
        Subject.__init__(self, contents, object_id, ref_id)
        object.__setattr__(self, 'event_types', event_types)

    @staticmethod
    def from_xml(xml):
        tree = PsObject.assert_xml(xml, '{%s}subject' % ns.SUMMARY)
        object_id = tree.get('id')
        ref_id = tree.get('metadataIdRef')

        contents = []
        event_types = []

        for child in tree.iterchildren():
            if child.tag == '{%s}eventType' % ns.NMWG:
                event_types.append(child.text)
            else:
                contents.append(PsObject.from_xml(child))

        if len(contents) == 0:
            contents = None
        elif len(contents) == 1:
            contents = contents[0]

        return SummarySubject(contents, event_types, object_id, ref_id)

    def to_xml(self, parent=None, tostring=True):
        """Serialize to XML representation."""
        if parent is None:
            tree = etree.Element('{%s}subject' % ns.SUMMARY, \
                                                        nsmap=ns.nsmap)
        else:
            tree = etree.SubElement(parent, '{%s}subject' % ns.SUMMARY)

        if self.object_id is not None:
            tree.set('id', self.object_id)

        if self.ref_id is not None:
            tree.set('metadataIdRef', self.ref_id)

        if self.contents is None:
            pass
        elif isinstance(self.contents, PsObject):
            self.contents.to_xml(tree, False)
        elif isinstance(self.contents, list):
            for cont in self.contents:
                if isinstance(cont, PsObject):
                    cont.to_xml(tree, False)
        #event_types
        if isinstance(self.event_types, list):
            events = self.event_types
        else:
            events = [self.event_types]

        for itr in events:
            if hasattr(itr, 'to_xml'):
                itr.to_xml(tree, False)
            else:
                event = etree.SubElement(tree, '{%s}eventType' % ns.NMWG)
                event.text = itr

        if tostring:
            return etree.tostring(tree, pretty_print=True)
        else:
            return tree
