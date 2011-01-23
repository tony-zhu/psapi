#!/usr/bin/env python
"""
A generic parent object for perfSONAR objects.
"""

__authors__ = [
    '"Ahmed El-Hassany" <<ahassany@udel.edu>',
  ]

import random
from lxml import etree
from psapi.protocol.xmlmapper import parse_psobject_from_xml


class PsObject(object):
    """Any perfSONAR objects contains two basic fields(id, referenceId).
    """
    def __init__(self, object_id=None, ref_id=None):
        """Initialize new PsObject."""
        if object_id is None:
            self.object_id = PsObject.generate_id()
        else:
            self.object_id = object_id
        self.ref_id = ref_id

    def to_xml(self, parent=None, tostring=True):
        """Serialize to XML representation."""
        pass

    @staticmethod
    def from_xml(xml):
        """Creates PsObject from XML input."""
        return parse_psobject_from_xml(xml)

    @staticmethod
    def generate_id():
        """Generates new random ID."""
        return "GenID.%i" % random.randint(100, 100000000)

    @staticmethod
    def assert_xml(xml, name):
        """
        Asserts the input xml (string or etree object) is valid fully
        qualified name.
        """
        if isinstance(xml, str):
            tree = etree.fromstring(xml)
        else:
            tree = xml

        if tree.tag != name:
            raise Exception("Found element of type '%s' while expecting\
                        element of type '%s'" % (tree.tag, name))
        return tree
