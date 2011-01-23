#!/usr/bin/env python
"""
Represents Metadata objects that have a subject, event types, and params.
"""

__authors__ = [
    '"Ahmed El-Hassany" <<ahassany@udel.edu>',
  ]

from lxml import etree

from psapi.protocol import PsObject
from psapi.protocol import Parameters
from psapi.protocol import Subject
from psapi.protocol import namespaces as ns


class Metadata(PsObject):
    """nmwg:metadata object."""
    def __init__(self, subject=None, event_types=None, parameters=None, \
                    object_id=None, ref_id=None):
        PsObject.__init__(self, object_id, ref_id)
        self.subject = subject
        self.event_types = event_types
        self.parameters = parameters

    def __eq__(self, other):
        if self.subject != other.subject:
            return False
        if self.event_types != other.event_types:
            return False
        if self.parameters != other.parameters:
            return False
        return True

    def __ne__(self, other):
        return not self.__eq__(other)

    @staticmethod
    def from_xml(xml):
        tree = PsObject.assert_xml(xml, '{%s}metadata' % ns.NMWG)
        object_id = tree.get('id')
        ref_id = tree.get('metadataIdRef')
        subject = None
        parameters = None
        event_types = []

        for child in tree.iterchildren():
            if child.tag == '{%s}eventType' % ns.NMWG:
                event_types.append(child.text)
            else:
                obj = PsObject.from_xml(child)
                if isinstance(obj, Subject):
                    subject = obj
                elif isinstance(obj, Parameters):
                    parameters = obj
                else:
                    pass  # TODO raise error or warn

        if len(event_types) == 0:
            event_types = None
        elif len(event_types) == 1:
            event_types = event_types[0]

        return Metadata(subject, event_types, parameters, object_id, \
                            ref_id)

    def to_xml(self, parent=None, tostring=True):
        """Serialize to XML representation."""
        if parent is None:
            tree = etree.Element('{%s}metadata' % ns.NMWG, nsmap=ns.nsmap)
        else:
            tree = etree.SubElement(parent, '{%s}metadata' % ns.NMWG)

        tree.set('id', self.object_id)

        if self.ref_id is not None:
            tree.set('metadataIdRef', self.ref_id)

        # Subject
        if hasattr(self.subject, 'to_xml'):
            self.subject.to_xml(tree, False)

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

        # Parameters
        if hasattr(self.parameters, 'to_xml'):
            self.parameters.to_xml(tree, False)

        if tostring:
            return etree.tostring(tree, pretty_print=True)
        else:
            return tree
